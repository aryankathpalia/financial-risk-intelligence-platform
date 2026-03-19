import pandas as pd
from build_synthetic_features import build_synthetic_features


           
# LOAD DATASET
           
df = pd.read_csv("app/data/synthetic_dataset/synthetic_fraud_dataset.csv")

           
# BUILD FEATURES
           
X = build_synthetic_features(df)

           
# INSPECTION
           
print("\nHead:")
print(X.head())

print("\nNaN check:")
print(X.isna().sum())

print("\nDescribe:")
print(X.describe())