import pandas as pd

# Task 1
# Set the file path
file_path = 'stock_data.csv'
# Load the data into a pandas dataframe
df = pd.read_csv(file_path)
# Filter out data will use in this task
df_filtered = df[['date', 'close', 'Name']]
# Print out first five row
# print(df_filtered.head())

# Task 2
# Get set of all names in the data and sort
stock_names = df['Name'].unique()
stock_names.sort()

# Counting the number of unique stock names
number_of_stocks = len(stock_names)

# Listing the first and last 5 names
first_5_names = stock_names[:5]
last_5_names = stock_names[-5:]






