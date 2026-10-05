import pandas as pd

df = pd.read_csv("datasets/depression/raw/depression_dataset_reddit_cleaned.csv")

print("\nColumns:\n")
print(df.columns)

print("\nShape:")
print(df.shape)

print("\nFirst 5 Rows:\n")
print(df.head())

print("\nMissing Values:\n")
print(df.isnull().sum())