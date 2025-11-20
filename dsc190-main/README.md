# Evaluating the Influence of Fuel Costs and Charging Infrastructure on National and State-Level Electric Vehicle Adoption
This repository contains my version of the DSC190 midterm project. It focuses on electric vehicle (EV) adoption across U.S. states and combines multiple public datasets (EV registrations, charging infrastructure, population, and gasoline prices) into a single panel-style dataset for exploration and forecasting.

## Project Goal & Approach

**Goal**

Understand how EV adoption differs across states and over time, and how it is related to the build-out of public charging infrastructure. Use this relationship to create simple 5-year forecasts of EV adoption under different charging-infrastructure scenarios.

**Approach**

1. **Build a unified state–year dataset**
   - Parse and clean raw data on EV registrations, public charging ports, state population, and gasoline prices.
   - Merge these sources into a single panel dataset by state and year.
   - Create per-capita metrics such as:
     - EVs per 1,000 people
     - Charging ports per 100,000 people

2. **Describe and visualize EV adoption**
   - Compute summary statistics for EV adoption and charging density.
   - Plot trends over time for the top EV-adopting states.
   - Visualize the relationship between EV adoption and charging ports.

3. **Model the relationship between chargers and EVs**
   - Fit a panel regression with state fixed effects:
     - EVs per 1,000 as the outcome
     - Chargers per 100k and a year trend as predictors
   - Interpret how changes in charging density are associated with changes in EV adoption, after accounting for state-specific differences.

4. **Forecast EV adoption**
   - Use the panel model to generate 5-year forecasts under:
     - A **baseline** scenario where charging ports grow at their historical rate.
     - An **accelerated** scenario where charging ports grow faster than in the past.
   - For comparison, fit simple ARIMA time-series models to EV adoption for each state and produce separate 5-year forecasts.

---
## Repository Structure

```text
dsc190/
│
├── Datasets/                 # Raw datasets (CSV/XLSX): EV registrations, ports, population, gas prices
│
├── data/
│   ├── processed/            # Cleaned data, merged panel, forecasts, and generated figures
│   └── raw/                  # (Optional) Raw data location used by the parsing scripts
│
├── notebooks/                # Jupyter notebooks for exploratory analysis (if used)
│
├── reports/                  # Plots and figures for write-ups or slides
│
├── src/
│   ├── parsing/              # Scripts to read and clean each raw dataset
│   │   ├── parse_ev_registrations.py
│   │   ├── parse_ports.py
│   │   ├── parse_population.py
│   │   └── parse_gas_prices.py
│   │
│   ├── cleaning/             # Data merging / feature construction
│   │   └── build_panel.py    # Builds state–year panel with per-capita metrics
│   │
│   ├── analysis/             # Summary stats and forecasting
│   │   ├── descriptives.py           # Basic summaries of the panel dataset
│   │   └── forecast_ev_panel.py      # Panel + ARIMA forecasts for EV adoption
│   │
│   └── visualization/        # Plotting utilities
│       └── plots.py          # Line plot for top states, scatter of ports vs EVs
│
├── src/config.py             # Central paths for raw/processed data files
│
└── requirements.txt          # Python dependencies for the project
```
## Data and Key Outputs

- **Raw data:** CSV/XLSX files in `Datasets/`.
- **Cleaned & merged data:**
  - `data/processed/ev_registrations_clean.csv`
  - `data/processed/ports_clean.csv`
  - `data/processed/population_states.csv`
  - `data/processed/gas_prices_clean.csv`
  - `data/processed/panel.csv` (main state–year dataset)
- **Forecasts (when scripts are run):**
  - `data/processed/forecast_panel_baseline.csv`
  - `data/processed/forecast_panel_accelerated.csv`
  - `data/processed/forecast_arima.csv`
- **Figures:**
  - `data/processed/ev_per_1000_top_states.png`
  - `data/processed/ports_vs_ev_scatter.png`

## Setup

1. Install Python (version compatible with `requirements.txt`).
2. From the project root, install dependencies:

   pip install -r requirements.txt

## Reproducing the Analysis

From the project root:

1. **Parse raw datasets** (creates cleaned CSVs in `data/processed/`):

   - Run the scripts in `src/parsing/`, for example:
     - parse_ev_registrations.py
     - parse_ports.py
     - parse_population.py
     - parse_gas_prices.py

2. **Build the panel dataset**:

   - Run `src/cleaning/build_panel.py`  
     → writes `data/processed/panel.csv`

3. **Explore and model**:

   - Run `src/analysis/descriptives.py` for basic summaries.  
   - Run `src/analysis/forecast_ev_panel.py` to create forecast CSVs.

4. **Generate plots**:

   - Run `src/visualization/plots.py` to produce figures stored in `data/processed/`.
