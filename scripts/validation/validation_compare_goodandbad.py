""" This file compares bad and good examples based on the feedback
"""
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from scipy.spatial.distance import pdist, squareform
import numpy as np


# Import dataframes
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
winetales_cos_dist_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/winetales_cos_dist_df_v2.pkl')
winetales_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/winetales_df.pkl')
with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_vec.pkl', 'rb') as handle:
    [weight_vec] = pickle.load(handle)
with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/validation100_input_idx.pkl', 'rb') as f:
    [validation100_input_idx, validation100_recomm_list] = pickle.load(f)
with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_cate_vec_dict.pkl', 'rb') as f:
    [weight_cate_vec_dict, weight_cate_vec_list] = pickle.load(f)

total_len = winetales_df.shape[0]

_, desc_temp, desc_idx_train, desc_idx_temp = train_test_split(range(total_len), range(total_len), test_size=0.20, random_state=0)
_, _, desc_idx_val, desc_idx_test = train_test_split(desc_temp,desc_idx_temp,test_size = 0.5, random_state=0)
desc_idx_train.extend(desc_idx_val)

# text data index
text_idx = range(50)
# numerical data index
alcohol_idx = 50
sugar_idx = 51
# Categorical order
# weight_cate = {'Madein_city':1,'Madein_country':1, 'Brand': 0.5, 'Sweetness': 0.6, \
#           'Style1': 0.7, 'Style2': 0.7, 'Variety': 1}
count = 52
madein_city_idx = range(count, count+len(weight_cate_vec_dict['Madein_city']))
count = count+len(weight_cate_vec_dict['Madein_city'])
madein_country_idx = range(count, count+len(weight_cate_vec_dict['Madein_country']))
count = count+len(weight_cate_vec_dict['Madein_country'])
madein_brand_idx = range(count, count+len(weight_cate_vec_dict['Brand']))
count = count+len(weight_cate_vec_dict['Brand'])
madein_sweetness_idx = range(count, count+len(weight_cate_vec_dict['Sweetness']))
count = count+len(weight_cate_vec_dict['Sweetness'])
madein_style1_idx = range(count, count+len(weight_cate_vec_dict['Style1']))
count = count+len(weight_cate_vec_dict['Style1'])
madein_style2_idx = range(count, count+len(weight_cate_vec_dict['Style2']))
count = count+len(weight_cate_vec_dict['Style2'])
madein_variety_idx = range(count, count+len(weight_cate_vec_dict['Variety']))




idx = 0

rw_df.loc[validation100_input_idx[idx] ,\
          ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', \
           'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']]
rw_df.loc[validation100_recomm_list[idx][0] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']]
rw_df.loc[validation100_recomm_list[idx][1] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']]
rw_df.loc[validation100_recomm_list[idx][2] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']]



# Cosine similarity calculation

winetales_cos_dist = squareform(pdist(winetales_df.to_numpy(), 'cosine', w=weight_vec))


winetales_df.loc[validation100_input_idx[idx], :]
winetales_df.loc[validation100_recomm_list[idx][0], :]
winetales_df.loc[validation100_recomm_list[idx][1], :]
winetales_df.loc[validation100_recomm_list[idx][2], :]

u = winetales_df.loc[validation100_input_idx[idx], :].to_numpy()
v = winetales_df.loc[validation100_recomm_list[idx][0], :].to_numpy()

uv = u * v

uv


weight_vec


uu = np.average(np.square(u), weights=weight_vec)
vv = np.average(np.square(v), weights=weight_vec)
dist = 1.0 - uv / np.sqrt(uu * vv)


uv[text_idx]
uv[alcohol_idx]
text_idx
alcohol_idx
sugar_idx

madein_city_idx, madein_country_idx, madein_brand_idx, madein_sweetness_idx,
madein_style1_idx, madein_style2_idx, madein_variety_idx












good_list_temp = [ \
    23, 24, 27, 28, 34, 37, 40, 42, 47, 48, 51, 52, 53, 57, 60, 70, 72, \
    73, 75, 76, 80, 85, 87, 95, 97, 98]
good_list = [idx - 1 for idx in good_list_temp]
bad_list_temp = [ \
    11, 16, 19, 22, 25, 63, 67, 68, 77, 81, 86, 88, 91, 93, 94, 99, 100]
bad_list = [idx - 1 for idx in bad_list_temp]



