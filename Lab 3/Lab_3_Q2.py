# Write a Pandas program to create a DataFrame from the clipboard (data from an Excel spreadsheet or a Google Sheet). Hence, print a summary of the basic information about the specified DataFrame and its data. Now, interchange column 1 and column 2 and create the Data frame.

import pandas as pd
#csv_file_link: https://www.kaggle.com/datasets/redwankarimsony/heart-disease-data
# Reading csv data
df = pd.read_csv('/content/heart_disease_uci.csv')
print("Original DataFrame:\n", df.head())
# Summary information
print("\nSummary Information:")
print(df.info())
df.describe() ## summarisation of the numerical data
df.describe(include='object')## To get the summary of the Categorical columns
cols = list(df.columns)

# Swap the first two columns (index 0 and 1)
cols[0], cols[1] = cols[1], cols[0]
# Create a new DataFrame with the columns in the new order
df_swapped = df[cols]
print("DataFrame with swapped columns:")
print(df_swapped.head())