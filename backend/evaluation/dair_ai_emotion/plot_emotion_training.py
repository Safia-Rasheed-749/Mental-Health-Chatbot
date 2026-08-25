import os
import json
import matplotlib.pyplot as plt


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

TRAINER_STATE = os.path.join(
    BASE_DIR,
    "models",
    "emotion_dair_ai_roberta",
    "checkpoint-6000",
    "trainer_state.json"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "evaluation"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(TRAINER_STATE):
    raise FileNotFoundError(
        f"trainer_state.json not found:\n{TRAINER_STATE}"
    )


print("=" * 70)
print("Emotion Detection Training Graph Generation")
print("=" * 70)

print("\nLoading:")
print(TRAINER_STATE)


# ============================================================
# LOAD TRAINING HISTORY
# ============================================================

with open(
    TRAINER_STATE,
    "r",
    encoding="utf-8"
) as f:
    state = json.load(f)


log_history = state.get(
    "log_history",
    []
)

print(
    f"\nTotal log entries: {len(log_history)}"
)


# ============================================================
# EXTRACT TRAINING LOSS
# ============================================================

train_steps = []
train_loss = []

for entry in log_history:

    if "loss" in entry and "eval_loss" not in entry:

        if "step" in entry:

            train_steps.append(
                entry["step"]
            )

            train_loss.append(
                entry["loss"]
            )


# ============================================================
# EXTRACT VALIDATION RESULTS
# ============================================================

eval_steps = []
eval_loss = []
eval_accuracy = []
eval_precision = []
eval_recall = []
eval_f1 = []

for entry in log_history:

    if "eval_loss" in entry:

        if "step" in entry:

            eval_steps.append(
                entry["step"]
            )

        eval_loss.append(
            entry["eval_loss"]
        )

        if "eval_accuracy" in entry:
            eval_accuracy.append(
                entry["eval_accuracy"]
            )

        if "eval_precision" in entry:
            eval_precision.append(
                entry["eval_precision"]
            )

        if "eval_recall" in entry:
            eval_recall.append(
                entry["eval_recall"]
            )

        if "eval_f1" in entry:
            eval_f1.append(
                entry["eval_f1"]
            )


# ============================================================
# PRINT EXTRACTED INFORMATION
# ============================================================

print("\nTraining loss points:", len(train_loss))
print("Validation points:", len(eval_loss))

print("\nTraining loss:")
for step, loss in zip(
    train_steps,
    train_loss
):
    print(
        f"Step {step}: {loss:.6f}"
    )

print("\nValidation results:")

for i in range(len(eval_loss)):

    print(
        f"Point {i + 1}: "
        f"loss={eval_loss[i]:.6f}, "
        f"accuracy={eval_accuracy[i] if i < len(eval_accuracy) else 'N/A'}, "
        f"precision={eval_precision[i] if i < len(eval_precision) else 'N/A'}, "
        f"recall={eval_recall[i] if i < len(eval_recall) else 'N/A'}, "
        f"f1={eval_f1[i] if i < len(eval_f1) else 'N/A'}"
    )


# ============================================================
# GRAPH 1 — TRAINING LOSS
# ============================================================

if train_loss:

    plt.figure(figsize=(10, 6))

    plt.plot(
        train_steps,
        train_loss,
        marker="o"
    )

    plt.title(
        "Emotion Detection - Training Loss"
    )

    plt.xlabel(
        "Training Step"
    )

    plt.ylabel(
        "Training Loss"
    )

    plt.grid(True)

    plt.tight_layout()

    output = os.path.join(
        OUTPUT_DIR,
        "emotion_training_loss.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"\nSaved: {output}"
    )


# ============================================================
# GRAPH 2 — VALIDATION LOSS
# ============================================================

if eval_loss:

    plt.figure(figsize=(10, 6))

    plt.plot(
        eval_steps,
        eval_loss,
        marker="o"
    )

    plt.title(
        "Emotion Detection - Validation Loss"
    )

    plt.xlabel(
        "Training Step"
    )

    plt.ylabel(
        "Validation Loss"
    )

    plt.grid(True)

    plt.tight_layout()

    output = os.path.join(
        OUTPUT_DIR,
        "emotion_validation_loss.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output}"
    )


# ============================================================
# GRAPH 3 — VALIDATION ACCURACY
# ============================================================

if eval_accuracy:

    plt.figure(figsize=(10, 6))

    plt.plot(
        eval_steps,
        eval_accuracy,
        marker="o"
    )

    plt.title(
        "Emotion Detection - Validation Accuracy"
    )

    plt.xlabel(
        "Training Step"
    )

    plt.ylabel(
        "Accuracy"
    )

    plt.ylim(
        0.85,
        1.0
    )

    plt.grid(True)

    plt.tight_layout()

    output = os.path.join(
        OUTPUT_DIR,
        "emotion_validation_accuracy.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output}"
    )


# ============================================================
# GRAPH 4 — VALIDATION PRECISION / RECALL / F1
# ============================================================

if (
    eval_precision
    and eval_recall
    and eval_f1
):

    plt.figure(figsize=(10, 6))

    plt.plot(
        eval_steps,
        eval_precision,
        marker="o",
        label="Precision"
    )

    plt.plot(
        eval_steps,
        eval_recall,
        marker="o",
        label="Recall"
    )

    plt.plot(
        eval_steps,
        eval_f1,
        marker="o",
        label="F1-score"
    )

    plt.title(
        "Emotion Detection - Validation Metrics"
    )

    plt.xlabel(
        "Training Step"
    )

    plt.ylabel(
        "Score"
    )

    plt.ylim(
        0.80,
        1.0
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    output = os.path.join(
        OUTPUT_DIR,
        "emotion_validation_metrics.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output}"
    )


# ============================================================
# FINISHED
# ============================================================

print("\n" + "=" * 70)
print("GRAPH GENERATION COMPLETED")
print("=" * 70)