import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

# Load the combined NAV file
df = pd.read_csv("data/raw/nav_history_all.csv")

print("=== RAW DATA ===")
print(df.shape)
print(df.dtypes)
print(df.head())

# Clean date column
df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")

# Clean NAV column — it comes as string from API
df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

# Drop rows where NAV or date is invalid
df = df.dropna(subset=["date", "nav"])

# Remove NAV <= 0 (invalid)
df = df[df["nav"] > 0]

# Remove duplicates
df = df.drop_duplicates(subset=["amfi_code", "date"])

# Sort
df = df.sort_values(["amfi_code", "date"]).reset_index(drop=True)

# Filter to 2022 onwards (matching your task scope)
df = df[df["date"] >= "2022-01-01"]

print("\n=== CLEANED DATA ===")
print(df.shape)
print(df.head())

# Save
df.to_csv("data/processed/nav_history_clean.csv", index=False)
print("\nSaved: data/processed/nav_history_clean.csv")