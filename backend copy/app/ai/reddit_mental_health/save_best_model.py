"""
Save the best model from checkpoints without retraining
"""
import json
import shutil
from pathlib import Path
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# ===== FIX: Use correct path relative to current directory =====
# Since you're running from 'backend' directory
MODEL_DIR = Path("models/reddit_mental_health").resolve()
print(f"Model directory: {MODEL_DIR}")

# Check if directory exists
if not MODEL_DIR.exists():
    print(f"❌ ERROR: Directory not found: {MODEL_DIR}")
    exit(1)

# Find all checkpoints
checkpoints = sorted([d for d in MODEL_DIR.iterdir() if d.is_dir() and d.name.startswith("checkpoint-")])

if not checkpoints:
    print("❌ No checkpoints found in:", MODEL_DIR)
    exit(1)

print("=" * 60)
print("Available Checkpoints")
print("=" * 60)

best_checkpoint = None
best_accuracy = 0
checkpoint_data = []

for ckpt in checkpoints:
    state_path = ckpt / "trainer_state.json"
    if state_path.exists():
        with open(state_path, "r") as f:
            state = json.load(f)
        
        # Extract best validation accuracy
        for log in state.get("log_history", []):
            if "eval_accuracy" in log:
                acc = log["eval_accuracy"]
                checkpoint_data.append((ckpt.name, acc))
                if acc > best_accuracy:
                    best_accuracy = acc
                    best_checkpoint = ckpt
                print(f"{ckpt.name}: eval_accuracy = {acc:.4f}")

if best_checkpoint:
    print(f"\n✅ Best checkpoint: {best_checkpoint.name}")
    print(f"   Validation Accuracy: {best_accuracy:.4f}")
    
    # ===== Convert to string for from_pretrained =====
    checkpoint_path = str(best_checkpoint)
    model_path = str(MODEL_DIR)
    
    print(f"\nLoading model from: {checkpoint_path}")
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path)
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
    
    # Save as final model
    print(f"\nSaving best model to: {model_path}")
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    
    # Save evaluation summary
    with open(MODEL_DIR / "best_model_info.txt", "w") as f:
        f.write(f"Best Checkpoint: {best_checkpoint.name}\n")
        f.write(f"Validation Accuracy: {best_accuracy:.4f}\n")
        f.write("Model saved from best checkpoint without retraining.\n")
        
    print("\n🎉 Success! Best model saved to:", MODEL_DIR)
else:
    print("❌ No checkpoint found with evaluation metrics.")