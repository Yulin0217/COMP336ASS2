import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Task 1
# Set the file path
file_path = 'stock_data.csv'
# Load the data into a pandas dataframe
df = pd.read_csv(file_path)
# Filter out data that requested
after_remove = df[['date', 'close', 'Name']]
# Display results
# print("Task1:")
# print("First five rows:\n", after_remove.head())

# Task 2
# Get set of stocks names then sort
stock_names = df['Name'].unique()
stock_names.sort()
# Count the number of unique stock names
number_of_stocks = len(stock_names)

# List the first and last five stocks names
first_5_names = stock_names[:5]
last_5_names = stock_names[-5:]

# Display results
# print("Task2:")
# print("Number of stocks:", number_of_stocks)
# print("First five names:", first_5_names)
# print("Last five names:",last_5_names)

# Task 3
# Used resource from: https://stackoverflow.com/questions/29370057/select-dataframe-rows-between-two-dates
#                     https://stackoverflow.com/questions/50459602/how-to-select-dataframe-rows-between-two-datetimes
# Convert 'date' column (String) to datetime64[ns] format, because it will be necessary to compare if choose to use Timestamp
df['date'] = pd.to_datetime(df['date'])

# Set the start and end timestamp prepare for filter
start_date = pd.Timestamp('2014-07-01')
end_date = pd.Timestamp('2017-06-30')
# Used resource from: https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.core.groupby.DataFrameGroupBy.agg.html
#                     https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html
# Group by stock name and use aggregations to find the first and last date for each stock
grouped_date = df.groupby('Name')['date'].agg(['min', 'max'])

# Get stocks that need to be removed
# The boolean mask could help to select the stocks we need
bool_mask = (grouped_date['min'] > start_date) | (grouped_date['max'] < end_date)
stocks_to_remove = grouped_date[bool_mask].index
# Change index to list to prepare for better a look when print
removed_stock = stocks_to_remove.tolist()

# Remove these stocks from the dataset
# Used resource from https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isin.html
# Copy from the website above:  To check if values is not in the DataFrame, use the ~ operator:
after_remove = df[~df['Name'].isin(stocks_to_remove)]

# Find the remaining stock names
remaining_stocks = after_remove['Name'].unique()

# Calculate the number of remaining stocks
how_many_left = len(remaining_stocks)

# Display results
# print("Task3:")
# print("Removed stocks:", removed_stock)
# print("Left stocks:", how_many_left)

# Task 4
# Get the number of stocks of each day
stocks_counts_of_each_day = after_remove.groupby('date').size()
# print(stocks_counts_of_each_day)

# Used resource from: https://datascience.stackexchange.com/questions/58546/valueerror-the-truth-value-of-a-dataframe-is-ambiguous-use-a-empty-a-bool
#                     https://pandas.pydata.org/docs/reference/api/pandas.Series.html
#                     https://sparkbyexamples.com/pandas/pandas-select-dataframe-rows-between-two-dates/
#                     https://stackoverflow.com/questions/38376938/sort-a-pandas-dataframe-based-on-datetime-field
# The day that have the same number of stocks as the nuber of remaining stocks is the day we want, then sort
common_dates = stocks_counts_of_each_day[stocks_counts_of_each_day == how_many_left].index.sort_values()

# Get the series for common_dates
common_dates_series = pd.Series(common_dates)
# Remove dates before 1st July 2014 or after 30th June 2017
bool_mask_task4 = (common_dates_series >= start_date) & (common_dates_series <= end_date)
task_4_filtered_dates = common_dates_series[bool_mask_task4]

# Count number of dates left
numbers_of_dates_left = len(task_4_filtered_dates)

# Get the first and last five dates
first_5_dates = task_4_filtered_dates.head(5)
last_5_dates = task_4_filtered_dates.tail(5)

# Display results
# print("Task4:")
# print("Numbers of dates left:", numbers_of_dates_left)
# print("\nFirst five dates: \n", first_5_dates)
# print("\nLast five dates: \n", last_5_dates)

# Task 5
# Filter out stocks that met two conditions:
# 1.remaining stocks in task 3,
# 2. the stocks with date that has been filtered in task 4
task_5_filtered_df = df[(df['Name'].isin(remaining_stocks)) & (df['date'].isin(task_4_filtered_dates))]

# Use pivot to creat a df that use date as index (each row is a different date), column as each stocks' close price
# Used resource from https://pandas.pydata.org/docs/user_guide/reshaping.html#pivot
task_5_df = task_5_filtered_df.pivot(index='date', columns='Name', values='close')

# Display results
# print("Task5:")
# print(task_5_df)

# Task 6
# Used resource from: https://www.codingfinance.com/post/2018-04-03-calc-returns-py/
#                     https://stackoverflow.com/questions/20000726/calculate-daily-returns-with-pandas-dataframe
#                     https://stackoverflow.com/questions/63747960/what-is-the-best-way-to-calculate-the-return-in-a-pandas-dataframe
#                     https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html#pandas.DataFrame.pct_change

# Computes the fractional change from the immediately previous row use pct_change()
returns_df = task_5_df.pct_change()
# Drop first row which is empty
returns_df = returns_df.drop(returns_df.index[0])

# Display results
# print("\nTask6:")
# print(returns_df)

# Task 7
# Used resource from: https://stackoverflow.com/questions/49520474/computing-first-principal-component-of-sklearns-pca
# Initialize a PCA instance
pca = PCA()
# Fit PCA model with returns
pca.fit(returns_df)
# Get top five principal components
top_five_components = pca.components_[:5]

# Display results
# print("\nTask7:")
# print("Top five principal components: \n", top_five_components)

# Task 8
# Used resource from: https://stackoverflow.com/questions/57293716/sklearn-pca-explained-variance-and-explained-variance-ratio-difference
#                     https://www.baeldung.com/cs/pca
#                     https://mikulskibartosz.name/pca-how-to-choose-the-number-of-components
#                     https://stackoverflow.com/questions/55678708/interpretation-of-pca-explained-variance-ratio
#                     https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
#                     https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axvline.html#matplotlib.pyplot.axvline
#                     https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D.set_marker
#                     https://matplotlib.org/stable/gallery/text_labels_and_annotations/legend_demo.html#sphx-glr-gallery-text-labels-and-annotations-legend-demo-py

# Get explained variance ratios
explained_variance_ratios = pca.explained_variance_ratio_

# Calculate the percentage of variance explained by the first principal component
first_variance = explained_variance_ratios[0] * 100

# Plot the first 20 explained variance ratios
plt.plot(range(1, 21), explained_variance_ratios[:20], marker='o')
plt.title('Explained Variance Ratios (20 Principal Components)')
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')

# By direct observation, before this point each new principal component significantly increases its explanation of the total variance.
# After this point each new principal component gradually decreases its contribution to the variance.
# So set the elbow point as 5 principal components
elbow_point = 5
plt.axvline(x=elbow_point, color='green', ls='-', label='Elbow Point')
plt.legend()
plt.show()

# Calculate how many principal components explain 90% of the variance
# Used resource from: https://www.baeldung.com/cs/pca
#                     https://mikulskibartosz.name/pca-how-to-choose-the-number-of-components
cumsum = np.cumsum(pca.explained_variance_ratio_)
number_of_components = np.argmax(cumsum >= 0.90) + 1
# Calculate first 5 principal components explain what percentage of variance
variance_explained_first_five = cumsum[4] * 100

# Display results
print("\nTask8:")
print('Percentage of variance explained by the first principal components is: ', first_variance)
print('How many principal components explain 90% of the variance', number_of_components)
print('First 5 principal components explain ', variance_explained_first_five, '% of the variance.')
