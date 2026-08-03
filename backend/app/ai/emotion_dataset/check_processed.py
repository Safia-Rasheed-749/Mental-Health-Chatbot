import pandas as pd

train = pd.read_csv(
    "datasets/emotion_dataset/processed/train_processed.csv"
)

print("=" * 60)
print("Processed Emotion Dataset")
print("=" * 60)

print("\nFirst 10 Rows")
print(train.head(10))

print("\nColumns")
print(train.columns.tolist())

print("\nUnique Emotions")
print(sorted(train["emotion"].unique()))

print("\nEmotion Distribution")
print(train["emotion"].value_counts())

print("\nMissing Values")
print(train.isnull().sum())