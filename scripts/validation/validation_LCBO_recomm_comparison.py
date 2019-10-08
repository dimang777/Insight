""" This is a visualization script. Twelve similar wine 
products were used as input. The input products had "featured products" from 
LCBO website (LCBO version of recommendation) 
and were used to generate the recommended wines.

"""
import pandas as pd
import pickle
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Load
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
winetales_cos_dist_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/winetales_cos_dist_df_v2.pkl')
winetales_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/winetales_df.pkl')
with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_vec.pkl', 'rb') as handle:
    [weight_vec] = pickle.load(handle)
total_len = winetales_df.shape[0]

# Input products
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

# Featured products by LCBO website
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

# Generate indices
list_input_idx = []
for LCBO_id_input in list_input:
    list_input_idx.append(rw_df.loc[rw_df['LCBO_id'] == LCBO_id_input].index[0])

# Get recommendations
list_input_wt_recomm = []
for input_idx in list_input_idx:
    sim_best = list(winetales_cos_dist_df[input_idx].sort_values().index[1:3])
    list_input_wt_recomm.extend(sim_best)

# Generate indices
list_LCBOfeatured_idx = []
for LCBO_featured in list_featured:
    list_LCBOfeatured_idx.append(rw_df.loc[rw_df['LCBO_id'] == LCBO_featured].index[0])

# Generate the figure using T-SNE
X = winetales_df.to_numpy()
tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

plt.scatter(X_tsne[:, 0], X_tsne[:, 1],color='grey', label='Samples')
plt.scatter(X_tsne[list_input_idx, 0], X_tsne[list_input_idx, 1],color='black', label='Inputs')
plt.scatter(X_tsne[list_input_wt_recomm, 0], X_tsne[list_input_wt_recomm, 1],color='blue', label='WT Recomm')
plt.scatter(X_tsne[list_LCBOfeatured_idx, 0], X_tsne[list_LCBOfeatured_idx, 1],color='red', label='LCBO Feature')
plt.legend(loc='upper left');
plt.show()


