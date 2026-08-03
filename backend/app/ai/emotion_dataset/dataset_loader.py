from datasets import load_dataset
import pandas as pd
import os

# ==============================
# Load Emotion Dataset
# ==============================

dataset = load_dataset("dair-ai/emotion")

# ==============================
# Output Folder
# ==============================

output_dir = "datasets/emotion_dataset/raw"
os.makedirs(output_dir, exist_ok=True)

# ==============================
# Save Splits
# ==============================

pd.DataFrame(dataset["train"]).to_csv(
    f"{output_dir}/train.csv",
    index=False
)

pd.DataFrame(dataset["validation"]).to_csv(
    f"{output_dir}/validation.csv",
    index=False
)

pd.DataFrame(dataset["test"]).to_csv(
    f"{output_dir}/test.csv",
    index=False
)

print("=" * 50)
print("Emotion Dataset Saved Successfully")
print("=" * 50)

print("\nFiles Created:")

print("train.csv")
print("validation.csv")
print("test.csv")