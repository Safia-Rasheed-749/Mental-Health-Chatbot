"""
=========================================================
Stress Detection Label Encoder
Project : AI Mental Health Chatbot (FYP)

Purpose
1. Create Label Mapping
2. Save Mapping as JSON

Author : Shamsa Akram
=========================================================
"""

import os
import json

# -------------------------------------------------------
# Label Mapping
# -------------------------------------------------------

label_mapping = {
    0: "No Stress",
    1: "Stress"
}

# -------------------------------------------------------
# Save Location
# -------------------------------------------------------

MODEL_PATH = os.path.join(
    os.getcwd(),
    "models",
    "stress"
)

os.makedirs(MODEL_PATH, exist_ok=True)

SAVE_PATH = os.path.join(
    MODEL_PATH,
    "label_mapping.json"
)

# -------------------------------------------------------
# Save JSON
# -------------------------------------------------------

with open(
    SAVE_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        label_mapping,
        file,
        indent=4
    )

# -------------------------------------------------------
# Print Labels
# -------------------------------------------------------

print("\n========== Stress Labels ==========\n")

for key, value in label_mapping.items():

    print(f"{key} --> {value}")

print("\n===================================")
print("Label Mapping Saved Successfully")
print("===================================")

print("\nSaved At:")

print(SAVE_PATH)