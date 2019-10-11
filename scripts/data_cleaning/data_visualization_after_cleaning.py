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

rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
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

rw_df_mvp_v2 = rw_df
print(rw_df_mvp_v2.shape)

# Visulization after the cleaning
listof_prices = rw_df_mvp_v2['Price'].value_counts()
numof_prices = len(listof_prices)
hist = rw_df_mvp_v2['Price'].hist(bins=15)

listof_sugar = rw_df_mvp_v2['Sugar'].value_counts()
numof_sugar = len(listof_sugar)
hist = rw_df_mvp_v2['Sugar'].hist(bins=20)

listof_alcohol = rw_df_mvp_v2['Alcohol'].value_counts()
numof_alcohol = len(listof_alcohol)
hist = rw_df_mvp_v2['Alcohol'].hist(bins=20)

listof_style1 = rw_df_mvp_v2['Style1'].value_counts()
numofstyle1 = len(listof_style1)
hist = rw_df_mvp_v2['Style1'].hist(bins=5)

listof_style2 = rw_df_mvp_v2['Style2'].value_counts()
numofstyle1 = len(listof_style2)
hist = rw_df_mvp_v2['Style2'].hist(bins=5)

listof_variety = rw_df_mvp_v2['Sweetness'].value_counts()
numofvariety = len(listof_variety)
hist = rw_df_mvp_v2['Sweetness'].hist(bins=9)

listof_variety = rw_df_mvp_v2['Variety'].value_counts()
numofvariety = len(listof_variety)
hist = rw_df_mvp_v2['Variety'].value_counts()[:15].plot(kind='bar')
hist = rw_df_mvp_v2['Variety'].hist(bins=9)

