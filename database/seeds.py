import pandas as pd
import numpy as np
import os
import random

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
DOCS_PATH = os.path.join(BASE_DIR, "docs", "partner_profiles")

# Ensure directories exist
os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(DOCS_PATH, exist_ok=True)

# 1. Generate Structured Data
def generate_structured_data(n=20):
    partners = [f"Partner_{i:03d}" for i in range(1, n+1)]
    industries = ["Financial Services", "Retail", "Healthcare", "Manufacturing", "Telecommunications"]
    regions = ["North America", "EMEA", "Asia Pacific", "Latin America"]
    
    data = []
    for p in partners:
        revenue = round(random.uniform(50000, 1000000), 2)
        deals = random.randint(5, 50)
        engagement_freq = random.randint(1, 10) # contacts per month
        industry = random.choice(industries)
        region = random.choice(regions)
        growth_potential = round(random.uniform(0.05, 0.30), 2)
        
        data.append({
            "partner_id": p,
            "industry": industry,
            "region": region,
            "revenue": revenue,
            "deals": deals,
            "engagement_frequency": engagement_freq,
            "growth_potential": growth_potential,
            "last_active": (pd.Timestamp.now() - pd.Timedelta(days=random.randint(0, 60))).strftime('%Y-%m-%d')
        })
    
    df = pd.DataFrame(data)
    csv_file = os.path.join(RAW_DATA_PATH, "partner_performance.csv")
    df.to_csv(csv_file, index=False)
    print(f"Generated structured data: {csv_file}")
    return df

# 2. Generate Unstructured Docs (Markdown)
def generate_unstructured_docs(df):
    for _, row in df.iterrows():
        p_id = row['partner_id']
        file_path = os.path.join(DOCS_PATH, f"{p_id}.md")
        
        content = f"""# Partner Profile: {p_id}
**Industry:** {row['industry']}
**Region:** {row['region']}

## Business Summary
{p_id} has been a key partner in the {row['industry']} sector within {row['region']}. Their focus is on digital transformation and AI adoption.

## Recent Feedback
- "Partner shows high interest in Partner Insights & GenAI integration."
- "Engagement frequency is {row['engagement_frequency']} times per month, which is {'adequate' if row['engagement_frequency'] > 5 else 'below average'}."
- "Revenue growth of {row['growth_potential']*100}% expected next fiscal year."

## Challenges
- Some integration delays reported in the last quarter.
- Requires more enablement on GenAI RAG workflows.

## Strategic Priority
{'High Growth' if row['growth_potential'] > 0.2 else 'Steady State'} - Focus on scaling {row['industry']} solutions.
"""
        with open(file_path, "w") as f:
            f.write(content)
    print(f"Generated {len(df)} partner profiles in: {DOCS_PATH}")

if __name__ == "__main__":
    df = generate_structured_data(25)
    generate_unstructured_docs(df)
