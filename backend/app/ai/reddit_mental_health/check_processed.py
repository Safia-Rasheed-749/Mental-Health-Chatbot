import pandas as pd

df = pd.read_csv(
    "datasets/reddit_mental_health/processed/train_processed.csv"
)

print("=" * 60)
print("Processed Reddit Mental Health Dataset")
print("=" * 60)

print("\nFirst 5 Rows\n")
print(df.head())

print("\nShape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nMissing Values")
print(df.isnull().sum())

print("\nSubreddit Distribution")
print(df["subreddit"].value_counts())

print("\nSample Title\n")
print(df.iloc[0]["title"])

print("\nSample Body\n")
print(df.iloc[0]["body"])