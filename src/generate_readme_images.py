"""
Generate Static Images for README
"""
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

OUTPUT_DIR = "/home/ubuntu/nyc_mobility_intelligence/visualizations"
IMG_DIR = "/home/ubuntu/nyc_mobility_intelligence/visualizations/images"
os.makedirs(IMG_DIR, exist_ok=True)

# Load results
with open(f"{OUTPUT_DIR}/analysis_results.json", 'r') as f:
    results = json.load(f)

# 1. Hourly Demand Comparison
hourly_yellow = pd.DataFrame(results['hourly_demand']['yellow_taxi'])
hourly_fhv = pd.DataFrame(results['hourly_demand']['fhv'])

plt.figure(figsize=(12, 6))
plt.plot(hourly_yellow['hour'], hourly_yellow['trips'], label='Yellow Taxi', marker='o', linewidth=2, color='#F7B731')
plt.plot(hourly_fhv['hour'], hourly_fhv['trips'], label='Uber/Lyft (FHV)', marker='o', linewidth=2, color='#000000')
plt.title('Hourly Demand: Yellow Taxi vs Uber/Lyft', fontsize=16, pad=20)
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Number of Trips', fontsize=12)
plt.xticks(range(0, 24))
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"{IMG_DIR}/hourly_demand.png", dpi=300)
plt.close()

# 2. Market Share Pie Chart
market_share = results['market_share']['overall']
labels = ['Yellow Taxi', 'Uber/Lyft (FHV)']
sizes = [market_share['yellow_taxi_pct'], market_share['fhv_pct']]
colors = ['#F7B731', '#2d3436']

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, 
        textprops={'fontsize': 14, 'weight': 'bold', 'color': 'white'}, pctdistance=0.85)
# Draw circle
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('NYC Ride Market Share (2024)', fontsize=16)
plt.tight_layout()
plt.savefig(f"{IMG_DIR}/market_share.png", dpi=300)
plt.close()

# 3. Feature Importance (Tip Prediction)
fi_data = pd.DataFrame(results['tip_analysis']['feature_importance']).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=fi_data, palette='viridis')
plt.title('Top Factors Influencing Tipping Behavior', fontsize=16)
plt.xlabel('Importance Score')
plt.ylabel('Feature')
plt.tight_layout()
plt.savefig(f"{IMG_DIR}/feature_importance.png", dpi=300)
plt.close()

print("Images generated successfully!")
