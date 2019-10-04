import pandas as pd
import numpy as np

rw_df_mvp_v3 = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v2.xlsx')
Remove_list = [11, 208, 229, 235, 252, 420, 473, 544, 620, 649, 706, 807, \
               952, 963, 987, 1073, \
 1077, 1091, 1145, 1146, 1150, 1151, 1189, 1391, 1398, 1438, 1492, 1576, \
     1603, 1685, 1687, 1781, 1860, 1969, 2023, 2034, 2042, 2046, 2294, \
         2303, 2343, 2421, 2444, 2476, 2516, 2595, 2606, 2696, 2861]

rw_df_mvp_v3 = rw_df_mvp_v3.drop(Remove_list)
len(rw_df_mvp_v3)
rw_df_mvp_v3.to_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')


# Main code
duplicate_idx = [i for i, x in enumerate(rw_df_mvp_v3.duplicated(subset = 'Name',keep=False)) if x]

order = 14

for order in range(14, len(duplicate_idx)):
    Size_1500_bool = rw_df_mvp_v3['Size'][rw_df_mvp_v3['Name'] == rw_df_mvp_v3['Name'][duplicate_idx[order]]]
    print(Size_1500_bool)
# Main code end



# =============================================================================
# 
# 
# 
# 
# dup_bool = rw_df_mvp_v3['Name'] == rw_df_mvp_v3['Name'][duplicate_idx[0]]
# dup_bool[dup_bool == True].index
# 
# 
# 
# to_delete_idx = (Size_1500_bool[Size_1500_bool == 1500]).index[0]
# 
# 
# 
# rw_df_mvp_v3.loc[543, :]
# rw_df_mvp_v3.loc[544, :]
# 
# 
# duplicate_idx = [i for i, x in enumerate(rw_df_mvp_v3['Name'].duplicated()) if x]
# 
# sum(rw_df_mvp_v3['Name'] == rw_df_mvp_v3['Name'][duplicate_idx[0]])
# print(duplicate_idx[0])
# 
#
# 
# =============================================================================
