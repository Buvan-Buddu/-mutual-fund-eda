import requests
import pandas as pd
import os
import time

# Make sure folders exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# The 5 key schemes from your task
SCHEMES = {
    "HDFC_Top100":    125497,
    "SBI_Bluechip":   119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap":118632,
    "Axis_Bluechip":  119092,
    "Kotak_Bluechip": 120841,
}

all_nav_records = []

for scheme_name, amfi_code in SCHEMES.items():
    print(f"Fetching: {scheme_name} (code: {amfi_code})...")
    
    try:
        url = f"https://api.mfapi.in/mf/{amfi_code}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Get scheme info
        scheme_info = data["meta"]
        nav_data = data["data"]  # list of {date, nav}
        
        print(f"  Fund House : {scheme_info['fund_house']}")
        print(f"  Scheme Name: {scheme_info['scheme_name']}")
        print(f"  NAV records: {len(nav_data)}")
        
        # Build a DataFrame for this scheme
        df = pd.DataFrame(nav_data)
        df["amfi_code"]    = amfi_code
        df["scheme_name"]  = scheme_info["scheme_name"]
        df["fund_house"]   = scheme_info["fund_house"]
        df["scheme_label"] = scheme_name
        
        # Save individual scheme CSV
        df.to_csv(f"data/raw/{scheme_name}_nav.csv", index=False)
        
        all_nav_records.append(df)
        time.sleep(0.5)  # be polite to the API
        
    except Exception as e:
        print(f"  ERROR fetching {scheme_name}: {e}")

# Combine all schemes into one master CSV
master_df = pd.concat(all_nav_records, ignore_index=True)
master_df.to_csv("data/raw/nav_history_all.csv", index=False)

print(f"\nDone! Total records saved: {len(master_df)}")
print("File saved: data/raw/nav_history_all.csv")