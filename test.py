import pandas as pd

data_set = pd.read_csv('./config_mixed.csv')

print(data_set.at[1, 'Notebooks'])