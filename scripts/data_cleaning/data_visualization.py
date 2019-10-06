""" This code visualizes the initial data scraped"""
import pandas as pd

# features to use
# LCBO ID
# Price
# Name
# Description
# Size
# Alcohol
# Madein_city
# Madein_country
# Brand
# Sugar
# Sweetness - should be removed due to redundancy and occasional inaccuracy - i.e., sugar can be used to derive this
# Style1
# Style2
# Variety
# URL
# Pic_src

# NOT USED

# Featured_wines
# Recomm_foods

rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_v3_pic_and_url.xlsx')
rw_df.columns
# Remove rows with missing values
Vars_to_keep = ['LCBO_id',
'Price',
'Name',
'Description',
'Size',
'Alcohol',
'Madein_city',
'Madein_country',
'Brand',
'Sugar',
'Sweetness',
'Style1',
'Style2',
'Variety',
'URL',
'Pic_src']

# Generate a list of boolean values to select rows with full data
rw_df_bool = rw_df.notnull()
full_rows_bool = rw_df_bool[Vars_to_keep[0]]

for idx in range(1,len(Vars_to_keep)): # number of columns to keep
    full_rows_bool = full_rows_bool & rw_df_bool[Vars_to_keep[idx]]

sum(full_rows_bool) # Total 2890

rw_df_mvp_v2 = rw_df.drop(columns=['Featured_wines', 'Recomm_foods'])[full_rows_bool]
print(rw_df_mvp_v2.shape)

# Visulization after the cleaning
listof_prices = rw_df_mvp_v2['Price'].value_counts()
numof_prices = len(listof_prices)
hist = rw_df_mvp_v2['Price'].value_counts().plot(kind='bar')

listof_sugar = rw_df_mvp_v2['Sugar'].value_counts()
numof_sugar = len(listof_sugar)
hist = rw_df_mvp_v2['Sugar'].value_counts().plot(kind='bar')

listof_alcohol = rw_df_mvp_v2['Alcohol'].value_counts()
numof_alcohol = len(listof_alcohol)
hist = rw_df_mvp_v2['Alcohol'].value_counts().plot(kind='bar')

listof_style1 = rw_df_mvp_v2['Style1'].value_counts()
numofstyle1 = len(listof_style1)
hist = rw_df_mvp_v2['Style1'].value_counts().plot(kind='bar')

listof_style2 = rw_df_mvp_v2['Style2'].value_counts()
numofstyle1 = len(listof_style2)
hist = rw_df_mvp_v2['Style2'].value_counts().plot(kind='bar')

listof_variety = rw_df_mvp_v2['Variety'].value_counts()
numofvariety = len(listof_variety)
hist = rw_df_mvp_v2['Variety'].value_counts().plot(kind='bar')

rw_df_mvp_v2.to_excel('rw_df_mvp_v2.xlsx', index=False)

rw_df_mvp_v2['URL'][1]
