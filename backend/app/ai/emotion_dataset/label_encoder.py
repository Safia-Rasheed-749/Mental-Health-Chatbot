import pandas as pd

label_map = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

files = [
    "train_processed.csv",
    "validation_processed.csv",
    "test_processed.csv"
]

for file in files:

    path = f"datasets/emotion_dataset/processed/{file}"

    df = pd.read_csv(path)

    df["emotion"] = df["label"].map(label_map)

    df.to_csv(path, index=False)

print("=" * 50)
print("Label Encoding Completed Successfully")
print("=" * 50)