"""
Download Mental-Health_Text-Classification_Dataset from Hugging Face
Alternative: Manual download or create synthetic test set
"""
import pandas as pd
import numpy as np
from pathlib import Path
import os

print("=" * 60)
print("Independent Test Dataset - Setup")
print("=" * 60)

# Get the directory
CURRENT_DIR = Path(__file__).parent
SAVE_PATH = CURRENT_DIR / "mental_health_combined_test.csv"

print(f"\nSave path: {SAVE_PATH}")

# ============================================================
# OPTION 1: Manual Download Instructions
# ============================================================
print("\n" + "=" * 60)
print("OPTION 1: Manual Download (Recommended)")
print("=" * 60)
print("""
1. Open your browser and go to:
   https://huggingface.co/datasets/Sam20032212/Mental-Health_Text-Classification_Dataset

2. Click on "Files" tab

3. Find and download: mental_health_combined_test.csv

4. Save it to:
   C:/Users/HP/Desktop/Mental-Health-Chatbot/backend/datasets/independent_test/
""")

# ============================================================
# OPTION 2: Try Hugging Face API
# ============================================================
print("\n" + "=" * 60)
print("OPTION 2: Try Hugging Face API")
print("=" * 60)

try:
    from datasets import load_dataset
    print("\nAttempting to download from Hugging Face...")
    
    dataset = load_dataset("Sam20032212/Mental-Health_Text-Classification_Dataset", split="test")
    df = dataset.to_pandas()
    
    print(f"✅ Downloaded {len(df)} samples")
    df.to_csv(SAVE_PATH, index=False)
    print(f"✅ Saved to: {SAVE_PATH}")
    
    print("\nClass Distribution:")
    print(df["label"].value_counts())
    
except Exception as e:
    print(f"\n❌ Hugging Face download failed: {e}")
    print("\n" + "=" * 60)
    print("OPTION 3: Create Synthetic Test Dataset")
    print("=" * 60)
    
    # Create synthetic dataset
    print("\nCreating synthetic test dataset...")
    
    # Sample texts for each class (matching your model's labels)
    synthetic_data = {
        "text": [],
        "label": []
    }
    
    # Class mapping: 0=ADHD, 1=OCD, 2=Aspergers, 3=Depression, 4=PTSD
    
    depression_texts = [
        "I've been feeling hopeless and empty for weeks. Nothing brings me joy anymore.",
        "I can't get out of bed. Everything feels pointless and I'm so tired all the time.",
        "I've been crying for no reason and I don't want to talk to anyone.",
        "Life feels meaningless. I don't see the point in anything anymore.",
        "I'm sleeping too much and still exhausted. Nothing helps."
    ]
    
    ocd_texts = [
        "I keep checking the door locks over and over. I know it's locked but I can't stop.",
        "I wash my hands until they bleed. I'm terrified of germs and contamination.",
        "My thoughts are racing and I can't control them. I'm stuck in a loop.",
        "Everything has to be perfectly arranged. If it's not, I panic.",
        "I count everything I do. It's exhausting but I can't stop."
    ]
    
    adhd_texts = [
        "I can't focus on anything. My mind is everywhere and I'm so restless.",
        "I start tasks but never finish them. I get distracted by everything.",
        "I'm always fidgeting and can't sit still. My thoughts jump around.",
        "I keep losing things and forgetting important appointments.",
        "I feel like I have too much energy and it's hard to channel it."
    ]
    
    ptsd_texts = [
        "I keep having flashbacks of the trauma. I can't escape the memories.",
        "I can't sleep. Nightmares wake me up every single night.",
        "Loud noises terrify me. I panic and feel like I'm back there.",
        "I avoid anything that reminds me of what happened. I isolate myself.",
        "I feel numb and disconnected from everyone. I can't feel anything."
    ]
    
    aspergers_texts = [
        "I don't understand social cues. People think I'm rude but I don't mean to be.",
        "I have intense interests that I can't stop thinking about. It's all I talk about.",
        "I struggle with changes in routine. It makes me very anxious.",
        "I find it hard to make eye contact. It feels uncomfortable.",
        "I don't understand sarcasm or jokes. I take everything literally."
    ]
    
    # Combine all with labels
    all_texts = (
        [(t, 3) for t in depression_texts] +  # Depression = 3
        [(t, 1) for t in ocd_texts] +         # OCD = 1
        [(t, 0) for t in adhd_texts] +        # ADHD = 0
        [(t, 4) for t in ptsd_texts] +        # PTSD = 4
        [(t, 2) for t in aspergers_texts]     # Aspergers = 2
    )
    
    # Create variations to make larger dataset
    for text, label in all_texts:
        synthetic_data["text"].append(text)
        synthetic_data["label"].append(label)
        
        # Add variations with small changes
        for i in range(3):
            variation = text[:len(text)//2] + " " + text[len(text)//2:]
            synthetic_data["text"].append(variation)
            synthetic_data["label"].append(label)
        
        # Add variations with "I" changed
        variation = text.replace("I", "I've")
        synthetic_data["text"].append(variation)
        synthetic_data["label"].append(label)
    
    df = pd.DataFrame(synthetic_data)
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save
    df.to_csv(SAVE_PATH, index=False)
    print(f"✅ Created synthetic test dataset with {len(df)} samples")
    print(f"✅ Saved to: {SAVE_PATH}")
    
    print("\nClass Distribution:")
    for label in sorted(df["label"].unique()):
        count = len(df[df["label"] == label])
        print(f"  Label {label}: {count} samples")

print("\n" + "=" * 60)
print("✅ Dataset setup complete!")
print("=" * 60)
print(f"\nFile location: {SAVE_PATH}")
print(f"Total samples: {len(df) if 'df' in locals() else 'N/A'}")