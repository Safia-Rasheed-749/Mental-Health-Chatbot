label_map = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

print("=" * 40)
print("Emotion Label Mapping")
print("=" * 40)

for key, value in label_map.items():
    print(f"{key} --> {value}")