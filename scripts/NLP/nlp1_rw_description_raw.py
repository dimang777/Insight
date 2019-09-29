import pandas as pd
import numpy as np


rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v2.xlsx')

rw_desc_df_raw = rw_df['Description']
rw_mod_desc = rw_df['Description']


rw_df.columns

cate_order = ['Madein_city', 'Madein_country', 'Variety', 'Brand']


for idx in range(rw_df.shape[0]):
    if np.mod(idx, 1000) == 0:
        print(idx)
    str_to_attach = ''
    for category in cate_order:
        str_to_attach = str_to_attach + str(rw_df.loc[idx, category]) + ' '

    rw_mod_desc[idx] = str_to_attach + str(rw_desc_df_raw.loc[idx])


rw_desc_df_raw.to_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_desc_df_raw.xlsx', index=False)
rw_mod_desc.to_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_mod_desc.xlsx', index=False)





