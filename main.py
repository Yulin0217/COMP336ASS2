import pandas as pd

# Task 1
# Set the file path
file_path = 'stock_data.csv'
# Load the data into a pandas dataframe
df = pd.read_csv(file_path)
# Filter out data will use in this task
df_filtered = df[['date', 'close', 'Name']]


# Display results
# print("Task1:")
# print("First five rows:", df_filtered.head())

# Task 2
# Get set of all names in the data and sort
stock_names = df['Name'].unique()
stock_names.sort()
# Count the number of unique stock names
number_of_stocks = len(stock_names)

# List the first and last 5 names
first_5_names = stock_names[:5]
last_5_names = stock_names[-5:]

# Display results
# print("Task2:")
# print("Number of stocks:", number_of_stocks)
# print("First five names:", first_5_names)
# print("Last five names:",last_5_names)

# Task 3
# Assuming df is the DataFrame with the stock data
df['date'] = pd.to_datetime(df['date'])  # Convert 'date' column to datetime

# Define the date range
start_date = pd.Timestamp('2014-07-01')
end_date = pd.Timestamp('2017-06-30')

# Group by stock name to find the first and last date for each stock
grouped = df.groupby('Name')['date'].agg(['min', 'max'])

# Identify stocks to remove
stocks_to_remove = grouped[(grouped['min'] > start_date) | (grouped['max'] < end_date)].index
removed_stock = stocks_to_remove.tolist()

# Remove these stocks from the dataset
df_filtered = df[~df['Name'].isin(stocks_to_remove)]

# Find the remaining stock names
remaining_stocks = df_filtered['Name'].unique()

# Calculate the number of remaining stocks
how_many_left = len(remaining_stocks)

print("Task3:")
print("Removed stocks:", removed_stock)
print("Left stocks:", how_many_left)






