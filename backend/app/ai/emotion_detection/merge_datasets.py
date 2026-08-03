import pandas as pd
import os

# -----------------------------
# Load GoEmotions Processed Data
# -----------------------------

goemotion = pd.read_csv(
    "datasets/processed/clean_train.csv"
)

# -----------------------------
# Load Emotion Dataset
# -----------------------------

emotion = pd.read_csv(
    "datasets/emotion_dataset/processed/train_processed.csv"
)

# -----------------------------
# Label Mapping
# -----------------------------

mapping = {

    0:25,      # sadness

    1:17,      # joy

    2:18,      # love

    3:2,       # anger

    4:14,      # fear

    5:26       # surprise

}

emotion["label"] = emotion["label"].map(mapping)

# -----------------------------
# Merge datasets
# -----------------------------

merged = pd.concat(
    [goemotion, emotion],
    ignore_index=True
)

# -----------------------------
# Shuffle
# -----------------------------

merged = merged.sample(
    frac=1,
    random_state=42
)

merged.reset_index(
    drop=True,
    inplace=True
)

# -----------------------------
# Save
# -----------------------------

os.makedirs(
    "datasets/final_emotion",
    exist_ok=True
)

merged.to_csv(
    "datasets/final_emotion/merged_train.csv",
    index=False
)

print("="*50)
print("Datasets Merged Successfully")
print("="*50)

print()

print("GoEmotions Samples :", len(goemotion))
print("Emotion Samples    :", len(emotion))
print("Merged Samples     :", len(merged))

print()

print("Unique Labels")

print(sorted(merged["label"].unique()))

print()

print("Saved At")

print("datasets/final_emotion/merged_train.csv")