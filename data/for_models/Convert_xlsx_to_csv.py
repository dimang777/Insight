import pandas as pd
data_xls = pd.read_excel('rw_df_mvp_v3.xlsx', index_col=0)
data_xls.to_csv('rw_df_mvp_v3.csv', encoding='utf-8', index=False)

data_csv = pd.read_csv('rw_df_mvp_v3.csv')
data_csv.iloc[0]
