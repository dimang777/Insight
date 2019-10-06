import pandas as pd
import numpy as np
from nlp2_rw_description_preprocess import remove_punct

rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
rw_prepro_bfr_desc = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')

rw_desc_df_raw = rw_df['Description']

# Processes before attaching to the description AFTER lemmatization
# Madein_city - remove space and combine
# Madein_country - remove space and combine
# Variety - remove spaces first and replace / with space
# Brand - remove all stop words first then attach to the string
# Style1 - okay
# Style2 - remove - and sapce
# Sweetness
# price, alcohol, sugar - changed to categorical data - refer to each function

for idx in range(rw_df.shape[0]):
    if len(str(rw_df.loc[idx, 'Madein_city']).split()) > 1:
        rw_prepro_bfr_desc['Madein_city'][idx] = str(rw_df.loc[idx, 'Madein_city']).replace(' ', '').lower()
    else:
        rw_prepro_bfr_desc['Madein_city'][idx] = str(rw_df.loc[idx, 'Madein_city']).lower()
    print(rw_prepro_bfr_desc.loc[idx, 'Madein_city'])



for idx in range(rw_df.shape[0]):
    if len(str(rw_df.loc[idx, 'Madein_country']).split()) > 1:
        rw_prepro_bfr_desc['Madein_country'][idx] = str(rw_df.loc[idx, 'Madein_country']).replace(' ', '').lower()
    else:
        rw_prepro_bfr_desc['Madein_country'][idx] = str(rw_df.loc[idx, 'Madein_country']).lower()
    print(rw_prepro_bfr_desc.loc[idx, 'Madein_country'])

for idx in range(rw_df.shape[0]):
    str_wo_space = str(rw_df.loc[idx, 'Variety']).replace(' ', '')
    rw_prepro_bfr_desc['Variety'][idx] = str_wo_space.replace('/', ' ').lower()
    print(rw_prepro_bfr_desc['Variety'][idx])

for idx in range(rw_df.shape[0]):
    str_wo_stopwords = remove_punct(rw_df.loc[idx, 'Brand'])
    rw_prepro_bfr_desc['Brand'][idx] = str_wo_stopwords.replace(' ', '').lower()
    print(rw_prepro_bfr_desc['Brand'][idx])

for idx in range(rw_df.shape[0]):
    str_wo_stopwords = remove_punct(rw_df.loc[idx, 'Style2'])
    rw_prepro_bfr_desc['Style2'][idx] = str_wo_stopwords.replace(' ', '').lower()
    print(rw_prepro_bfr_desc['Style2'][idx])

for idx in range(rw_df.shape[0]):
    dash_idx = rw_df['Sweetness'][idx].find('-')
    rw_prepro_bfr_desc['Sweetness'][idx] = rw_df['Sweetness'][idx][dash_idx+1:].strip().replace(' ', '').lower()
    print(rw_prepro_bfr_desc['Sweetness'][idx])

for idx in range(rw_df.shape[0]):
    # Round down to multiples of 5. e.g., 26.5 -> 25; 31 -> 30
    rw_prepro_bfr_desc['Price'][idx] = 'price' + str(int(5*np.floor(rw_df['Price'][idx]/5)))
    print(rw_prepro_bfr_desc['Price'][idx])

for idx in range(rw_df.shape[0]):
    # Round down to multiples of 0.5. e.g., 11.6 -> 11.5; 5.1 -> 5
    # Decimal removed. e.g., 110 -> 11; 105 -> 10.5
    rw_prepro_bfr_desc['Alcohol'][idx] = 'alcohol' + str(int(np.floor(rw_df['Alcohol'][idx]*2)*5))
    print(rw_prepro_bfr_desc['Alcohol'][idx])

for idx in range(rw_df.shape[0]):
    # Round down to multiples of 1. e.g., 11.6 -> 11; 5.1 -> 5
    rw_prepro_bfr_desc['Sugar'][idx] = 'sugar' + str(int(np.floor(rw_df['Sugar'][idx])))
    print(rw_prepro_bfr_desc['Sugar'][idx])

rw_desc_df_raw.to_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_desc_df_raw.xlsx', index=False)
rw_prepro_bfr_desc.to_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_prepro_bfr_desc.xlsx', index=False)



