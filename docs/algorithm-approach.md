# Data science approach — status and open questions

Covers what's built, why it's built this way, what it deliberately leaves
out, and where I'd like a second opinion before we split up further work.

## The core idea

Given a farm location, recommend which 3-year crop rotation best balances
soil health, water sustainability, and drought resilience, using live NASA
Earth observation data rather than static lookup tables. Output a ranked
list of rotations with a score breakdown the frontend can turn into
"why this rotation" visuals.

Demo location: Central Iowa (Ames, 42.0308, -93.6319) was chosen over
Punjab/Spain for richest public validation data (USDA yield history) if we
want to sanity-check outputs later.

