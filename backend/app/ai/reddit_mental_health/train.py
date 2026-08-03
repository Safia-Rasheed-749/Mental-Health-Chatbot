import pandas as pd

print("=" * 60)
print("Reddit Mental Health Training Pipeline")
print("=" * 60)

df = pd.read_csv(
    "datasets/reddit_mental_health/processed/train_processed.csv"
)

print("\nLoading Dataset...\n")

print(df.head())

print("\nTotal Samples :", len(df))

print("\nColumns")
print(df.columns.tolist())

print("\nSubreddits")
print(df["subreddit"].value_counts())

print("\nDataset Ready")

print("\nNext Step (Later)")

print("""
Load Tokenizer
↓

Load Language Model

↓

Tokenize Posts

↓

Fine-tune

↓

Save Model
""")