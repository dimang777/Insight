import pandas as pd
import numpy as np


kag_folder = 'C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/'
kag_df_raw = pd.read_excel(kag_folder+ 'winemag-data-130k-v2.xlsx')

kag_df_raw.columns
kag_df_essential = kag_df_raw[['country', 'description', 'points', 'province',\
                               'region_1', 'variety', 'winery']]
kag_df_description = kag_df_raw['description']
kag_df_mod_desc = kag_df_raw['description']

cate_order = ['region_1', 'province', 'country', 'variety', 'winery']


for idx in range(kag_df_raw.shape[0]):
    if np.mod(idx, 1000) == 0:
        print(idx)
    str_to_attach = ''
    for category in cate_order:
        str_to_attach = str_to_attach + str(kag_df_essential.loc[idx, category]) + ' '

    kag_df_mod_desc[idx] = str_to_attach + str(kag_df_description.loc[idx])

kag_df_essential.to_excel(kag_folder + 'kag_df_essential.xlsx')
kag_df_description.to_excel(kag_folder + 'kag_df_description.xlsx')
kag_df_mod_desc.to_excel(kag_folder + 'kag_df_mod_desc.xlsx')




