from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.model_selection import train_test_split

rw_df_ohe_numeric = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_df_ohe.pkl')
rw_df_ohe_numeric = rw_df_ohe_numeric.drop(['LCBO_id', 'Name', 'Description', 'Pic_src', 'URL', 'Unnamed: 0'], axis = 1)
rw_df_ohe_numeric.columns


Dist_cos = squareform(pdist(rw_df_ohe_numeric.to_numpy(), 'cosine'))
Dist_cos.shape
total_len = rw_df_ohe_numeric.shape[0]

# Divide into train, validation, and test sets
_, desc_temp, desc_idx_train, desc_idx_temp = train_test_split(range(total_len), range(total_len), test_size=0.20, random_state=0)
_, _, desc_idx_val, desc_idx_test = train_test_split(desc_temp,desc_idx_temp,test_size = 0.5, random_state=0)

desc_idx_test.extend(desc_idx_val)
len(desc_idx_test)

Dist_cos_df = pd.DataFrame(Dist_cos)

best_idx = []
for idx in range(200,400):
    best_idx.append(Dist_cos_df[idx].sort_values().index[1])
    print(Dist_cos_df[idx].sort_values().index[1])


len(Dist_cos_df[idx])
best_idx.append(Dist_cos_df[0].sort_values().index[1])



Dist_cos = cosine_similarity(rw_df_ohe_numeric.to_numpy())

Dist_cos.shape

Dist_cos_df = pd.DataFrame(Dist_cos)

best_idx = []
for idx in range(200,400):
    best_idx.append(Dist_cos_df[idx].sort_values().index[-2])
    print(Dist_cos_df[idx].sort_values().index[-2])



