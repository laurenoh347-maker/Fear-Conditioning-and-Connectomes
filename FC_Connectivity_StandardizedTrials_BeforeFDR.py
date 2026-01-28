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

# Use Animal ID directly
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

day1_df = (
    day1.groupby("Animal ID", as_index=False)
         .agg(Day1_Freezing=("Pct Total Time Freezing", "mean"))
)

day2_df = (
    day2.groupby("Animal ID", as_index=False)
         .agg(Day2_Freezing=("Pct Total Time Freezing", "mean"))
)

# Merge
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
