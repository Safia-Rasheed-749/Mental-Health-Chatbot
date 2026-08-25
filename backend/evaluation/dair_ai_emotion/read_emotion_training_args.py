import os
import torch


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ARGS_PATH = os.path.join(
    BASE_DIR,
    "models",
    "emotion_dair_ai_roberta",
    "training_args.bin"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "evaluation",
    "emotion_training_args.txt"
)


print("=" * 70)
print("EMOTION DETECTION - SAVED TRAINING ARGUMENTS")
print("=" * 70)

print("\nLoading:")
print(ARGS_PATH)

if not os.path.exists(ARGS_PATH):
    raise FileNotFoundError(
        f"File not found:\n{ARGS_PATH}"
    )


args = torch.load(
    ARGS_PATH,
    map_location="cpu",
    weights_only=False
)

print("\nTrainingArguments attributes:\n")

# Important parameters
important = [
    "learning_rate",
    "per_device_train_batch_size",
    "per_device_eval_batch_size",
    "gradient_accumulation_steps",
    "num_train_epochs",
    "weight_decay",
    "warmup_ratio",
    "warmup_steps",
    "logging_steps",
    "eval_steps",
    "save_steps",
    "save_total_limit",
    "evaluation_strategy",
    "eval_strategy",
    "save_strategy",
    "load_best_model_at_end",
    "metric_for_best_model",
    "greater_is_better",
    "fp16",
    "bf16",
    "seed",
    "data_seed",
    "optim",
    "lr_scheduler_type",
    "max_grad_norm",
    "gradient_checkpointing",
    "per_device_train_batch_size",
]

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "EMOTION DETECTION - SAVED TRAINING ARGUMENTS\n"
    )

    f.write("=" * 70 + "\n\n")

    for name in important:

        if hasattr(args, name):

            value = getattr(args, name)

            print(
                f"{name}: {value}"
            )

            f.write(
                f"{name}: {value}\n"
            )

print("\n" + "=" * 70)

print(
    f"Saved to:\n{OUTPUT_PATH}"
)

print("=" * 70)