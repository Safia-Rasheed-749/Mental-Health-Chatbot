"""
============================================================
Depression Label Encoder
Project : AI Mental Health Chatbot
============================================================
"""

import os
import json

# ---------------------------------------------------------
# Label Mapping
# ---------------------------------------------------------

label_mapping = {
    0: "No Depression",
    1: "Depression"
}

# ---------------------------------------------------------
# Save Path
# ---------------------------------------------------------

SAVE_PATH = os.path.join(
    os.getcwd(),
    "models",
    "depression",
    "label_mapping.json"
)

os.makedirs(
    os.path.dirname(SAVE_PATH),
    exist_ok=True
)

# ---------------------------------------------------------
# Print Labels
# ---------------------------------------------------------

print("\n========== Depression Labels ==========\n")

for key, value in label_mapping.items():
    print(f"{key} --> {value}")

# ---------------------------------------------------------
# Save JSON
# ---------------------------------------------------------

with open(
    SAVE_PATH,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        label_mapping,
        f,
        indent=4
    )

print("\n===================================")
print("Label Mapping Saved Successfully")
print("===================================")

print("\nSaved At:")

print(SAVE_PATH)