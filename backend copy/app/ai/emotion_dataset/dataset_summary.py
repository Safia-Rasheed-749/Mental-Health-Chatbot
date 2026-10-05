import pandas as pd

train = pd.read_csv("datasets/emotion_dataset/processed/train_processed.csv")
val = pd.read_csv("datasets/emotion_dataset/processed/validation_processed.csv")
test = pd.read_csv("datasets/emotion_dataset/processed/test_processed.csv")

print("=" * 50)
print("Emotion Dataset Summary")
print("=" * 50)

print(f"Train Shape      : {train.shape}")
print(f"Validation Shape : {val.shape}")
print(f"Test Shape       : {test.shape}")

print()

print("Columns")
print(train.columns.tolist())

print()

print("Unique Labels")
print(sorted(train["label"].unique()))

print()

print("Total Classes")
print(train["label"].nunique())