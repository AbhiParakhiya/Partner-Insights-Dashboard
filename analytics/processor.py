import pandas as pd
import numpy as np
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed")

# Ensure directories exist
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

def process_partner_data():
    csv_file = os.path.join(RAW_DATA_PATH, "partner_performance.csv")
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Source data not found: {csv_file}")
    
    df = pd.read_csv(csv_file)
    
    # 1. Cleaning
    df = df.dropna()
    df['last_active'] = pd.to_datetime(df['last_active'])
    
    # 2. Feature Engineering & KPIs
    # Revenue per deal
    df["avg_deal_value"] = (df["revenue"] / df["deals"]).round(2)
    
    # Engagement Score (Synthetic formula: freq * 10 + potential * 100)
    df["engagement_score"] = (df["engagement_frequency"] * 10 + df["growth_potential"] * 100).round(2)
    
    revenue_median = df['revenue'].median()
    df['partner_tier'] = np.where(df['revenue'] > revenue_median, 'Gold', 'Silver')
    
    # 3. Export Processed Data
    processed_file = os.path.join(PROCESSED_DATA_PATH, "partner_insights.csv")
    df.to_csv(processed_file, index=False)
    print(f"Processed data saved to: {processed_file}")
    return df

if __name__ == "__main__":
    process_partner_data()
