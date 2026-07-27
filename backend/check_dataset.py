import pandas as pd

df = pd.read_csv("datasets/stress/raw/dreaddit-train.csv")

print("\nColumns:\n")
print(df.columns)

print("\nFirst 5 Rows:\n")
print(df.head())