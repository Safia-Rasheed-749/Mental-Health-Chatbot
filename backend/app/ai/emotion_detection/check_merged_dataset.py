import pandas as pd

df = pd.read_csv(
    "datasets/final_emotion/merged_train.csv"
)

print("=" * 60)
print("Merged Emotion Dataset")
print("=" * 60)

print("\nShape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nFirst 10 Rows")
print(df.head(10))

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nUnique Labels")
print(sorted(df["label"].unique()))

print("\nLabel Distribution")
print(df["label"].value_counts().sort_index())

print("=" * 60)