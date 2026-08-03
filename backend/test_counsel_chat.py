from datasets import load_dataset

print("Loading Counsel Chat Dataset...")

dataset = load_dataset("nbertagnolli/counsel-chat")

print(dataset)

print("\nFirst Sample:\n")
print(dataset["train"][0])