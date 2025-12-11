import pandas as pd
from src.config import RAW_DIR  # RAW_DIR = PROJECT_ROOT / "Datasets" in your config

YEARS = [2016, 2017, 2018, 2019]

EXPECTED_COLS = [
    "State",
    "Electric (EV)",
    "Plug-In Hybrid Electric (PHEV)",
    "Hybrid Electric (HEV)",
    "Biodiesel",
    "Ethanol/Flex (E85)",
    "Compressed Natural Gas (CNG)",
    "Propane",
    "Hydrogen",
    "Methanol",
    "Gasoline",
    "Diesel",
    "Unknown Fuel",
]


def main():
    print(f"Saving CSVs to: {RAW_DIR}\n")

    for year in YEARS:
        url = f"https://afdc.energy.gov/vehicle-registration?year={year}"
        print(f"Downloading {year} from {url} ...")

        # read all HTML tables on the page
        tables = pd.read_html(url)

        # pick the one that has the EV column
        table = None
        for t in tables:
            if "Electric (EV)" in t.columns:
                table = t
                break

        if table is None:
            raise ValueError(f"Could not find registration table for {year}")

        # reorder & check columns
        missing = [c for c in EXPECTED_COLS if c not in table.columns]
        if missing:
            raise ValueError(f"{year}: missing columns {missing}")

        table = table[EXPECTED_COLS]

        out_path = RAW_DIR / f"ev_registrations_{year}.csv"
        table.to_csv(out_path, index=False)
        print(f"Saved {out_path}\n")


if __name__ == "__main__":
    main()
