"""FastAPI app wrapping the rotation scoring engine for the frontend.

Run from backend/: uvicorn app.main:app --reload
"""
import json
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.data.nasa_power import fetch_power_daily
from app.data.soilgrids import fetch_soilgrids
from app.engine.candidates import generate_candidate_sequences
from app.engine.climate_suitability import (
    climate_mismatched_crops,
    filter_climate_suitable_crops,
    frost_days_in_best_window,
)
from app.engine.evapotranspiration import crop_water_demand_mm, et0_penman_monteith
from app.engine.rotation_scoring import (
    EnvironmentalBaseline,
    RotationWeights,
    compute_impact_metrics,
    generate_risks_and_gaps,
    score_sequence,
    single_year_perennials,
)
from app.schemas import FarmRequest, FarmResponse

REPO_ROOT = Path(__file__).resolve().parents[2]
CROPS_PATH = REPO_ROOT / "data" / "crops.json"
FRONTEND_PATH = REPO_ROOT / "frontend"

app = FastAPI(title="Harvest Heroes Crop Rotation API")

# Open CORS for the hackathon demo; tighten if this ever goes beyond that.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory=FRONTEND_PATH), name="assets")


@app.get("/")
def index():
    return FileResponse(FRONTEND_PATH / "index.html")


@app.get("/planner")
def planner():
    return FileResponse(FRONTEND_PATH / "planner.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/crops")
def list_crops():
    crops = json.loads(CROPS_PATH.read_text())
    return {name: data for name, data in crops.items() if not name.startswith("_")}


@app.post("/rotations", response_model=FarmResponse)
def rank_rotations(request: FarmRequest):
    crops = json.loads(CROPS_PATH.read_text())

    try:
        power_df = fetch_power_daily(request.lat, request.lon, start=request.start_date, end=request.end_date)
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="NASA POWER weather data is unavailable or timed out for this location. Try again in a moment.",
        )
    try:
        soil = fetch_soilgrids(request.lat, request.lon)
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="ISRIC SoilGrids soil data is unavailable or timed out for this location. Try again in a moment.",
        )

    # GWETROOT/GWETTOP are land-surface reanalysis fields: NASA POWER has no
    # value for them over open ocean, and forward-filling can't recover a
    # column that's missing for the entire requested window. Left unchecked,
    # that NaN silently propagates into every downstream score and crashes
    # JSON serialization of the response instead of failing with a clear
    # message.
    required_columns = ["T2M", "T2M_MAX", "T2M_MIN", "RH2M", "WS2M", "ALLSKY_SFC_SW_DWN",
                         "PRECTOTCORR", "GWETROOT", "GWETTOP"]
    if power_df[required_columns].isna().any().any():
        raise HTTPException(
            status_code=422,
            detail="NASA POWER has no usable land-surface weather data at this location "
            "(likely open ocean, ice sheet, or another location outside its land-surface "
            "model coverage). Choose a location on land.",
        )

    et0 = et0_penman_monteith(power_df, lat_deg=request.lat)

    soil_is_estimated = soil.get("soc_g_kg") is None
    baseline = EnvironmentalBaseline(
        seasonal_precip_mm=float(power_df["PRECTOTCORR"].sum()),
        mean_root_zone_wetness=float(power_df["GWETROOT"].mean()),
        soil_organic_carbon_g_kg=soil["soc_g_kg"] or 15.0,
        soil_carbon_is_estimated=soil_is_estimated,
    )

    weights = RotationWeights(**request.priority_weights)
    suitable_crops, excluded_crops = filter_climate_suitable_crops(crops, power_df)
    candidates = generate_candidate_sequences(suitable_crops, sequence_length=request.sequence_length)

    baseline_crop_name = crops.get("_baseline_crop", "maize")
    baseline_crop = {**crops[baseline_crop_name], "_name": baseline_crop_name}
    baseline_water_demand_mm = crop_water_demand_mm(et0, baseline_crop)

    def score_named_sequence(sequence: list[dict], is_current: bool = False) -> dict:
        water_demands = [crop_water_demand_mm(et0, crop) for crop in sequence]
        result = score_sequence(sequence, baseline, water_demands, weights)
        result["impact_metrics"] = compute_impact_metrics(
            sequence, water_demands, baseline_crop, baseline_water_demand_mm
        )
        result["metrics"] = {
            "water_demand_mm": round(sum(water_demands), 1),
            "nitrogen_balance_kg_ha": sum(crop["nitrogen_balance_kg_ha"] for crop in sequence),
            "uncovered_days": sum(365 - crop["season_length_days"] for crop in sequence),
        }
        frost_risk_crops = list(dict.fromkeys(
            crop["_name"] for crop in sequence if frost_days_in_best_window(power_df, crop) > 0
        ))
        # Recommended candidates are already climate-filtered upstream, so this
        # is always empty for them; current_rotation skips that filter on
        # purpose (it's what the farmer already does), so it needs its own check.
        mismatched = climate_mismatched_crops(sequence, power_df) if is_current else []
        flood_irrigated_crops = list(dict.fromkeys(
            crop["_name"] for crop in sequence if crop.get("flood_irrigated")
        ))
        result["risks_and_gaps"] = generate_risks_and_gaps(
            frost_risk_crops, soil_is_estimated, single_year_perennials(sequence), mismatched,
            flood_irrigated_crops,
        )
        return result

    results = [score_named_sequence(sequence) for sequence in candidates]
    results.sort(key=lambda r: r["rsi"], reverse=True)

    current_rotation = None
    if request.current_rotation:
        unknown = [name for name in request.current_rotation if name not in crops]
        if unknown:
            raise HTTPException(status_code=400, detail=f"Unknown crop(s) in current_rotation: {unknown}")
        current_sequence = [{**crops[name], "_name": name} for name in request.current_rotation]
        current_rotation = score_named_sequence(current_sequence, is_current=True)

    return FarmResponse(
        soil=soil,
        mean_et0_mm_day=float(et0.mean()),
        top_rotations=results[: request.top_n],
        excluded_crops=excluded_crops,
        current_rotation=current_rotation,
        rainfall_mm=float(power_df["PRECTOTCORR"].sum()),
        root_wetness=float(power_df["GWETROOT"].mean()),
        data_window=[request.start_date, request.end_date],
    )
