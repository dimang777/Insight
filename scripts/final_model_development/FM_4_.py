from scipy.spatial.distance import pdist, squareform, cosine
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from scipy.spatial.distance import cosine
import numpy as np

rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')

winetales_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/winetales_df.pkl')
with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_vec.pkl', 'rb') as handle:
    [weight_vec] = pickle.load(handle)

total_len = winetales_df.shape[0]

_, desc_temp, desc_idx_train, desc_idx_temp = train_test_split(range(total_len), range(total_len), test_size=0.20, random_state=0)
_, _, desc_idx_val, desc_idx_test = train_test_split(desc_temp,desc_idx_temp,test_size = 0.5, random_state=0)
desc_idx_train.extend(desc_idx_val)

# Practice
if 0:
    cosine([1,1,0], [1,1,1], w=[1,1,1])
    cosine([1,1,0], [1,1,1], w=[1,1,0])
    Dist_cos = squareform(pdist([[1,1,0], [1,1,1]], 'cosine', w=[1,1,1]))
    Dist_cos = squareform(pdist([[1,1,0], [1,1,1]], 'cosine', w=[1,1,0]))


winetales_cos_dist = squareform(pdist(winetales_df.to_numpy(), 'cosine', w=weight_vec))

with open('C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/winetales_cos_dist_v2.pkl', 'wb') as f:
    pickle.dump([winetales_cos_dist], f)

winetales_cos_dist_df = pd.DataFrame(winetales_cos_dist)
winetales_cos_dist_df.to_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/winetales_cos_dist_df_v2.pkl')

# dist_list = []
# index = 0
# for idx in range(total_len):
#     dist_list.append(cosine(winetales_df[index], winetales_df[idx], w=weight_vec))

# dist_list_df = pd.DataFrame(dist_list).sort_values()
# dist_list_df[0:5]








index = 5
sim_best = winetales_cos_dist_df[desc_idx_test[index]].sort_values().index[1]
print(rw_df['Description'][desc_idx_test[index]])
print('\n')
print(rw_df['Description'][sim_best])

print(rw_df.loc[desc_idx_test[index], ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
print('\n')
print(rw_df.loc[sim_best, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])



for idx in desc_idx_test[0:10]:
    print(rw_df.loc[idx, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])

desc_idx_test
# rw_df.loc[desc_idx_test, ['LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']].sort_values(by=['Variety']).to_excel('test_variety.xlsx')
rw_df.loc[:, ['LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']].sort_values(by=['Variety']).to_excel('test_variety_entire.xlsx')



# best_idx = []
# for idx in range(200,400):
#     best_idx.append(Dist_cos_df[idx].sort_values().index[1])
#     print(Dist_cos_df[idx].sort_values().index[1])


# len(Dist_cos_df[idx])
# best_idx.append(Dist_cos_df[0].sort_values().index[1])









