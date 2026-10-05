"""
Quick test of saved best model
"""
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json

# ===== FIX: Use correct path =====
MODEL_DIR = Path("models/reddit_mental_health").resolve()
model_path = str(MODEL_DIR)

print("=" * 60)
print("Testing Best Reddit Mental Health Model")
print("=" * 60)
print(f"Model path: {model_path}")

# Check if model exists
if not MODEL_DIR.exists():
    print(f"\n❌ ERROR: Directory not found: {MODEL_DIR}")
    exit(1)

if not (MODEL_DIR / "config.json").exists():
    print("\n❌ ERROR: No model found! Run save_best_model.py first.")
    exit(1)

# Load model
print("\nLoading model...")
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load label mapping
label_mapping_path = MODEL_DIR / "label_mapping.json"
if label_mapping_path.exists():
    with open(label_mapping_path, "r") as f:
        label_mapping = json.load(f)
    print(f"Loaded {len(label_mapping)} labels")
else:
    label_mapping = {"0": "ADHD", "1": "OCD", "2": "PTSD", "3": "Depression", "4": "Aspergers"}
    print("Using default label mapping")

# Test samples
test_texts = [
    "I've been feeling very depressed lately and can't get out of bed. Everything feels hopeless.",
    "I'm so happy today! Everything is going well and I feel great.",
    "I can't stop obsessing over small details, it's exhausting and I keep checking things repeatedly.",
    "I keep having flashbacks of the accident, I can't sleep and I feel anxious all the time.",
    "I struggle with social interactions and understanding other people's emotions.",
    "I can't focus on my work and I'm always fidgeting, my mind races constantly.",
]

print("\n" + "=" * 60)
print("Test Results")
print("=" * 60)

model.eval()
with torch.no_grad():
    for i, text in enumerate(test_texts, 1):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        pred = torch.argmax(probs, dim=-1).item()
        confidence = probs[0][pred].item()
        
        # Convert label key to string for lookup
        label = label_mapping.get(str(pred), f"Label_{pred}")
        
        print(f"\n{i}. Text: {text[:70]}...")
        print(f"   Predicted: {label} (confidence: {confidence:.2%})")
        print("-" * 40)
        
# Show all probabilities for first sample
print("\n" + "=" * 60)
print("Detailed Probabilities (Sample 1)")
print("=" * 60)

sample_text = test_texts[0]
inputs = tokenizer(sample_text, return_tensors="pt", truncation=True, max_length=128)
outputs = model(**inputs)
probs = torch.softmax(outputs.logits, dim=-1)

for i, prob in enumerate(probs[0]):
    label = label_mapping.get(str(i), f"Label_{i}")
    print(f"{label}: {prob.item():.2%}")

print("\n✅ Testing complete!")