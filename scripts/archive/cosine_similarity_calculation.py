""" Weighted cosine similarity calculation between each pair of products
The results are saved for hashing
"""
from scipy.spatial.distance import pdist, squareform
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle

# Load
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
winetales_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/winetales_df.pkl')
with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_vec.pkl', 'rb') as handle:
    [weight_vec] = pickle.load(handle)
total_len = winetales_df.shape[0]
_, desc_temp, desc_idx_train, desc_idx_temp = train_test_split(range(total_len), range(total_len), test_size=0.20, random_state=0)
_, _, desc_idx_val, desc_idx_test = train_test_split(desc_temp,desc_idx_temp,test_size = 0.5, random_state=0)
desc_idx_train.extend(desc_idx_val)

# Calculation
winetales_cos_dist = squareform(pdist(winetales_df.to_numpy(), 'cosine', w=weight_vec))

# Save
with open('C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/winetales_cos_dist_v2.pkl', 'wb') as f:
    pickle.dump([winetales_cos_dist], f)
winetales_cos_dist_df = pd.DataFrame(winetales_cos_dist)
winetales_cos_dist_df.to_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/winetales_cos_dist_df_v2.pkl')





