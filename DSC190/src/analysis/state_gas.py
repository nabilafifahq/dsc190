import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
from src.config import PANEL_FILE, TEXT_SUMMARIES_DIR, FIGURES_DIR

def run_state_gas_fe():
    """
    State-level panel regression of EV adoption on gas prices (2016-2023)
    Model: log(ev_per_1000) ~ log(gas_real_2023) + year_centered + state FE
    Generates diagnostic plots for the Final Report.
    """
    # 1. Load and Prep Data
    panel = pd.read_csv(PANEL_FILE)
    df = panel.copy()

    # Filter for the years 2016-2023
    df = df[(df["year"] >= 2016) & (df["year"] <= 2023)]

    # Keep needed columns and drop missing
    cols = ["state", "year", "ev_per_1000", "gas_real_2023"]
    df = df[cols].dropna()

    # Require strictly positive values for logs
    df = df[(df["ev_per_1000"] > 0) & (df["gas_real_2023"] > 0)].copy()

    # Logs + centered year
    df["log_ev_per_1000"] = np.log(df["ev_per_1000"])
    df["log_gas_real_2023"] = np.log(df["gas_real_2023"])
    df["year_centered"] = df["year"] - df["year"].mean()

    # 2. Run Regression (Clustered SEs)
    formula = "log_ev_per_1000 ~ log_gas_real_2023 + year_centered + C(state)"
    model = smf.ols(formula, data=df)
    results = model.fit(
        cov_type="cluster",
        cov_kwds={"groups": df["state"]},
    )

    # 3. Save Text Summary
    coef = results.params["log_gas_real_2023"]
    se = results.bse["log_gas_real_2023"]
    ci_low = coef - 1.96 * se
    ci_high = coef + 1.96 * se

    lines = []
    lines.append("=== State-level FE regression (2016-2023) ===\n")
    lines.append(f"Formula: {formula}\n\n")
    lines.append(results.summary().as_text())
    lines.append("\n\nElasticity interpretation (log-log):\n")
    lines.append(
        f"  coef(log_gas_real_2023) = {coef:.3f}\n"
        f"  95% CI = [{ci_low:.3f}, {ci_high:.3f}]\n"
    )
    
    out_path = TEXT_SUMMARIES_DIR / "state_gas_summary.txt"
    with out_path.open("w") as f:
        for line in lines:
            f.write(line)
    print(f"Regression summary saved to {out_path}")

    # 4. Generate 4-Panel Diagnostic Plots (Advanced Analysis)
    fitted_vals = results.fittedvalues
    residuals = results.resid

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot A: Predicted vs Actual
    axes[0, 0].scatter(df["log_ev_per_1000"], fitted_vals, alpha=0.5, color='purple')
    axes[0, 0].plot([df["log_ev_per_1000"].min(), df["log_ev_per_1000"].max()], 
                    [df["log_ev_per_1000"].min(), df["log_ev_per_1000"].max()], 'r--')
    axes[0, 0].set_title("Predicted vs Actual log(EV Rate)")
    axes[0, 0].set_xlabel("Actual log(EV Rate)")
    axes[0, 0].set_ylabel("Predicted log(EV Rate)")

    # Plot B: Histogram of Residuals
    sns.histplot(residuals, kde=True, ax=axes[0, 1], color='skyblue')
    axes[0, 1].set_title("Histogram of Residuals")
    axes[0, 1].set_xlabel("Residuals")

    # Plot C: Q-Q Plot (Normality)
    sm.qqplot(residuals, line='45', fit=True, ax=axes[1, 0])
    axes[1, 0].set_title("Normal Q-Q Plot")

    # Plot D: Residuals vs Fitted (Homoscedasticity)
    axes[1, 1].scatter(fitted_vals, residuals, alpha=0.5, color='black')
    axes[1, 1].axhline(0, color='red', linestyle='--')
    axes[1, 1].set_title("Residuals vs Fitted Values")
    axes[1, 1].set_xlabel("Fitted Values")
    axes[1, 1].set_ylabel("Residuals")

    plt.tight_layout()
    plot_path = FIGURES_DIR / "state_gas_diagnostics.png"
    plt.savefig(plot_path, dpi=150)
    print(f"Diagnostic plots saved to {plot_path}")
    plt.close()

if __name__ == "__main__":
    run_state_gas_fe()