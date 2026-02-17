import pandas as pd

# Exact path to data
DATA_DIR = "/Users/bass/LaurenOh/FearConditioning/data/FC"

# Load files
day0 = pd.read_csv(f"{DATA_DIR}/FC_Day0_combined_metadata.csv")
day1 = pd.read_csv(f"{DATA_DIR}/FC_Day1_combined_metadata.csv")
day2 = pd.read_csv(f"{DATA_DIR}/FC_Day2_combined_metadata.csv")

# Verify columns
print("Day0 columns:", day0.columns.tolist())
print("Day1 columns:", day1.columns.tolist())
print("Day2 columns:", day2.columns.tolist())

# ==============================
# DAY 0 — Acquisition (unchanged)
# ==============================
day0_df = (
    day0
    .groupby("Animal ID")
    .apply(
        lambda g: pd.Series({
            "Day0_Slope": (
                g["Pct Total Time Freezing"].iloc[-1]
                - g["Pct Total Time Freezing"].iloc[0]
            )
        })
    )
    .reset_index()
)

# ==============================
# DAY 1 — Context Memory (unchanged)
# ==============================
day1_df = (
    day1.groupby("Animal ID", as_index=False)
         .agg(Day1_Context=("Pct Total Time Freezing", "mean"))
)

# ==============================
# DAY 2 — Cued Memory (UPDATED)
# ==============================

# Identify baseline vs tone rows
# (Adjust these strings if needed after printing unique values)
print("Unique Day2 Component Names:")
print(day2["Component Name"].unique())

# Baseline rows (acclimation)
baseline = day2[
    day2["Component Name"].str.contains("acclim|baseline", case=False, na=False)
]

# Tone rows (CS)
tone = day2[
    day2["Component Name"].str.contains("tone|cs", case=False, na=False)
]

baseline_df = (
    baseline.groupby("Animal ID", as_index=False)
            .agg(Day2_Baseline=("Pct Total Time Freezing", "mean"))
)

tone_df = (
    tone.groupby("Animal ID", as_index=False)
        .agg(Day2_Tone=("Pct Total Time Freezing", "mean"))
)

day2_df = (
    tone_df
    .merge(baseline_df, on="Animal ID", how="inner")
)

day2_df["Day2_Cued"] = day2_df["Day2_Tone"] - day2_df["Day2_Baseline"]

day2_df = day2_df[["Animal ID", "Day2_Cued"]]

# ==============================
# Merge All
# ==============================

behavior = (
    day0_df
    .merge(day1_df, on="Animal ID")
    .merge(day2_df, on="Animal ID")
)

# Save
out = f"{DATA_DIR}/FC_standardized_behavior.csv"
behavior.to_csv(out, index=False)

print("Saved:", out)
print("Rows:", behavior.shape[0])
print("Columns:", behavior.columns.tolist())
