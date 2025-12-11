import pandas as pd

from src.config import PROCESSED_DIR, TEXT_SUMMARIES_DIR

# Folder name with a space, matching your repo
FORECAST_DIR = PROCESSED_DIR / "forecast output"


def _pick_year_col(df: pd.DataFrame, filename: str) -> str:
    """Choose the year column."""
    cols = list(df.columns)

    if "Year" in cols:
        return "Year"
    if "year" in cols:
        return "year"

    year_like = [c for c in cols if "year" in c.lower()]
    if year_like:
        return year_like[0]

    # fallback: numeric column that looks like calendar years
    for c in cols:
        s = df[c]
        if not pd.api.types.is_numeric_dtype(s):
            continue
        vals = pd.to_numeric(s, errors="coerce").dropna()
        if vals.empty:
            continue
        frac_plausible = ((vals >= 2000) & (vals <= 2100)).mean()
        if frac_plausible > 0.8:
            return c

    raise ValueError(
        f"Could not identify a year column in {filename}. Columns: {cols}"
    )


def _pick_ev_col(df: pd.DataFrame, filename: str) -> str:
    """Choose the EVs-per-1000 forecast column."""
    cols = list(df.columns)

    # most specific first
    for target in [
        "EVs_per_1000_forecast_panel_baseline",
        "EVs_per_1000_forecast_panel_accelerated",
        "ev_per_1000_forecast",
        "ev_per_1000",
    ]:
        if target in cols:
            return target

    ev_like = [c for c in cols if "ev" in c.lower()]
    if ev_like:
        return ev_like[0]

    # fallback: last numeric column
    numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
    if numeric_cols:
        return numeric_cols[-1]

    raise ValueError(
        f"Could not identify an EV forecast column in {filename}. Columns: {cols}"
    )


def _load_forecast(kind: str) -> tuple[pd.DataFrame, str, str]:
    """
    Load a forecast file for 'baseline' or 'accelerated' and
    return (yearly_mean_df, year_col, ev_col).
    """
    kind = kind.lower()
    pattern = f"forecast_panel_{kind}.csv"
    path = FORECAST_DIR / pattern

    if not path.exists():
        raise FileNotFoundError(
            f"Expected forecast file {pattern} not found in {FORECAST_DIR}"
        )

    df = pd.read_csv(path)
    year_col = _pick_year_col(df, path.name)
    ev_col = _pick_ev_col(df, path.name)

    # aggregate to national mean per year
    yearly = (
        df.groupby(year_col)[ev_col]
        .mean()
        .reset_index()
        .sort_values(year_col)
    )
    return yearly, year_col, ev_col


def run_forecast_summary():
    """
    RQ3 summary: short-run EV adoption forecasts (2020–2023-based)
    using panel-based baseline and accelerated scenarios.

    Expects in `data/processed/forecast output/`:
      - forecast_panel_baseline.csv
      - forecast_panel_accelerated.csv
    """

    # ---- Load baseline & accelerated forecasts ----
    base_yearly, year_col_base, base_col = _load_forecast("baseline")
    accel_yearly, year_col_accel, accel_col = _load_forecast("accelerated")

    # keep only forecast years (> 2023)
    base_fore = base_yearly[base_yearly[year_col_base] > 2023].copy()
    accel_fore = accel_yearly[accel_yearly[year_col_accel] > 2023].copy()

    if base_fore.empty or accel_fore.empty:
        raise ValueError(
            "No forecast years found (> 2023). "
            "Check forecast_panel_baseline/accelerated.csv contents."
        )

    start_year = int(base_fore[year_col_base].min())
    end_year = int(base_fore[year_col_base].max())

    base_final = float(
        base_fore.loc[base_fore[year_col_base] == end_year, base_col].iloc[0]
    )
    accel_final = float(
        accel_fore.loc[accel_fore[year_col_accel] == end_year, accel_col].iloc[0]
    )

    if base_final > 0:
        lift_pct = (accel_final - base_final) / base_final * 100.0
    else:
        lift_pct = float("nan")

    # CAGR from 2023 to final year
    base_2023 = base_yearly[base_yearly[year_col_base] == 2023]
    if not base_2023.empty:
        base_2023_val = float(base_2023[base_col].iloc[0])
        n_years = end_year - 2023
        if base_2023_val > 0 and n_years > 0:
            base_cagr = (base_final / base_2023_val) ** (1.0 / n_years) - 1.0
            accel_cagr = (accel_final / base_2023_val) ** (1.0 / n_years) - 1.0
        else:
            base_cagr = float("nan")
            accel_cagr = float("nan")
    else:
        base_cagr = float("nan")
        accel_cagr = float("nan")

    # ---- Write text summary ----
    TEXT_SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TEXT_SUMMARIES_DIR / "forecast_ev_summary.txt"

    lines = []
    lines.append("RQ3: Short-run EV adoption forecasts (2020–2023-based)\n")
    lines.append("-----------------------------------------------------\n\n")
    lines.append(
        "This summary compares national EV adoption forecasts "
        "(EVs per 1,000 residents, averaged across states) under:\n"
        "  (1) a baseline charging-growth scenario, and\n"
        "  (2) an accelerated charging-growth scenario.\n\n"
    )

    lines.append(f"Forecast horizon: {start_year}–{end_year}\n\n")
    lines.append("Final-year national EV adoption (EVs per 1,000 residents):\n")
    lines.append(f"  Baseline scenario    : {base_final:.2f}\n")
    lines.append(f"  Accelerated scenario : {accel_final:.2f}\n")
    if base_final > 0:
        lines.append(
            f"  Relative lift in {end_year} (accelerated vs baseline): "
            f"{lift_pct:.1f}%\n"
        )

    lines.append("\nApproximate compound annual growth from 2023 to final year:\n")
    lines.append(f"  Baseline CAGR   : {base_cagr * 100:.1f}% per year\n")
    lines.append(f"  Accelerated CAGR: {accel_cagr * 100:.1f}% per year\n")

    lines.append(
        "\nInterpretation (informal):\n"
        f"- Over {start_year}–{end_year}, both scenarios imply continued growth "
        "in EV adoption relative to 2023.\n"
        "- The accelerated scenario reaches a higher national EVs-per-1,000 "
        "level than the baseline, summarizing how faster infrastructure\n"
        "  build-out could be associated with higher short-run EV penetration.\n"
        "- These are short-run, scenario-based projections rather than precise "
        "long-run predictions.\n"
    )

    with out_path.open("w") as f:
        for line in lines:
            f.write(line)

    print(f"Saved RQ3 forecast summary to {out_path}")


if __name__ == "__main__":
    run_forecast_summary()
