# Q1. Write a python program to read a MS excel data file using 'pandas' assume that there are 3 columns & 100 rows. hence create a matrix of order 4*4 for the highest 16 elements of the data file.
#Creating new data for the Processing
import pandas as pd
import random
data = random.sample(range(1, 1001), 300) # Generate 300 unique random numbers from 1 to 1000
# Split into 3 columns (100 rows each column)
col1 = data[:100]
col2 = data[100:200]
col3 = data[200:300]
# Create DataFrame
df = pd.DataFrame({
"Column1": col1,
"Column2": col2,
"Column3": col3
})
df.to_excel("data.xlsx", index=False) # Save to Excel
print("Excel file 'data.xlsx' created successfully with 3 columns and 300 rows.")
df.head()
df_read = pd.read_excel('data.xlsx') # Read the Excel file
flattened_data = df_read.values.flatten() # Flatten the DataFrame to a single series
highest_16_values = np.sort(flattened_data)[-16:] # Get the highest 16 values
print("The highest 16 values are:")
print(highest_16_values)