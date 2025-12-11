# Evaluating the Influence of Fuel Costs and Charging Infrastructure on National and State-Level Electric Vehicle Adoption (2016–2023)

This repository contains my version of the DSC 190 project. It builds a **state–year panel (2016–2023)** that combines EV registrations, public charging infrastructure, population, and gasoline prices to explore how fuel costs and charging access relate to electric vehicle (EV) adoption over time in the United States.

---

## Project Overview

### Goal

Quantify how EV adoption differs across states and over time (2016–2023), and evaluate the role of:

- Real gasoline prices (inflation-adjusted to 2023 dollars)
- Public charging ports per capita
- Population and state-specific differences

The project also produces simple forecasts of EV adoption under different charging infrastructure growth scenarios.

### Main Research Questions

1. **RQ1 → Charging ports and EV adoption**  
   How strongly is the availability of public charging infrastructure (ports per 100,000 residents) associated with EV adoption (EVs per 1,000 residents) across U.S. states from **2016–2023**?

2. **RQ2 → Gas prices and EV adoption**  
   How are real gasoline prices associated with EV adoption (EVs per 1,000 residents) at the national and state level over **2016–2023**?

3. **RQ3 → Forecasting under alternative charging scenarios**  
   Under baseline versus accelerated growth in public charging infrastructure, how is national EV adoption projected to evolve in the next few years?

### Guiding Questions

These more intuitive questions motivated the analysis:

1. How have EVs per 1,000 people evolved nationally and across states since **2016**?  
2. How strongly are gasoline prices associated with changes in EV adoption?  
3. How does public charging infrastructure per capita relate to EV penetration?  
4. How might EV adoption evolve over the next five years under baseline vs. accelerated charging build-out?

---

## Approach

1. **Build a unified state–year dataset (2016–2023)**  
   - Parse and clean raw data on:
     - EV registrations by state and year
     - Public charging ports
     - State population
     - Gasoline prices (in 2023 dollars)
   - Merge these sources into a single panel dataset by **state × year**.
   - Create per-capita metrics such as:
     - EVs per 1,000 people
     - Ports per 100,000 people

2. **Describe trends and heterogeneity**
   - Summarize EV adoption and charging infrastructure by state and year.
   - Identify top/bottom states in EVs per 1,000 residents.
   - Examine how charging ports per capita and gas prices have changed over time.

3. **Relate charging infrastructure, gas prices, and EV adoption**
   - Fit panel regressions with state fixed effects:
     - Outcome: EVs per 1,000 people
     - Predictors: ports per 100k, log ports, real gas prices, and a year trend
   - Use both log–log specifications and level models.
   - Interpret how changes in charging density and gas prices are associated with changes in EV adoption, after accounting for time-invariant state differences.

4. **Forecast EV adoption**
   - Use the national series to generate multi-year forecasts of EVs per 1,000 people under:
     - A **baseline** scenario where charging ports grow at a historical rate.
     - An **accelerated** scenario with faster charging build-out.
   - Compare how EV adoption trajectories differ across scenarios.

---

## Repository Structure

```text
.
│
├── Datasets/                       # Raw datasets (CSV/XLSX): EV regs, ports, population, gas prices
│   ├── 2016_ports.csv
│   ├── 2017_ports.csv
│   ├── 2018_ports.csv
│   ├── 2019_ports.csv
│   ├── 2020_ports.csv
│   ├── 2021_ports.csv
│   ├── 2022_ports.csv
│   ├── 2023_ports.csv
│   ├── ev_registrations_2016.csv
│   ├── ev_registrations_2017.csv
│   ├── ev_registrations_2018.csv
│   ├── ev_registrations_2019.csv
│   ├── ev_registrations_2020.csv
│   ├── ev_registrations_2021.csv
│   ├── ev_registrations_2022.csv
│   ├── ev_registrations_2023.csv
│   ├── nst-est2020-alldata.csv          # Census population vintage 2020 (for 2016–2019)
│   ├── population_estimate.csv          # Census population vintage 2024 (for 2020–2023)
│   ├── 10641_gasoline_prices_by_year_1-26-24.xlsx
│   └── 10567_pev_sales_2-28-20.xlsx     # (optional / exploratory)
│
├── data/
│   └── processed/
│       ├── cleaned table/               # Cleaned / merged tables
│       │   ├── gas_prices_clean.csv
│       │   ├── ports_clean.csv
│       │   ├── population_states.csv
│       │   └── panel.csv                # Main state–year panel (2016–2023)
│       │
│       ├── forecast output/             # Forecast CSVs (baseline vs accelerated)
│       ├── text summaries/              # .txt summaries for write-up (e.g., gas_vs_ev_summary.txt)
│       └── figures/                     # Saved plots used in the report / slides
│
├── notebooks/                          # Jupyter notebooks for exploratory analysis (optional)
│
├── reports/                            # Slides / write-ups
│
├── src/
│   ├── config.py                       # Central paths: PROJECT_ROOT, RAW_DIR, PROCESSED_DIR, etc.
│   │
│   ├── datadownload/
│   │   └── download_ev_registrations.py   # Downloads & saves AFDC EV registration tables (2016–2019+)
│   │
│   ├── parsing/
│   │   ├── parse_ev_registrations.py   # parses EV registration CSVs into a consistent format
│   │   ├── parse_gas_prices.py         # cleans gas price Excel → real 2023 $/gal
│   │   ├── parse_population.py         # earlier population parsing (superseded by population_states)
│   │   └── parse_ports.py              # cleans AFDC port counts by state/year
│   │
│   ├── cleaning/
│   │   ├── population_states.py           # Builds 2016–2023 state population panel
│   │   └── build_panel.py                 # Builds state–year panel with per-capita metrics
│   │
│   ├── analysis/
│   │   ├── descriptives.py              # Basic descriptives / sanity checks
│   │   ├── gas_vs_ev.py                 # RQ2: national gas vs EV (correlations + OLS on 2020–2023)
│   │   ├── logspec.py                   # RQ1: log–log FE model for ports vs EV (state FE)
│   │   ├── state_gas.py                 # State-level FE model: EV vs gas with state fixed effects
│   │   ├── forecast_ev_panel.py         # Panel-based EV forecasting / scenario setup (by state)
│   │   └── forecast_summary.py          # National EV adoption forecasts + text summary for the report
│   │
│   └── visualization/                     # Plotting utilities 
│       └── plots.py                       # Helper functions for line charts / scatters
│
├── src/config.py                       # central paths for raw/processed data
├── README.md                           # this file
└── requirements.txt                    # Python dependencies
```
