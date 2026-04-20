import pandas as pd
# Load the dataset
data = pd.read_csv("dataset.csv", header=None)
row_sum = data.sum(axis=1)
row_avg = data.mean(axis=1)
data['Row_Sum'] = row_sum
data['Row_Avg'] = row_avg
col_sum = data.sum(axis=0)
col_avg = data.mean(axis=0)
data.loc['Col_Sum'] = col_sum
data.loc['Col_Avg'] = col_avg
data.to_csv("dataset_with_sums_and_averages.csv", index=True,header=True) 
print(data)