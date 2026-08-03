import pandas as pd

# ===============================
# Load Raw Dataset
# ===============================

train = pd.read_csv("datasets/emotion_dataset/raw/train.csv")
val = pd.read_csv("datasets/emotion_dataset/raw/validation.csv")
test = pd.read_csv("datasets/emotion_dataset/raw/test.csv")


# ===============================
# Preprocessing Function
# ===============================

def clean(df):

    df = df.drop_duplicates()

    df = df.dropna()

    df["text"] = (
        df["text"]
        .str.lower()
        .str.strip()
    )

    return df


# ===============================
# Clean Dataset
# ===============================

train = clean(train)
val = clean(val)
test = clean(test)


# ===============================
# Save Processed Files
# ===============================

train.to_csv(
    "datasets/emotion_dataset/processed/train_processed.csv",
    index=False
)

val.to_csv(
    "datasets/emotion_dataset/processed/validation_processed.csv",
    index=False
)

test.to_csv(
    "datasets/emotion_dataset/processed/test_processed.csv",
    index=False
)


# ===============================
# Summary
# ===============================

print("=" * 50)
print("Emotion Dataset Preprocessing Completed")
print("=" * 50)

print("\nFiles Saved:")
print("train_processed.csv")
print("validation_processed.csv")
print("test_processed.csv")

print("\nTrain Shape:", train.shape)
print("Validation Shape:", val.shape)
print("Test Shape:", test.shape)

print("\nSample Processed Data:")
print(train.head())

print("\nMissing Values")
print(train.isnull().sum())

print("=" * 50)