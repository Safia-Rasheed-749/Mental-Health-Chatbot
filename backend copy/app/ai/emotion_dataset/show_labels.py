import pandas as pd

train = pd.read_csv("datasets/emotion_dataset/raw/train.csv")

label_map = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

print("=" * 50)
print("Emotion Dataset Labels")
print("=" * 50)

for key, value in label_map.items():
    print(f"{key} --> {value}")

print("\nLabel Distribution")
print(train["label"].value_counts().sort_index())