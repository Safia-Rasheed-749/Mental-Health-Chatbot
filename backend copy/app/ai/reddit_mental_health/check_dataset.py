"""
=========================================================
Check Reddit Mental Health Dataset
=========================================================
"""

import pandas as pd

df = pd.read_csv(
    "datasets/reddit_mental_health/raw/train.csv"
)

print("=" * 60)
print("Reddit Mental Health Dataset")
print("=" * 60)

print("\nFirst 5 Rows\n")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nSubreddit Distribution")
print(df["subreddit"].value_counts())

print("\nSample Post Title")
print(df["title"].iloc[0])

print("\nSample Post")
print(df["body"].iloc[0])