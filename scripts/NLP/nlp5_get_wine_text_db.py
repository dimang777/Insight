import pandas as pd
import numpy as np
import math


kag_folder = 'C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/'
kag_df_raw = pd.read_excel(kag_folder+ 'winemag-data-130k-v2.xlsx')

kag_df_raw.columns
kag_df_essential = kag_df_raw[['country', 'description', 'points', 'province',\
                               'region_1', 'variety', 'winery']]
kag_df_description = kag_df_raw['description']
kag_df_mod_desc = kag_df_raw['description']

cate_order_template = ['region_1', 'province', 'country', 'variety', 'winery']

flag = False
for idx in range(kag_df_raw.shape[0]):
    if np.mod(idx, 1000) == 0:
        print(idx)

    str_to_attach = ''
    if type(kag_df_essential.loc[idx, 'region_1']) == str:
        # region and province can be same. Do not include region in that case
        if kag_df_essential.loc[idx, 'region_1'].lstrip().rstrip().lower() == \
            kag_df_essential.loc[idx, 'province'].lstrip().rstrip().lower():
            cate_order = cate_order_template[1:]
            flag = True
        else:
            cate_order = cate_order_template
    elif math.isnan(kag_df_essential.loc[idx, 'region_1']): # exception
            cate_order = cate_order_template[1:]
            flag = True

    else:
        cate_order = cate_order_template
        flag = True

    for category in cate_order:
        str_to_attach = str_to_attach + str(kag_df_essential.loc[idx, category]) + ' '

    if flag:
        # Print corrected version here if needed
        flag = False

    kag_df_mod_desc[idx] = str_to_attach + str(kag_df_description.loc[idx])

kag_df_essential.to_excel(kag_folder + 'kag_df_essential.xlsx')
kag_df_description.to_excel(kag_folder + 'kag_df_description.xlsx')
kag_df_mod_desc.to_excel(kag_folder + 'kag_df_mod_desc.xlsx')




