"""
================================================================
RoBERTa Stress Detection Model – Final Evaluation
================================================================

Model: roberta-base (stress_roberta)
Dataset: Stress Detection (binary classification)
Task: Predict Stress vs No Stress

This script evaluates the trained model on the held‑out test set
and generates:
- Metrics (accuracy, precision, recall, F1)
- Confusion matrix (image + table)
- Classification report
- Predictions with confidence
- Wrong predictions analysis
- Sample predictions
================================================================
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
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]  # backend directory

# Model path (stress_roberta)
MODEL_PATH = BASE_DIR / "models" / "stress_roberta"

# Test dataset path (the same file used as validation during training)
TEST_PATH = BASE_DIR / "datasets" / "stress" / "processed" / "clean_test.csv"

# Output directory
OUTPUT_DIR = BASE_DIR / "evaluation" / "stress_detection"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("RoBERTa Stress Detection Model – Final Evaluation")
print("=" * 70)
print(f"\nModel Path: {MODEL_PATH}")
print(f"Test Dataset: {TEST_PATH}")
print(f"Output Directory: {OUTPUT_DIR}")

# ============================================================
# CHECK FILES
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"❌ Model not found: {MODEL_PATH}")

if not TEST_PATH.exists():
    raise FileNotFoundError(f"❌ Test dataset not found: {TEST_PATH}")

# ============================================================
# LOAD LABEL MAPPING
# ============================================================

# Try loading from model folder if exists, otherwise use default
label_mapping = {
    "0": "No Stress",
    "1": "Stress"
}

# Check if label_mapping.json exists in model folder
mapping_file = MODEL_PATH / "label_mapping.json"
if mapping_file.exists():
    with open(mapping_file, "r") as f:
        label_mapping = json.load(f)
        # Ensure keys are strings
        label_mapping = {str(k): v for k, v in label_mapping.items()}

print("\nLabel Mapping:")
for k, v in label_mapping.items():
    print(f"  {k} -> {v}")

# ============================================================
# LOAD TEST DATASET
# ============================================================

print("\n" + "=" * 70)
print("Loading Test Dataset")
print("=" * 70)

df = pd.read_csv(TEST_PATH)
print(f"\nDataset shape: {df.shape}")

# Ensure required columns exist
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

print(f"Samples after cleaning: {len(df)}")

print("\nClass Distribution in Test Set:")
class_dist = df["label"].value_counts().sort_index()
for label, count in class_dist.items():
    label_name = label_mapping.get(str(label), f"Label_{label}")
    print(f"  {label_name} ({label}): {count}")

# ============================================================
# LOAD TOKENIZER & MODEL
# ============================================================

print("\n" + "=" * 70)
print("Loading Model and Tokenizer")
print("=" * 70)

tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH))
model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_PATH))
model.eval()

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

print(f"\n✅ Model loaded successfully.")
print(f"   Device: {device}")
print(f"   Number of labels: {model.config.num_labels}")

# ============================================================
# RUN PREDICTIONS
# ============================================================

print("\n" + "=" * 70)
print("Running Test Predictions")
print("=" * 70)

texts = df["text"].tolist()
true_labels = df["label"].tolist()

predicted_labels = []
prediction_confidences = []

batch_size = 16
start_time = time.time()

for start in range(0, len(texts), batch_size):
    batch_texts = texts[start:start + batch_size]
    
    encoded = tokenizer(
        batch_texts,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )
    
    encoded = {key: value.to(device) for key, value in encoded.items()}
    
    with torch.no_grad():
        outputs = model(**encoded)
        probabilities = torch.softmax(outputs.logits, dim=-1)
        predictions = torch.argmax(probabilities, dim=-1)
        confidences = torch.max(probabilities, dim=-1).values
    
    predicted_labels.extend(predictions.cpu().numpy().tolist())
    prediction_confidences.extend(confidences.cpu().numpy().tolist())
    
    processed = min(start + batch_size, len(texts))
    print(f"\rProcessed {processed}/{len(texts)} samples", end="")

evaluation_time = time.time() - start_time

print("\n")
print(f"✅ Predictions completed!")
print(f"   Evaluation time: {evaluation_time:.2f} seconds")

# ============================================================
# CALCULATE METRICS
# ============================================================

print("\n" + "=" * 70)
print("Calculating Metrics")
print("=" * 70)

# Overall metrics
accuracy = accuracy_score(true_labels, predicted_labels)
precision, recall, f1, _ = precision_recall_fscore_support(
    true_labels, predicted_labels, average="binary", zero_division=0
)
macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
    true_labels, predicted_labels, average="macro", zero_division=0
)

# Per-class metrics
per_class_precision, per_class_recall, per_class_f1, _ = precision_recall_fscore_support(
    true_labels, predicted_labels, average=None, zero_division=0
)

print("\n📊 FINAL TEST RESULTS")
print("-" * 50)
print(f"✅ Accuracy          : {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"   Precision (binary): {precision:.4f} ({precision*100:.2f}%)")
print(f"   Recall (binary)   : {recall:.4f} ({recall*100:.2f}%)")
print(f"   F1 (binary)       : {f1:.4f} ({f1*100:.2f}%)")
print(f"   Macro Precision   : {macro_precision:.4f}")
print(f"   Macro Recall      : {macro_recall:.4f}")
print(f"   Macro F1          : {macro_f1:.4f}")

print("\nPer-Class Performance:")
labels = sorted(set(true_labels))
for i, label in enumerate(labels):
    label_name = label_mapping.get(str(label), f"Label_{label}")
    print(f"  {label_name}:")
    print(f"    Precision: {per_class_precision[i]:.4f}")
    print(f"    Recall: {per_class_recall[i]:.4f}")
    print(f"    F1: {per_class_f1[i]:.4f}")

# ============================================================
# CLASSIFICATION REPORT
# ============================================================

target_labels = sorted(set(true_labels) | set(predicted_labels))
target_names = [label_mapping.get(str(label), str(label)) for label in target_labels]

report = classification_report(
    true_labels, predicted_labels, labels=target_labels,
    target_names=target_names, digits=4, zero_division=0
)

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)
print(report)

# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(true_labels, predicted_labels, labels=target_labels)

print("\n" + "=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)
print("Rows: Actual Labels, Columns: Predicted Labels")
print(pd.DataFrame(cm, index=target_names, columns=target_names))

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(
    cm, 
    annot=True, 
    fmt="d", 
    cmap="Blues",
    xticklabels=target_names, 
    yticklabels=target_names,
    cbar_kws={'label': 'Number of Samples'}
)
plt.title("Stress Detection Model - Confusion Matrix", fontsize=14, fontweight='bold')
plt.xlabel("Predicted Label", fontsize=12)
plt.ylabel("Actual Label", fontsize=12)
plt.tight_layout()

confusion_matrix_file = OUTPUT_DIR / "stress_confusion_matrix.png"
plt.savefig(confusion_matrix_file, dpi=300, bbox_inches="tight")
plt.close()

print(f"\n✅ Confusion matrix saved to: {confusion_matrix_file}")

# ============================================================
# SAVE PREDICTIONS
# ============================================================

results_df = df.copy()
results_df["predicted_label"] = predicted_labels
results_df["prediction_confidence"] = prediction_confidences
results_df["actual_class"] = results_df["label"].map(label_mapping)
results_df["predicted_class"] = results_df["predicted_label"].map(label_mapping)
results_df["correct"] = results_df["label"] == results_df["predicted_label"]

predictions_file = OUTPUT_DIR / "stress_predictions.csv"
results_df.to_csv(predictions_file, index=False, encoding="utf-8-sig")
print(f"✅ Predictions saved to: {predictions_file}")

# ============================================================
# SAMPLE PREDICTIONS
# ============================================================

print("\n" + "=" * 70)
print("SAMPLE PREDICTIONS")
print("=" * 70)

# Get 5 correct and 5 wrong predictions (if available)
correct_samples = results_df[results_df["correct"] == True].head(5)
wrong_samples = results_df[results_df["correct"] == False].head(5)

print("\n✅ Correct Predictions:")
for idx, row in correct_samples.iterrows():
    print(f"\n  Text: {row['text'][:80]}...")
    print(f"  Actual: {row['actual_class']} | Predicted: {row['predicted_class']} (Confidence: {row['prediction_confidence']:.2%})")

if len(wrong_samples) > 0:
    print("\n❌ Wrong Predictions:")
    for idx, row in wrong_samples.iterrows():
        print(f"\n  Text: {row['text'][:80]}...")
        print(f"  Actual: {row['actual_class']} | Predicted: {row['predicted_class']} (Confidence: {row['prediction_confidence']:.2%})")
else:
    print("\n✅ No wrong predictions! Model is perfect on this test set.")

# ============================================================
# SAVE WRONG PREDICTIONS
# ============================================================

wrong_predictions = results_df[results_df["correct"] == False].copy()
wrong_predictions_file = OUTPUT_DIR / "stress_wrong_predictions.csv"
wrong_predictions.to_csv(wrong_predictions_file, index=False, encoding="utf-8-sig")
print(f"\n✅ Wrong predictions saved to: {wrong_predictions_file}")
print(f"   Total wrong predictions: {len(wrong_predictions)}")

# ============================================================
# CONFIDENCE ANALYSIS
# ============================================================

correct_conf = results_df[results_df["correct"] == True]["prediction_confidence"]
wrong_conf = results_df[results_df["correct"] == False]["prediction_confidence"]

confidence_file = OUTPUT_DIR / "stress_confidence_analysis.txt"
with open(confidence_file, "w", encoding="utf-8") as f:
    f.write("Confidence Analysis - Stress Detection Model\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Correct Predictions: {len(correct_conf)}\n")
    f.write(f"Wrong Predictions: {len(wrong_conf)}\n\n")
    f.write("Confidence Scores:\n")
    if len(correct_conf) > 0:
        f.write(f"  Correct Mean: {correct_conf.mean():.4f}\n")
        f.write(f"  Correct Std: {correct_conf.std():.4f}\n")
        f.write(f"  Correct Min: {correct_conf.min():.4f}\n")
        f.write(f"  Correct Max: {correct_conf.max():.4f}\n")
    if len(wrong_conf) > 0:
        f.write(f"  Wrong Mean: {wrong_conf.mean():.4f}\n")
        f.write(f"  Wrong Std: {wrong_conf.std():.4f}\n")
        f.write(f"  Wrong Min: {wrong_conf.min():.4f}\n")
        f.write(f"  Wrong Max: {wrong_conf.max():.4f}\n")

print(f"✅ Confidence analysis saved to: {confidence_file}")

# ============================================================
# SAVE COMPLETE METRICS
# ============================================================

metrics_file = OUTPUT_DIR / "stress_metrics.txt"
with open(metrics_file, "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("STRESS DETECTION MODEL - FINAL EVALUATION\n")
    f.write("=" * 70 + "\n\n")
    
    # Model Information
    f.write("MODEL INFORMATION\n")
    f.write("-" * 40 + "\n")
    f.write(f"Base Model: roberta-base\n")
    f.write(f"Fine-tuned Model: stress_roberta\n")
    f.write(f"Task: Binary Classification (Stress vs No Stress)\n")
    f.write(f"Number of Classes: 2\n")
    f.write(f"Classes: 0 = No Stress, 1 = Stress\n")
    f.write(f"Device: {device}\n")
    f.write(f"Evaluation Time: {evaluation_time:.2f} seconds\n\n")
    
    # Dataset Information
    f.write("DATASET INFORMATION\n")
    f.write("-" * 40 + "\n")
    f.write(f"Test Samples: {len(df)}\n")
    f.write(f"Class Distribution:\n")
    for label, count in class_dist.items():
        label_name = label_mapping.get(str(label), f"Label_{label}")
        f.write(f"  {label_name}: {count}\n")
    f.write("\n")
    
    # Label Mapping
    f.write("LABEL MAPPING\n")
    f.write("-" * 40 + "\n")
    for key, value in label_mapping.items():
        f.write(f"  {key} -> {value}\n")
    f.write("\n")
    
    # Test Metrics
    f.write("TEST METRICS\n")
    f.write("-" * 40 + "\n")
    f.write(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)\n")
    f.write(f"Precision (binary): {precision:.4f} ({precision*100:.2f}%)\n")
    f.write(f"Recall (binary): {recall:.4f} ({recall*100:.2f}%)\n")
    f.write(f"F1 (binary): {f1:.4f} ({f1*100:.2f}%)\n")
    f.write(f"Macro Precision: {macro_precision:.4f}\n")
    f.write(f"Macro Recall: {macro_recall:.4f}\n")
    f.write(f"Macro F1: {macro_f1:.4f}\n\n")
    
    # Per-Class Performance
    f.write("PER-CLASS PERFORMANCE\n")
    f.write("-" * 40 + "\n")
    for i, label in enumerate(target_labels):
        label_name = label_mapping.get(str(label), f"Label_{label}")
        f.write(f"{label_name}:\n")
        f.write(f"  Precision: {per_class_precision[i]:.4f}\n")
        f.write(f"  Recall: {per_class_recall[i]:.4f}\n")
        f.write(f"  F1: {per_class_f1[i]:.4f}\n")
    f.write("\n")
    
    # Correct/Wrong Counts
    f.write("PREDICTION COUNTS\n")
    f.write("-" * 40 + "\n")
    f.write(f"Correct Predictions: {int(results_df['correct'].sum())}\n")
    f.write(f"Wrong Predictions: {int((~results_df['correct']).sum())}\n")
    f.write(f"Accuracy: {accuracy*100:.2f}%\n\n")
    
    # Confusion Matrix
    f.write("CONFUSION MATRIX\n")
    f.write("-" * 40 + "\n")
    f.write("Rows: Actual Labels, Columns: Predicted Labels\n")
    f.write(pd.DataFrame(cm, index=target_names, columns=target_names).to_string())
    f.write("\n\n")
    
    # Classification Report
    f.write("CLASSIFICATION REPORT\n")
    f.write("-" * 40 + "\n")
    f.write(report)
    f.write("\n")
    
    # Sample Predictions
    f.write("SAMPLE PREDICTIONS\n")
    f.write("-" * 40 + "\n")
    f.write("Correct Predictions:\n")
    for idx, row in correct_samples.iterrows():
        f.write(f"  Text: {row['text'][:80]}...\n")
        f.write(f"  Actual: {row['actual_class']} | Predicted: {row['predicted_class']} (Confidence: {row['prediction_confidence']:.2%})\n\n")
    
    if len(wrong_samples) > 0:
        f.write("Wrong Predictions:\n")
        for idx, row in wrong_samples.iterrows():
            f.write(f"  Text: {row['text'][:80]}...\n")
            f.write(f"  Actual: {row['actual_class']} | Predicted: {row['predicted_class']} (Confidence: {row['prediction_confidence']:.2%})\n\n")
    else:
        f.write("No wrong predictions on the test set.\n")

print(f"✅ Complete metrics saved to: {metrics_file}")

# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("✅ EVALUATION COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\n📁 Generated Files:")
files = [
    ("Metrics Summary", metrics_file),
    ("Confusion Matrix Image", confusion_matrix_file),
    ("All Predictions", predictions_file),
    ("Wrong Predictions", wrong_predictions_file),
    ("Confidence Analysis", confidence_file),
]

for name, file_path in files:
    if file_path.exists():
        print(f"  ✅ {name}: {file_path.name}")

print(f"\n📊 Summary:")
print(f"  Test Samples: {len(df)}")
print(f"  Accuracy: {accuracy*100:.2f}%")
print(f"  F1 Score: {f1*100:.2f}%")
print(f"  Correct: {results_df['correct'].sum()}")
print(f"  Wrong: {(~results_df['correct']).sum()}")

print("\n🎉 Evaluation finished! All results are in:")
print(f"   {OUTPUT_DIR}")