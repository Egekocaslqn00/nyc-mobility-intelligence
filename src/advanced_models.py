"""
NYC Urban Mobility Intelligence Platform
Advanced ML Models - Trip Duration Prediction
"""

import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import json
import gc

DATA_DIR = "/home/ubuntu/nyc_mobility_intelligence/data"
OUTPUT_DIR = "/home/ubuntu/nyc_mobility_intelligence/visualizations"
MODEL_DIR = "/home/ubuntu/nyc_mobility_intelligence/models"

print("=" * 60)
print("Advanced ML Models - Trip Duration Prediction")
print("=" * 60)

# Load data
print("\n[1/4] Veri yükleniyor...")
yellow_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count',
               'trip_distance', 'PULocationID', 'DOLocationID', 'fare_amount']

yellow_df = pq.read_table(f"{DATA_DIR}/yellow_2024_01.parquet", columns=yellow_cols).to_pandas()
yellow_df = yellow_df.sample(n=min(300000, len(yellow_df)), random_state=42)

# Clean and prepare
print("\n[2/4] Veri hazırlanıyor...")
yellow_df['pickup_datetime'] = pd.to_datetime(yellow_df['tpep_pickup_datetime'])
yellow_df['dropoff_datetime'] = pd.to_datetime(yellow_df['tpep_dropoff_datetime'])
yellow_df['trip_duration'] = (yellow_df['dropoff_datetime'] - yellow_df['pickup_datetime']).dt.total_seconds() / 60

# Filter
yellow_df = yellow_df[(yellow_df['trip_duration'] > 1) & (yellow_df['trip_duration'] < 120)]
yellow_df = yellow_df[(yellow_df['trip_distance'] > 0) & (yellow_df['trip_distance'] < 50)]
yellow_df = yellow_df[(yellow_df['fare_amount'] > 0) & (yellow_df['fare_amount'] < 200)]

# Features
yellow_df['hour'] = yellow_df['pickup_datetime'].dt.hour
yellow_df['day_of_week'] = yellow_df['pickup_datetime'].dt.dayofweek
yellow_df['is_weekend'] = yellow_df['day_of_week'].isin([5, 6]).astype(int)
yellow_df['is_rush_hour'] = yellow_df['hour'].isin([7, 8, 9, 17, 18, 19]).astype(int)

print(f"  Hazırlanan veri: {len(yellow_df):,} kayıt")

# =============================================================================
# TRIP DURATION PREDICTION MODEL
# =============================================================================
print("\n[3/4] Süre tahmin modeli eğitiliyor...")

duration_features = ['trip_distance', 'hour', 'day_of_week', 'is_weekend', 
                     'is_rush_hour', 'PULocationID', 'DOLocationID']

X = yellow_df[duration_features].dropna()
y = yellow_df.loc[X.index, 'trip_duration']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost model
duration_model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=8,
    learning_rate=0.1,
    random_state=42,
    n_jobs=-1
)
duration_model.fit(X_train, y_train)

# Evaluate
y_pred = duration_model.predict(X_test)
duration_mae = mean_absolute_error(y_test, y_pred)
duration_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
duration_r2 = r2_score(y_test, y_pred)

print(f"  MAE: {duration_mae:.2f} dakika")
print(f"  RMSE: {duration_rmse:.2f} dakika")
print(f"  R²: {duration_r2:.3f}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': duration_features,
    'importance': duration_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n  Feature Importance:")
for _, row in feature_importance.iterrows():
    print(f"    {row['feature']}: {row['importance']:.3f}")

# Save model
joblib.dump(duration_model, f"{MODEL_DIR}/duration_prediction_model.joblib")

# =============================================================================
# SAVE RESULTS
# =============================================================================
print("\n[4/4] Sonuçlar kaydediliyor...")

# Load existing results
with open(f"{OUTPUT_DIR}/analysis_results.json", 'r') as f:
    results = json.load(f)

# Add duration model results
results['ml_results']['duration_prediction'] = {
    'mae_minutes': round(duration_mae, 2),
    'rmse_minutes': round(duration_rmse, 2),
    'r2_score': round(duration_r2, 3),
    'feature_importance': feature_importance.to_dict('records')
}

# Add congestion analysis
congestion_by_hour = yellow_df.groupby('hour').agg({
    'trip_duration': 'mean',
    'trip_distance': 'mean'
}).round(2)
congestion_by_hour['avg_speed_mph'] = (congestion_by_hour['trip_distance'] / 
                                        (congestion_by_hour['trip_duration'] / 60)).round(2)
congestion_by_hour = congestion_by_hour.reset_index()

results['congestion_analysis'] = {
    'hourly_speed': congestion_by_hour.to_dict('records'),
    'rush_hour_avg_speed': round(yellow_df[yellow_df['is_rush_hour'] == 1].apply(
        lambda x: x['trip_distance'] / (x['trip_duration'] / 60), axis=1).mean(), 2),
    'off_peak_avg_speed': round(yellow_df[yellow_df['is_rush_hour'] == 0].apply(
        lambda x: x['trip_distance'] / (x['trip_duration'] / 60), axis=1).mean(), 2)
}

# Save updated results
with open(f"{OUTPUT_DIR}/analysis_results.json", 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\n" + "=" * 60)
print("✅ Süre tahmin modeli tamamlandı!")
print(f"📁 Model: {MODEL_DIR}/duration_prediction_model.joblib")
print("=" * 60)
