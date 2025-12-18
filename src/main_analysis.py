"""
NYC Urban Mobility Intelligence Platform
=========================================
Kapsamlı NYC Taksi ve Rideshare Veri Analizi & Tahmin Sistemi
(Bellek Optimizasyonlu Versiyon)
"""

import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import joblib
import json
import os
import gc

# Paths
DATA_DIR = "/home/ubuntu/nyc_mobility_intelligence/data"
OUTPUT_DIR = "/home/ubuntu/nyc_mobility_intelligence/visualizations"
MODEL_DIR = "/home/ubuntu/nyc_mobility_intelligence/models"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

print("=" * 60)
print("NYC Urban Mobility Intelligence Platform")
print("=" * 60)

# =============================================================================
# 1. DATA LOADING (Optimized - Only needed columns)
# =============================================================================
print("\n[1/8] Veriler yükleniyor (optimize edilmiş)...")

# Yellow Taxi - sadece gerekli sütunlar
yellow_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count',
               'trip_distance', 'PULocationID', 'DOLocationID', 'fare_amount', 
               'tip_amount', 'tolls_amount', 'payment_type']

yellow_jan = pq.read_table(f"{DATA_DIR}/yellow_2024_01.parquet", columns=yellow_cols).to_pandas()
print(f"  Ocak verisi yüklendi: {len(yellow_jan):,} kayıt")

# Sample for memory efficiency
yellow_df = yellow_jan.sample(n=min(500000, len(yellow_jan)), random_state=42)
del yellow_jan
gc.collect()

# FHV - sadece gerekli sütunlar ve sample
fhv_cols = ['hvfhs_license_num', 'pickup_datetime', 'dropoff_datetime', 
            'PULocationID', 'DOLocationID', 'trip_miles', 'trip_time']

fhvhv_full = pq.read_table(f"{DATA_DIR}/fhvhv_2024_01.parquet", columns=fhv_cols).to_pandas()
fhvhv_df = fhvhv_full.sample(n=min(500000, len(fhvhv_full)), random_state=42)
fhv_total_count = len(fhvhv_full)
del fhvhv_full
gc.collect()

# Taxi Zone Lookup
zones_df = pd.read_csv(f"{DATA_DIR}/taxi_zone_lookup.csv")

print(f"  Yellow Taxi sample: {len(yellow_df):,}")
print(f"  FHV sample: {len(fhvhv_df):,}")

# =============================================================================
# 2. DATA CLEANING & FEATURE ENGINEERING
# =============================================================================
print("\n[2/8] Veri temizleme ve özellik mühendisliği...")

def clean_yellow_taxi(df):
    df = df.copy()
    df = df[(df['fare_amount'] > 0) & (df['fare_amount'] < 500)]
    df = df[(df['trip_distance'] > 0) & (df['trip_distance'] < 100)]
    df = df[(df['passenger_count'] > 0) & (df['passenger_count'] <= 6)]
    df = df[df['tip_amount'] >= 0]
    
    df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['day_name'] = df['pickup_datetime'].dt.day_name()
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    df['is_rush_hour'] = df['hour'].isin([7, 8, 9, 17, 18, 19]).astype(int)
    df['is_night'] = df['hour'].isin([22, 23, 0, 1, 2, 3, 4]).astype(int)
    
    df['trip_duration'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds() / 60
    df = df[(df['trip_duration'] > 1) & (df['trip_duration'] < 180)]
    
    df['avg_speed'] = df['trip_distance'] / (df['trip_duration'] / 60)
    df = df[(df['avg_speed'] > 0) & (df['avg_speed'] < 60)]
    
    df['tip_percentage'] = (df['tip_amount'] / df['fare_amount'] * 100).clip(0, 100)
    df['total_fare'] = df['fare_amount'] + df['tip_amount'] + df['tolls_amount']
    
    return df

def clean_fhvhv(df):
    df = df.copy()
    df = df[df['trip_miles'] > 0]
    df = df[df['trip_time'] > 0]
    
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['day_name'] = df['pickup_datetime'].dt.day_name()
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    df['is_rush_hour'] = df['hour'].isin([7, 8, 9, 17, 18, 19]).astype(int)
    df['is_night'] = df['hour'].isin([22, 23, 0, 1, 2, 3, 4]).astype(int)
    
    df['company'] = df['hvfhs_license_num'].map({
        'HV0003': 'Uber', 'HV0005': 'Lyft', 'HV0004': 'Via', 'HV0002': 'Juno'
    }).fillna('Other')
    
    return df

yellow_clean = clean_yellow_taxi(yellow_df)
fhvhv_clean = clean_fhvhv(fhvhv_df)

del yellow_df, fhvhv_df
gc.collect()

print(f"  Temizlenmiş Yellow Taxi: {len(yellow_clean):,}")
print(f"  Temizlenmiş FHV: {len(fhvhv_clean):,}")

# Zone bilgilerini ekle
yellow_clean = yellow_clean.merge(
    zones_df[['LocationID', 'Borough', 'Zone']], 
    left_on='PULocationID', right_on='LocationID', how='left'
).rename(columns={'Borough': 'PU_Borough', 'Zone': 'PU_Zone'})

fhvhv_clean = fhvhv_clean.merge(
    zones_df[['LocationID', 'Borough', 'Zone']], 
    left_on='PULocationID', right_on='LocationID', how='left'
).rename(columns={'Borough': 'PU_Borough', 'Zone': 'PU_Zone'})

# =============================================================================
# 3. ANALYSIS
# =============================================================================
print("\n[3/8] Keşifsel Veri Analizi (EDA)...")

results = {
    'summary_stats': {},
    'hourly_demand': {},
    'daily_demand': {},
    'borough_analysis': {},
    'market_share': {},
    'profitable_locations': {},
    'tip_analysis': {},
    'airport_analysis': {},
    'nightlife_analysis': {},
    'ml_results': {}
}

# Özet istatistikler
results['summary_stats'] = {
    'yellow_taxi': {
        'total_trips': int(len(yellow_clean)),
        'avg_fare': round(float(yellow_clean['fare_amount'].mean()), 2),
        'avg_distance': round(float(yellow_clean['trip_distance'].mean()), 2),
        'avg_duration': round(float(yellow_clean['trip_duration'].mean()), 2),
        'avg_tip_pct': round(float(yellow_clean['tip_percentage'].mean()), 2),
        'total_revenue': round(float(yellow_clean['total_fare'].sum()), 2)
    },
    'fhv': {
        'total_trips': int(len(fhvhv_clean)),
        'uber_trips': int((fhvhv_clean['company'] == 'Uber').sum()),
        'lyft_trips': int((fhvhv_clean['company'] == 'Lyft').sum()),
        'avg_distance': round(float(fhvhv_clean['trip_miles'].mean()), 2),
        'avg_duration': round(float(fhvhv_clean['trip_time'].mean() / 60), 2)
    }
}

# Saatlik talep
hourly_yellow = yellow_clean.groupby('hour').size().reset_index(name='trips')
hourly_fhv = fhvhv_clean.groupby('hour').size().reset_index(name='trips')

results['hourly_demand'] = {
    'yellow_taxi': hourly_yellow.to_dict('records'),
    'fhv': hourly_fhv.to_dict('records')
}

# Günlük talep
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_yellow = yellow_clean.groupby('day_name').size()
daily_yellow = daily_yellow.reindex(day_order).reset_index(name='trips')
daily_fhv = fhvhv_clean.groupby('day_name').size()
daily_fhv = daily_fhv.reindex(day_order).reset_index(name='trips')

results['daily_demand'] = {
    'yellow_taxi': daily_yellow.to_dict('records'),
    'fhv': daily_fhv.to_dict('records')
}

# Borough analizi
borough_yellow = yellow_clean.groupby('PU_Borough').agg({
    'fare_amount': ['count', 'mean', 'sum'],
    'tip_percentage': 'mean',
    'trip_distance': 'mean'
}).round(2)
borough_yellow.columns = ['trips', 'avg_fare', 'total_revenue', 'avg_tip_pct', 'avg_distance']
borough_yellow = borough_yellow.reset_index()

borough_fhv = fhvhv_clean.groupby('PU_Borough').size().reset_index(name='trips')

results['borough_analysis'] = {
    'yellow_taxi': borough_yellow.to_dict('records'),
    'fhv': borough_fhv.to_dict('records')
}

# =============================================================================
# 4. MARKET SHARE
# =============================================================================
print("\n[4/8] Pazar payı analizi...")

hourly_market = pd.DataFrame({
    'hour': range(24),
    'yellow_taxi': hourly_yellow['trips'].values,
    'fhv': hourly_fhv['trips'].values
})
hourly_market['yellow_pct'] = (hourly_market['yellow_taxi'] / 
    (hourly_market['yellow_taxi'] + hourly_market['fhv']) * 100).round(1)
hourly_market['fhv_pct'] = (hourly_market['fhv'] / 
    (hourly_market['yellow_taxi'] + hourly_market['fhv']) * 100).round(1)

total_yellow = len(yellow_clean)
total_fhv = len(fhvhv_clean)

results['market_share'] = {
    'hourly': hourly_market.to_dict('records'),
    'overall': {
        'yellow_taxi_pct': round(total_yellow / (total_yellow + total_fhv) * 100, 1),
        'fhv_pct': round(total_fhv / (total_yellow + total_fhv) * 100, 1)
    },
    'uber_vs_lyft': {
        'uber_pct': round((fhvhv_clean['company'] == 'Uber').mean() * 100, 1),
        'lyft_pct': round((fhvhv_clean['company'] == 'Lyft').mean() * 100, 1)
    }
}

# =============================================================================
# 5. PROFITABLE LOCATIONS
# =============================================================================
print("\n[5/8] Karlı lokasyonlar analizi...")

profitable_zones = yellow_clean.groupby(['PU_Borough', 'PU_Zone']).agg({
    'total_fare': ['mean', 'sum', 'count'],
    'tip_percentage': 'mean',
    'trip_distance': 'mean'
}).round(2)
profitable_zones.columns = ['avg_fare', 'total_revenue', 'trip_count', 'avg_tip_pct', 'avg_distance']
profitable_zones = profitable_zones.reset_index()
profitable_zones = profitable_zones[profitable_zones['trip_count'] >= 50]
profitable_zones = profitable_zones.sort_values('avg_fare', ascending=False)

profitable_hours = yellow_clean.groupby('hour').agg({
    'total_fare': 'mean',
    'tip_percentage': 'mean'
}).round(2).reset_index()

results['profitable_locations'] = {
    'top_zones': profitable_zones.head(20).to_dict('records'),
    'profitable_hours': profitable_hours.to_dict('records')
}

# =============================================================================
# 6. TIP PREDICTION MODEL
# =============================================================================
print("\n[6/8] Bahşiş tahmin modeli...")

tip_features = ['trip_distance', 'fare_amount', 'hour', 'day_of_week', 
                'is_weekend', 'is_rush_hour', 'is_night', 'passenger_count']

tip_df = yellow_clean[tip_features + ['tip_percentage']].dropna()
tip_df = tip_df[tip_df['tip_percentage'] > 0]
tip_sample = tip_df.sample(n=min(50000, len(tip_df)), random_state=42)

X_tip = tip_sample[tip_features]
y_tip = tip_sample['tip_percentage']

X_train, X_test, y_train, y_test = train_test_split(X_tip, y_tip, test_size=0.2, random_state=42)

tip_model = xgb.XGBRegressor(n_estimators=50, max_depth=5, learning_rate=0.1, random_state=42, n_jobs=-1)
tip_model.fit(X_train, y_train)

tip_pred = tip_model.predict(X_test)
tip_mae = mean_absolute_error(y_test, tip_pred)
tip_r2 = r2_score(y_test, tip_pred)

tip_importance = pd.DataFrame({
    'feature': tip_features,
    'importance': tip_model.feature_importances_
}).sort_values('importance', ascending=False)

results['tip_analysis'] = {
    'model_performance': {'mae': round(tip_mae, 2), 'r2_score': round(tip_r2, 3)},
    'feature_importance': tip_importance.to_dict('records'),
    'avg_tip_by_hour': {int(k): round(v, 2) for k, v in yellow_clean.groupby('hour')['tip_percentage'].mean().to_dict().items()},
    'avg_tip_by_day': {k: round(v, 2) for k, v in yellow_clean.groupby('day_name')['tip_percentage'].mean().to_dict().items()}
}

joblib.dump(tip_model, f"{MODEL_DIR}/tip_prediction_model.joblib")
print(f"  Bahşiş modeli - MAE: {tip_mae:.2f}%, R²: {tip_r2:.3f}")

# =============================================================================
# 7. DEMAND PREDICTION
# =============================================================================
print("\n[7/8] Talep tahmin modeli...")

demand_df = yellow_clean.groupby([
    yellow_clean['pickup_datetime'].dt.date, 'hour'
]).agg({'fare_amount': 'count', 'is_weekend': 'first', 'is_rush_hour': 'first'}).reset_index()
demand_df.columns = ['date', 'hour', 'trip_count', 'is_weekend', 'is_rush_hour']
demand_df['day_of_week'] = pd.to_datetime(demand_df['date']).dt.dayofweek

demand_features = ['hour', 'day_of_week', 'is_weekend', 'is_rush_hour']
X_d = demand_df[demand_features]
y_d = demand_df['trip_count']

X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_d, y_d, test_size=0.2, random_state=42)

demand_model = RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42, n_jobs=-1)
demand_model.fit(X_train_d, y_train_d)

demand_pred = demand_model.predict(X_test_d)
demand_mae = mean_absolute_error(y_test_d, demand_pred)
demand_r2 = r2_score(y_test_d, demand_pred)

results['ml_results']['demand_prediction'] = {
    'mae': round(demand_mae, 0),
    'r2_score': round(demand_r2, 3),
    'feature_importance': {f: round(v, 3) for f, v in zip(demand_features, demand_model.feature_importances_)}
}

joblib.dump(demand_model, f"{MODEL_DIR}/demand_prediction_model.joblib")
print(f"  Talep modeli - MAE: {demand_mae:.0f}, R²: {demand_r2:.3f}")

# =============================================================================
# 8. SPECIAL SEGMENTS
# =============================================================================
print("\n[8/8] Özel segment analizleri...")

# Havalimanı
airport_zones = [1, 132, 138]
airport_trips = yellow_clean[
    (yellow_clean['PULocationID'].isin(airport_zones)) | 
    (yellow_clean['DOLocationID'].isin(airport_zones))
]

airport_hourly = airport_trips.groupby('hour').agg({
    'fare_amount': ['count', 'mean'], 'tip_percentage': 'mean'
}).round(2)
airport_hourly.columns = ['trip_count', 'avg_fare', 'avg_tip']
airport_hourly = airport_hourly.reset_index()

results['airport_analysis'] = {
    'total_trips': int(len(airport_trips)),
    'avg_fare': round(float(airport_trips['fare_amount'].mean()), 2),
    'avg_tip_pct': round(float(airport_trips['tip_percentage'].mean()), 2),
    'hourly_demand': airport_hourly.to_dict('records'),
    'pct_of_total': round(len(airport_trips) / len(yellow_clean) * 100, 2)
}

# Gece hayatı
nightlife_trips = yellow_clean[yellow_clean['is_night'] == 1]
nightlife_zones = nightlife_trips.groupby(['PU_Borough', 'PU_Zone']).size().reset_index(name='trips')
nightlife_zones = nightlife_zones.sort_values('trips', ascending=False)

weekend_night = nightlife_trips[nightlife_trips['is_weekend'] == 1]
weekday_night = nightlife_trips[nightlife_trips['is_weekend'] == 0]

results['nightlife_analysis'] = {
    'total_night_trips': int(len(nightlife_trips)),
    'pct_of_total': round(len(nightlife_trips) / len(yellow_clean) * 100, 2),
    'top_nightlife_zones': nightlife_zones.head(15).to_dict('records'),
    'weekend_vs_weekday': {
        'weekend_trips': int(len(weekend_night)),
        'weekday_trips': int(len(weekday_night)),
        'weekend_avg_fare': round(float(weekend_night['fare_amount'].mean()), 2) if len(weekend_night) > 0 else 0,
        'weekday_avg_fare': round(float(weekday_night['fare_amount'].mean()), 2) if len(weekday_night) > 0 else 0
    },
    'hourly_distribution': {int(k): int(v) for k, v in nightlife_trips.groupby('hour').size().to_dict().items()}
}

# =============================================================================
# SAVE
# =============================================================================
print("\n" + "=" * 60)
print("Sonuçlar kaydediliyor...")

with open(f"{OUTPUT_DIR}/analysis_results.json", 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n✅ Analiz tamamlandı!")
print(f"📁 Sonuçlar: {OUTPUT_DIR}/analysis_results.json")
print(f"🤖 Modeller: {MODEL_DIR}/")
print("=" * 60)

print("\n📊 ÖZET RAPOR")
print("-" * 40)
print(f"Yellow Taxi yolculuğu: {results['summary_stats']['yellow_taxi']['total_trips']:,}")
print(f"FHV yolculuğu: {results['summary_stats']['fhv']['total_trips']:,}")
print(f"Ortalama ücret: ${results['summary_stats']['yellow_taxi']['avg_fare']}")
print(f"Ortalama bahşiş: %{results['summary_stats']['yellow_taxi']['avg_tip_pct']}")
print(f"\nPazar Payı: Yellow %{results['market_share']['overall']['yellow_taxi_pct']} vs FHV %{results['market_share']['overall']['fhv_pct']}")
print(f"Uber vs Lyft: %{results['market_share']['uber_vs_lyft']['uber_pct']} vs %{results['market_share']['uber_vs_lyft']['lyft_pct']}")
print(f"\nML Performans:")
print(f"  Bahşiş: MAE={tip_mae:.2f}%, R²={tip_r2:.3f}")
print(f"  Talep: MAE={demand_mae:.0f}, R²={demand_r2:.3f}")
