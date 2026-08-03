from datasets import load_dataset

print("Loading Emotion dataset...")

dataset = load_dataset("dair-ai/emotion")

print(dataset)

print(dataset["train"][0])