import pandas as pd

train = pd.read_csv("datasets/emotion_dataset/raw/train.csv")
val = pd.read_csv("datasets/emotion_dataset/raw/validation.csv")
test = pd.read_csv("datasets/emotion_dataset/raw/test.csv")
print("="*50)
print("TRAIN")
print(train.head())

print("="*50)
print(train.info())

print("="*50)
print(train["label"].value_counts())

print("="*50)
print(train.isnull().sum())

print("="*50)
print(train.duplicated().sum())