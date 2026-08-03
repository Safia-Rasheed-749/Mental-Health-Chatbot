from datasets import load_dataset

print("Loading Reddit Mental Health Dataset...")

dataset = load_dataset("solomonk/reddit_mental_health_posts")

print(dataset)

print("\nFirst Sample:\n")

print(dataset["train"][0])