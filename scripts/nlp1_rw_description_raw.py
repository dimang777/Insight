import pandas as pd


rw_df = pd.read_excel('rw_df_mvp_v2.xlsx')

rw_desc_df_raw_v1 = rw_df[['LCBO_id', 'Description']]

rw_desc_df_raw_v1.to_excel('rw_desc_df_raw_v1.xlsx', index=False)




