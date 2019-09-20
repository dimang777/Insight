import pandas as pd
import numpy as np
import itertools

# features to use
# price
# alcohol
# sugar
# sweetness
# style1
# style2
# variety

# NOT USED
# LCBO ID
# name
# description
# size
# city
# country
# brand
# featured wines
# recommended food

# rw_df_full_clean_v1
# columns: 'LCBO_id', 'Price', 'Name', 'Description', 'Size', 'Alcohol',
# 'Madein_city', 'Madein_country', 'Brand', 'Sugar', 'Sweetness',
# 'Style1', 'Style2', 'Variety'
rw_df_full_clean_v1 = pd.read_excel('rw_df_full_clean_v1.xlsx')

# Features used: 'Price', 'Alcohol', 'Sugar', 'Sweetness', 'Style1', 'Style2', 'Variety'
# LCBO_id is used as index
rw_df_full_clean_v1.columns
rw_df_mvp = rw_df_full_clean_v1.drop(columns = ['Description', 'Size', 'Madein_city', 'Madein_country', 'Brand'])
rw_df_mvp.set_index('LCBO_id')


listof_prices = rw_df_mvp['Price'].value_counts()
numof_prices = len(listof_prices)
hist = rw_df_mvp['Price'].value_counts().plot(kind='bar')

listof_sugar = rw_df_mvp['Sugar'].value_counts()
numof_sugar = len(listof_sugar)
hist = rw_df_mvp['Sugar'].value_counts().plot(kind='bar')

listof_alcohol = rw_df_mvp['Alcohol'].value_counts()
numof_alcohol = len(listof_alcohol)
hist = rw_df_mvp['Alcohol'].value_counts().plot(kind='bar')

listof_sweetness = rw_df_mvp['Sweetness'].value_counts()
numofsweetness = len(listof_sweetness)
hist = rw_df_mvp['Sweetness'].value_counts().plot(kind='bar')

listof_style1 = rw_df_mvp['Style1'].value_counts()
numofstyle1 = len(listof_style1)
hist = rw_df_mvp['Style1'].value_counts().plot(kind='bar')

listof_style2 = rw_df_mvp['Style2'].value_counts()
numofstyle1 = len(listof_style2)
hist = rw_df_mvp['Style2'].value_counts().plot(kind='bar')

listof_variety = rw_df_mvp['Variety'].value_counts()
numofvariety = len(listof_variety)
hist = rw_df_mvp['Variety'].value_counts().plot(kind='bar')

# rw_df_mvp.to_excel('rw_df_mvp.xlsx', index=False)

