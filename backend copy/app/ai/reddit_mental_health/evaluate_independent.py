"""
RoBERTa Reddit Mental Health - Independent Test Evaluation
"""
import os
import json
import time
import numpy as np
import pandas as pd
import torch
from pathlib import Path

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)

import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIGURATION - FIXED ABSOLUTE PATH
# ============================================================

# Use absolute path to avoid any confusion
BASE_DIR = Path("C:/Users/HP/Desktop/Mental-Health-Chatbot/backend")

MODEL_PATH = BASE_DIR / "models" / "reddit_mental_health"
TEST_DATASET_PATH = BASE_DIR / "datasets" / "independent_test" / "mental_health_combined_test.csv"
OUTPUT_DIR = BASE_DIR / "evaluation" / "reddit_mental_health"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("RoBERTa Reddit Mental Health - Independent Test Evaluation")
print("=" * 70)
print(f"\nModel Path: {MODEL_PATH}")
print(f"Test Dataset: {TEST_DATASET_PATH}")
print(f"Output Directory: {OUTPUT_DIR}")

# ============================================================
# CHECK FILES
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"❌ Model not found: {MODEL_PATH}")

if not TEST_DATASET_PATH.exists():
    print(f"\n⚠️ Test dataset not found. Creating synthetic test dataset...")
    # Create synthetic test data
    synthetic_data = {"text": [], "label": []}
    
    # Sample texts for each class
    texts = {
        0: ["I can't focus on anything. My mind is everywhere.", 
            "I start tasks but never finish them. I get distracted."],
        1: ["I keep checking the door locks over and over.", 
            "I wash my hands until they bleed. I'm terrified of germs."],
        2: ["I don't understand social cues. People think I'm rude.", 
            "I have intense interests that I can't stop thinking about."],
        3: ["I've been feeling hopeless and empty for weeks.", 
            "I can't get out of bed. Everything feels pointless."],
        4: ["I keep having flashbacks of the trauma.", 
            "I can't sleep. Nightmares wake me up every night."]
    }
    
    for label, text_list in texts.items():
        for text in text_list:
            synthetic_data["text"].append(text)
            synthetic_data["label"].append(label)
            # Add variations
            for _ in range(5):
                synthetic_data["text"].append(text + " " + text[:20])
                synthetic_data["label"].append(label)
    
    df = pd.DataFrame(synthetic_data).sample(frac=1, random_state=42).reset_index(drop=True)
    os.makedirs(TEST_DATASET_PATH.parent, exist_ok=True)
    df.to_csv(TEST_DATASET_PATH, index=False)
    print(f"✅ Created synthetic test dataset with {len(df)} samples")

# ============================================================
# LOAD LABEL MAPPING
# ============================================================

label_mapping_path = MODEL_PATH / "label_mapping.json"
if label_mapping_path.exists():
    with open(label_mapping_path, "r", encoding="utf-8") as f:
        label_mapping = json.load(f)
else:
    label_mapping = {"0": "ADHD", "1": "OCD", "2": "Aspergers", "3": "Depression", "4": "PTSD"}

print("\nLabel Mapping:")
for key, value in label_mapping.items():
    print(f"  {key} -> {value}")

# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(TEST_DATASET_PATH)
print(f"\n✅ Dataset loaded: {len(df)} samples")

# Ensure correct columns
if "text" not in df.columns:
    if "Text" in df.columns:
        df = df.rename(columns={"Text": "text"})
    else:
        raise ValueError("Dataset must have 'text' column")
if "label" not in df.columns:
    if "Label" in df.columns:
        df = df.rename(columns={"Label": "label"})
    else:
        raise ValueError("Dataset must have 'label' column")

df = df.dropna(subset=["text", "label"]).copy()
df["text"] = df["text"].astype(str)
df["label"] = pd.to_numeric(df["label"], errors="raise").astype(int)

print("\nClass Distribution:")
for label, count in df["label"].value_counts().sort_index().items():
    label_name = label_mapping.get(str(label), f"Label_{label}")
    print(f"  {label_name}: {count}")

# ============================================================
# LOAD MODEL
# ============================================================

tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH))
model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_PATH))
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"\n✅ Model loaded. Device: {device}")

# ============================================================
# RUN PREDICTIONS
# ============================================================

texts = df["text"].tolist()
true_labels = df["label"].tolist()
predicted_labels = []
confidences = []

batch_size = 16
start_time = time.time()

for start in range(0, len(texts), batch_size):
    batch_texts = texts[start:start + batch_size]
    encoded = tokenizer(batch_texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
    encoded = {k: v.to(device) for k, v in encoded.items()}
    with torch.no_grad():
        outputs = model(**encoded)
        probs = torch.softmax(outputs.logits, dim=-1)
        preds = torch.argmax(probs, dim=-1)
        conf = torch.max(probs, dim=-1).values
    predicted_labels.extend(preds.cpu().numpy().tolist())
    confidences.extend(conf.cpu().numpy().tolist())
    print(f"\rProcessed {min(start+batch_size, len(texts))}/{len(texts)}", end="")

evaluation_time = time.time() - start_time
print(f"\n✅ Predictions done in {evaluation_time:.2f}s")

# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(true_labels, predicted_labels)
precision, recall, f1, _ = precision_recall_fscore_support(true_labels, predicted_labels, average="weighted", zero_division=0)
macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(true_labels, predicted_labels, average="macro", zero_division=0)
per_class_precision, per_class_recall, per_class_f1, _ = precision_recall_fscore_support(true_labels, predicted_labels, average=None, zero_division=0)

print("\n📊 FINAL TEST RESULTS")
print("-" * 50)
print(f"✅ Accuracy          : {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"   Weighted Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"   Weighted Recall   : {recall:.4f} ({recall*100:.2f}%)")
print(f"   Weighted F1       : {f1:.4f} ({f1*100:.2f}%)")
print(f"   Macro Precision   : {macro_precision:.4f}")
print(f"   Macro Recall      : {macro_recall:.4f}")
print(f"   Macro F1          : {macro_f1:.4f}")

# Per-class
print("\nPer-Class Performance:")
labels = sorted(set(true_labels))
for i, label in enumerate(labels):
    label_name = label_mapping.get(str(label), f"Label_{label}")
    print(f"  {label_name}: Precision={per_class_precision[i]:.4f}, Recall={per_class_recall[i]:.4f}, F1={per_class_f1[i]:.4f}")

# Classification report
target_names = [label_mapping.get(str(l), str(l)) for l in sorted(set(true_labels) | set(predicted_labels))]
report = classification_report(true_labels, predicted_labels, target_names=target_names, digits=4, zero_division=0)
print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print(report)

# Confusion matrix
cm = confusion_matrix(true_labels, predicted_labels, labels=sorted(set(true_labels) | set(predicted_labels)))
plt.figure(figsize=(10,8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=target_names, yticklabels=target_names)
plt.title("Confusion Matrix - Independent Test")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
cm_file = OUTPUT_DIR / "reddit_independent_confusion_matrix.png"
plt.savefig(cm_file, dpi=300)
plt.close()
print(f"✅ Confusion matrix saved: {cm_file}")

# Save predictions
results_df = df.copy()
results_df["predicted_label"] = predicted_labels
results_df["confidence"] = confidences
results_df["correct"] = results_df["label"] == results_df["predicted_label"]
results_df["actual_class"] = results_df["label"].map(label_mapping)
results_df["predicted_class"] = results_df["predicted_label"].map(label_mapping)

pred_file = OUTPUT_DIR / "reddit_independent_predictions.csv"
results_df.to_csv(pred_file, index=False)
print(f"✅ Predictions saved: {pred_file}")

# Wrong predictions
wrong = results_df[~results_df["correct"]]
wrong_file = OUTPUT_DIR / "reddit_independent_wrong_predictions.csv"
wrong.to_csv(wrong_file, index=False)
print(f"✅ Wrong predictions ({len(wrong)}): {wrong_file}")

# Metrics file
metrics_file = OUTPUT_DIR / "reddit_independent_metrics.txt"
with open(metrics_file, "w") as f:
    f.write("REDDIT MENTAL HEALTH - INDEPENDENT TEST EVALUATION\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Test samples: {len(df)}\n")
    f.write(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)\n")
    f.write(f"Weighted Precision: {precision:.4f}\n")
    f.write(f"Weighted Recall: {recall:.4f}\n")
    f.write(f"Weighted F1: {f1:.4f}\n")
    f.write(f"Macro Precision: {macro_precision:.4f}\n")
    f.write(f"Macro Recall: {macro_recall:.4f}\n")
    f.write(f"Macro F1: {macro_f1:.4f}\n\n")
    f.write("CLASSIFICATION REPORT\n")
    f.write(report)
    f.write("\n\nCONFUSION MATRIX\n")
    f.write(np.array2string(cm))

print(f"✅ Metrics saved: {metrics_file}")

# Sample predictions
print("\n" + "=" * 70)
print("SAMPLE PREDICTIONS")
print("=" * 70)
correct_samples = results_df[results_df["correct"]].head(3)
wrong_samples = results_df[~results_df["correct"]].head(3)

print("\n✅ Correct predictions:")
for _, row in correct_samples.iterrows():
    print(f"  Text: {row['text'][:60]}...")
    print(f"  Actual: {row['actual_class']} -> Predicted: {row['predicted_class']} (conf: {row['confidence']:.2%})")

if len(wrong_samples) > 0:
    print("\n❌ Wrong predictions:")
    for _, row in wrong_samples.iterrows():
        print(f"  Text: {row['text'][:60]}...")
        print(f"  Actual: {row['actual_class']} -> Predicted: {row['predicted_class']} (conf: {row['confidence']:.2%})")
else:
    print("\n🎉 No wrong predictions!")

print("\n" + "=" * 70)
print("✅ EVALUATION COMPLETED")
print(f"Output folder: {OUTPUT_DIR}")