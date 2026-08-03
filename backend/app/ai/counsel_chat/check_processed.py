import pandas as pd

df = pd.read_csv(
    "datasets/counsel_chat/processed/train_processed.csv"
)

print("="*60)
print("Processed Counsel Chat Dataset")
print("="*60)

print("\nFirst 5 Rows\n")

print(df.head())

print("\nShape")

print(df.shape)

print("\nColumns")

print(df.columns.tolist())

print("\nMissing Values")

print(df.isnull().sum())

print("\nTopics")

print(df["topic"].value_counts())

print("\nSample Question\n")

print(df.iloc[0]["questionText"])

print("\nSample Therapist Response\n")

print(df.iloc[0]["answerText"])