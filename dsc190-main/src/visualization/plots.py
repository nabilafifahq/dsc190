import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.config import PANEL_FILE, PROCESSED_DIR

def lineplot_top_states_ev(panel, top_n=5):
    # Find top N states in latest year by EV per 1000
    latest_year = panel["year"].max()
    latest = panel[panel["year"] == latest_year].copy()
    top_states = (
        latest.sort_values("ev_per_1000", ascending=False)
              .head(top_n)["state"]
              .tolist()
    )

    subset = panel[panel["state"].isin(top_states)].copy()

    plt.figure(figsize=(8, 5))
    sns.lineplot(
        data=subset,
        x="year",
        y="ev_per_1000",
        hue="state",
        marker="o"
    )
    plt.title(f"EVs per 1,000 People, {top_n} Leading States")
    plt.ylabel("EVs per 1,000 people")
    plt.tight_layout()
    out_path = PROCESSED_DIR / "ev_per_1000_top_states.png"
    plt.savefig(out_path, dpi=150)
    print(f"Saved {out_path}")
    plt.close()

def scatter_ports_vs_ev(panel):
    plt.figure(figsize=(7, 5))
    sns.scatterplot(
        data=panel,
        x="ports_per_100k",
        y="ev_per_1000",
        hue="year"
    )
    plt.xlabel("Public charging ports per 100,000 people")
    plt.ylabel("EVs per 1,000 people")
    plt.title("EV Adoption vs. Charging Ports (by state-year)")
    plt.tight_layout()
    out_path = PROCESSED_DIR / "ports_vs_ev_scatter.png"
    plt.savefig(out_path, dpi=150)
    print(f"Saved {out_path}")
    plt.close()

def main():
    panel = pd.read_csv(PANEL_FILE)
    lineplot_top_states_ev(panel, top_n=5)
    scatter_ports_vs_ev(panel)

if __name__ == "__main__":
    main()
