import pandas as pd
from src.config import RAW_DIR, POP_CLEAN_FILE  

# Raw files in Datasets/
OLD_FILE = RAW_DIR / "nst-est2020-alldata.csv"      # 2010–2020
NEW_FILE = RAW_DIR / "population_estimate.csv"      # 2020–2024

def tidy_old():
    df = pd.read_csv(OLD_FILE)

    # state-level only
    df = df[df["SUMLEV"] == 40].copy()

    # keep FIPS + state name + 2016–2019
    cols = [
        "STATE",
        "NAME",
        "POPESTIMATE2016",
        "POPESTIMATE2017",
        "POPESTIMATE2018",
        "POPESTIMATE2019",
    ]
    df = df[cols]

    # wide → long
    long = df.melt(
        id_vars=["STATE", "NAME"],
        value_vars=[
            "POPESTIMATE2016",
            "POPESTIMATE2017",
            "POPESTIMATE2018",
            "POPESTIMATE2019",
        ],
        var_name="estimate",
        value_name="population",
    )

    long["year"] = long["estimate"].str[-4:].astype(int)
    long = long.drop(columns="estimate")
    return long


def tidy_new():
    df = pd.read_csv(NEW_FILE)

    # state-level only
    df = df[df["SUMLEV"] == 40].copy()

    cols = [
        "STATE",
        "NAME",
        "POPESTIMATE2020",
        "POPESTIMATE2021",
        "POPESTIMATE2022",
        "POPESTIMATE2023",
    ]
    df = df[cols]

    long = df.melt(
        id_vars=["STATE", "NAME"],
        value_vars=[
            "POPESTIMATE2020",
            "POPESTIMATE2021",
            "POPESTIMATE2022",
            "POPESTIMATE2023",
        ],
        var_name="estimate",
        value_name="population",
    )

    long["year"] = long["estimate"].str[-4:].astype(int)
    long = long.drop(columns="estimate")
    return long


def build_population_states():
    old_long = tidy_old()
    new_long = tidy_new()

    combined = (
        pd.concat([old_long, new_long], ignore_index=True)
        .query("2016 <= year <= 2023")
        .rename(columns={"NAME": "state", "STATE": "state_fips"})
        .sort_values(["state_fips", "year"])
    )

    POP_CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(POP_CLEAN_FILE, index=False)
    print(f"Saved {POP_CLEAN_FILE}")


if __name__ == "__main__":
    build_population_states()
