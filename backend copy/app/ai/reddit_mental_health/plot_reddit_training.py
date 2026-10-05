"""
Extract training history from checkpoint logs and plot curves
"""
import json
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Path to the model directory (where checkpoints are)
MODEL_DIR = Path("models/reddit_mental_health")

# Find the latest checkpoint (or the one with best accuracy)
checkpoints = sorted([d for d in MODEL_DIR.iterdir() if d.is_dir() and d.name.startswith("checkpoint-")])
if not checkpoints:
    print("No checkpoints found.")
    exit()

best_ckpt = checkpoints[-1]  # latest, or you can select by best accuracy
state_file = best_ckpt / "trainer_state.json"
if not state_file.exists():
    print(f"No trainer_state.json in {best_ckpt}")
    exit()

with open(state_file, "r") as f:
    state = json.load(f)

# Create dataframe from log_history
history = pd.DataFrame(state["log_history"])

# Extract training loss
train_loss = history[history["loss"].notna()][["step", "loss"]]

# Extract validation accuracy
val_acc = history[history["eval_accuracy"].notna()][["step", "eval_accuracy"]]
val_loss = history[history["eval_loss"].notna()][["step", "eval_loss"]]

# Plot training loss
plt.figure(figsize=(8,5))
plt.plot(train_loss["step"], train_loss["loss"], label="Training Loss")
plt.xlabel("Step")
plt.ylabel("Loss")
plt.title("Reddit Mental Health - Training Loss")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("evaluation/reddit_mental_health/reddit_training_loss.png", dpi=300)
plt.close()

# Plot validation accuracy
if not val_acc.empty:
    plt.figure(figsize=(8,5))
    plt.plot(val_acc["step"], val_acc["eval_accuracy"], label="Validation Accuracy", color="green")
    plt.xlabel("Step")
    plt.ylabel("Accuracy")
    plt.title("Reddit Mental Health - Validation Accuracy")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("evaluation/reddit_mental_health/reddit_validation_accuracy.png", dpi=300)
    plt.close()

# Plot validation loss
if not val_loss.empty:
    plt.figure(figsize=(8,5))
    plt.plot(val_loss["step"], val_loss["eval_loss"], label="Validation Loss", color="red")
    plt.xlabel("Step")
    plt.ylabel("Loss")
    plt.title("Reddit Mental Health - Validation Loss")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("evaluation/reddit_mental_health/reddit_validation_loss.png", dpi=300)
    plt.close()

print("✅ Training curves saved to evaluation/reddit_mental_health/")