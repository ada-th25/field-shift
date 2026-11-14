# Validation: multi-site stress test and real-world comparison

Two checks on the model's outputs: whether the climate filter behaves
sensibly across very different climates, and whether the Iowa
recommendation lines up with real published agronomy research rather than
just looking plausible.

## Multi-site stress test

Same pipeline, same `crops.json`, three climates chosen to be as different
as possible, run via `python scripts/demo.py <lat> <lon>`:

| Site | Climate | Crops excluded (too cold/hot for any viable window) | Top-ranked rotation |
|---|---|---|---|
| Ames, Iowa (42.03, -93.63) | Humid continental | None | alfalfa → maize → alfalfa (RSI 1.809) |
| Reykjavik, Iceland (64.13, -21.90) | Subarctic | maize, alfalfa | soybean → cereal_rye_cover → soybean (RSI 1.559) |
| Singapore (1.35, 103.82) | Tropical | None | alfalfa → maize → alfalfa (RSI 2.070) |

*Numbers above include the erosion and revenue scoring changes; re-run `scripts/demo.py <lat> <lon>` for all three sites if `rotation_scoring.py` changes again.*

What this shows: the climate filter correctly drops maize and alfalfa for
Iceland (both need warmer conditions than any window in Iceland's year
provides) while leaving Iowa unaffected. It also exposes a real limitation
worth stating plainly: Singapore keeps the full crop list, including
winter wheat and alfalfa, because the filter only checks temperature — it
doesn't know winter wheat needs a vernalization period and short days,
things a temperature-only check can't see. That's an honest limitation,
not a hidden one: **the filter prevents the model from being obviously
wrong (recommending maize in the Arctic), it doesn't guarantee full
agronomic correctness everywhere.**