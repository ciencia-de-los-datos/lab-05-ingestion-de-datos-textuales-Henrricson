import pandas as pd

train_dataset = pd.read_csv("train_dataset.csv")
print(train_dataset["sentiment"].value_counts())
counts = train_dataset["sentiment"].value_counts()
