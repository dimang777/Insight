import pandas as pd

# histogram of the features

# find missing data for sugar, sweetness, style1, style2, variety versus total data


# histogram of alcohol
# histogram of sugar
# histogram of brand
# histogram of variety
# histogram of price
# histogram of country
# sub-histogram of city with in a country

# rw_df = pd.read_excel('tmp.xlsx', index_col=0)

rw_df = pd.read_excel('RW_data_wofeaturedwines_UTF-8.xlsx')

data_count = rw_df.count(axis = 0) 

hist = rw_df.hist(column = 'Sugar', bins = 20)

hist = rw_df.hist(column = 'Price', bins = 20)

hist = rw_df.hist(column = 'Alcohol', bins = 20)



listof_brandcounts = rw_df['Brand'].value_counts()
numof_brands = len(listof_brandcounts)
hist = rw_df['Brand'].value_counts().plot(kind='bar')

listof_countrycounts = rw_df['Madein_country'].value_counts()
numofcountries = len(listof_countrycounts)
hist = rw_df['Madein_country'].value_counts().plot(kind='bar')

listof_style1 = rw_df['Style1'].value_counts()
numofstyle1 = len(listof_style1)
hist = rw_df['Style1'].value_counts().plot(kind='bar')

listof_style2 = rw_df['Style2'].value_counts()
numofstyle1 = len(listof_style2)
hist = rw_df['Style2'].value_counts().plot(kind='bar')

listof_sweetness = rw_df['Sweetness'].value_counts()
numofsweetness = len(listof_sweetness)
hist = rw_df['Sweetness'].value_counts().plot(kind='bar')

listof_variety = rw_df['Variety'].value_counts()
numofvariety = len(listof_variety)
hist = rw_df['Variety'].value_counts().plot(kind='bar')

# Use top ten countries and plot cities
rw_df_city = []
listof_city = []
numofcity = []

for count in range(10):
    is_city =  rw_df['Madein_country']==listof_countrycounts.keys()[count]
    rw_df_city.append(rw_df[is_city])
    print(rw_df_city[count].shape)
    
    listof_city.append(rw_df_city[count]['Madein_city'].value_counts())
    numofcity.append(len(listof_city[count]))
    hist = rw_df_city[count]['Madein_city'].value_counts().plot(kind='bar')


# drop nans
    
rw_df_bool = rw_df.notnull()
full_rows_bool = rw_df_bool[rw_df.columns[0]]
sum(full_rows_bool)
sum(rw_df_bool[rw_df.columns[6]])
full_rows_bool = full_rows_bool & rw_df_bool[rw_df.columns[3]]
sum(full_rows_bool)
sum(full_rows_bool & rw_df_bool[rw_df.columns[6]])
full_rows_bool = full_rows_bool & rw_df_bool[rw_df.columns[6]]


for idx in range(1,rw_df.shape[1]-2): # number of columns
    full_rows_bool = full_rows_bool & rw_df_bool[rw_df.columns[idx]]
    
sum(full_rows_bool) # Total 2890

rw_df_full_clean_v1 = rw_df[full_rows_bool].drop(columns=['Featured_wines', 'Recomm_foods'])

rw_df_full_clean_v1.shape

# rw_df_full_clean_v1.to_excel('rw_df_full_clean_v1.xlsx', index=False)


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

