import os
import requests
import pandas as pd
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ASEAN_CODES = ['MY', 'SG', 'ID', 'TH', 'PH', 'VN', 'BN', 'MM', 'KH', 'LA']
API_BASE = "https://api.ransomware.live/v2/countryvictims/"

def fetch_asean_data():
    all_data = []
    for code in ASEAN_CODES:
        try:
            print(f"📡 Fetching {code}")
            response = requests.get(API_BASE + code)
            if response.status_code == 200:
                country_data = response.json()
                for entry in country_data:
                    entry['country_code'] = code
                all_data.extend(country_data)
            else:
                print(f"Failed to fetch {code}: {response.status_code}")
        except Exception as e:
            print(f" Error fetching {code}: {e}")
    return all_data

# clean rows before inserting it
def clean_data(data):
    df = pd.DataFrame(data)
    if df.empty:
        return df
    keep = [
        'post_title', 'activity', 'country', 'country_code', 'group_name',
        'description', 'website', 'post_url', 'published', 'discovered'
    ]
    df = df[keep]
    df['published'] = pd.to_datetime(df['published'], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%S')
    df['discovered'] = pd.to_datetime(df['discovered'], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%S')
    df = df.drop_duplicates(subset=["post_url"])
    return df

def upload_to_supabase(df):
    if df.empty:
        print("⚠️ No data to upload.")
        return
    records = df.to_dict(orient="records")
    for i in range(0, len(records), 50):
        chunk = records[i:i+50]
        supabase.table("asean_ransomware").upsert(chunk, on_conflict=["post_url"]).execute()
        print(f"✅ Uploaded {len(chunk)} records")

if __name__ == "__main__":
    print("Starting ransomware sync...")
    raw_data = fetch_asean_data()
    cleaned = clean_data(raw_data)
    upload_to_supabase(cleaned)
    print("Sync complete!")
