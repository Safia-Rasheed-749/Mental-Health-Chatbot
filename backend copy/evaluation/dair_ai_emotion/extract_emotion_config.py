import os
import json


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

STATE_FILE = os.path.join(
    BASE_DIR,
    "models",
    "emotion_dair_ai_roberta",
    "checkpoint-6000",
    "trainer_state.json"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "evaluation",
    "emotion_training_history.json"
)


with open(
    STATE_FILE,
    "r",
    encoding="utf-8"
) as f:
    state = json.load(f)


print("=" * 70)
print("EMOTION TRAINING HISTORY")
print("=" * 70)

print("\nTrainer state keys:")
for key in state.keys():
    print("-", key)


print("\nTraining configuration stored in trainer state:")

for key in [
    "best_model_checkpoint",
    "best_metric",
    "global_step",
    "epoch",
    "max_steps",
    "num_train_epochs"
]:

    if key in state:
        print(
            f"{key}: {state[key]}"
        )


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        state,
        f,
        indent=4
    )


print("\nFull training history saved to:")
print(OUTPUT_FILE)

print("\nDone.")