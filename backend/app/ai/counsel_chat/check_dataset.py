import pandas as pd

df = pd.read_csv("datasets/counsel_chat/raw/train.csv")

print("=" * 60)
print("Counsel Chat Dataset")
print("=" * 60)

print("\nFirst 5 Rows\n")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nTopics")
print(df["topic"].value_counts())