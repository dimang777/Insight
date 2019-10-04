from scipy.spatial.distance import pdist, squareform, cosine
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from scipy.spatial.distance import cosine
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')

winetales_cos_dist_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/winetales_cos_dist_df_v2.pkl')

winetales_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/winetales_df.pkl')
with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_vec.pkl', 'rb') as handle:
    [weight_vec] = pickle.load(handle)

total_len = winetales_df.shape[0]


list_input = ['L383885',
'L461053',
'L541961',
'L356113',
'L643882',
'L292128',
'L68924',
'L336974',
'L541946',
'L269761',
'L392647',
'L392225']

list_featured = ['L434696',
'L638221',
'L541946',
'L383885',
'V337238',
'V985002',
'L515684',
'L570754',
'L460667',
'V27516',
'L572800',
'L454835',
'V59311',
'L442491',
'V606590',
'V656561',
'L358838',
'V521021',
'V478727',
'L457119']

list_input_idx = []
for LCBO_id_input in list_input:
    list_input_idx.append(rw_df.loc[rw_df['LCBO_id'] == LCBO_id_input].index[0])


list_input_wt_recomm = []

for input_idx in list_input_idx:
    sim_best = list(winetales_cos_dist_df[input_idx].sort_values().index[1:3])
    list_input_wt_recomm.extend(sim_best)

list_LCBOfeatured_idx = []
for LCBO_featured in list_featured:
    list_LCBOfeatured_idx.append(rw_df.loc[rw_df['LCBO_id'] == LCBO_featured].index[0])

input_df = winetales_df.loc[list_input_idx,:]
wt_recomm_df = winetales_df.loc[list_input_wt_recomm,:]
LCBO_featured_df = winetales_df.loc[list_LCBOfeatured_idx,:]




# fig = plt.figure()
# ax1 = fig.add_subplot(111)

X = winetales_df.to_numpy()
tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)
plt.scatter(x,y, c='b', marker='x', label='1')
plt.scatter(x, y, c='r', marker='s', label='-1')
plt.legend(loc='upper left')
plt.show()

plt.scatter(X_tsne[:, 0], X_tsne[:, 1],color='grey', label='Samples')

plt.scatter(X_tsne[list_input_idx, 0], X_tsne[list_input_idx, 1],color='black', label='Inputs')

plt.scatter(X_tsne[list_input_wt_recomm, 0], X_tsne[list_input_wt_recomm, 1],color='blue', label='WT Recomm')

plt.scatter(X_tsne[list_LCBOfeatured_idx, 0], X_tsne[list_LCBOfeatured_idx, 1],color='red', label='LCBO Feature')
plt.legend(loc='upper left');

plt.show()

len(X_tsne)
color=['red','green','blue']


sim_best = winetales_cos_dist_df[list_input_idx[index]].sort_values().index[1]
print(rw_df['Description'][list_input_idx[index]])
print('\n')
print(rw_df['Description'][sim_best])

print(rw_df.loc[list_input_idx[index], ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
print('\n')
print(rw_df.loc[sim_best, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])







rw_df['LCBO_id'][rw_df['LCBO_id'] == 'L538074']








