import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Load
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
winetales_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/winetales_df_v2.pkl')
with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_vec.pkl', 'rb') as handle:
    [weight_vec] = pickle.load(handle)
total_len = winetales_df.shape[0]
_, desc_temp, desc_idx_train, desc_idx_temp = train_test_split(range(total_len), range(total_len), test_size=0.20, random_state=0)
_, _, desc_idx_val, desc_idx_test = train_test_split(desc_temp,desc_idx_temp,test_size = 0.5, random_state=0)
desc_idx_train.extend(desc_idx_val)

winetales_cos_dist_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/winetales_cos_dist_df_v3.pkl')

text_idx = 1
recommedation_list = list(winetales_cos_dist_df[desc_idx_test[text_idx]].sort_values().index[1:4])

cosine_result = np.multiply((np.multiply(winetales_df.loc[desc_idx_test[text_idx], :], winetales_df.loc[recommedation_list[0], :])).to_numpy(), weight_vec)


with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_cate_vec_dict.pkl', 'rb') as f:
    [weight_cate_vec_dict, weight_cate_vec_list] = pickle.load(f)


doc2vec_idx = range(50)
alcohol_idx = 50
sugar_idx = 51
madein_city_idx = range(52,52+len(weight_cate_vec_dict['Madein_city']))
idx = 52+len(weight_cate_vec_dict['Madein_city'])
madein_country_idx = range(idx,idx+len(weight_cate_vec_dict['Madein_country']))
idx = idx+len(weight_cate_vec_dict['Madein_country'])
brand_idx = range(idx,idx+len(weight_cate_vec_dict['Brand']))
idx = idx+len(weight_cate_vec_dict['Brand'])
sweetness_idx = range(idx,idx+len(weight_cate_vec_dict['Sweetness']))
idx = idx+len(weight_cate_vec_dict['Sweetness'])
style1_idx = range(idx,idx+len(weight_cate_vec_dict['Style1']))
idx = idx+len(weight_cate_vec_dict['Style1'])
style2_idx = range(idx,idx+len(weight_cate_vec_dict['Style2']))
idx = idx+len(weight_cate_vec_dict['Style2'])
variety_idx = range(idx,idx+len(weight_cate_vec_dict['Variety']))

Variable = 'Madein_city'
rw_df.loc[desc_idx_test[text_idx], Variable]
rw_df.loc[recommedation_list[0], Variable]

cosine_result_sum = {}
cosine_result_sum['D2V'] = sum(cosine_result[list(doc2vec_idx)])
cosine_result_sum['Al'] = (cosine_result[alcohol_idx])
cosine_result_sum['Sug'] = (cosine_result[sugar_idx])
cosine_result_sum['City'] = sum(cosine_result[madein_city_idx])
cosine_result_sum['Coun'] = sum(cosine_result[madein_country_idx])
cosine_result_sum['Br'] = sum(cosine_result[brand_idx])
cosine_result_sum['Swe'] = sum(cosine_result[sweetness_idx])
cosine_result_sum['Stl1'] = sum(cosine_result[style1_idx])
cosine_result_sum['Stl2'] = sum(cosine_result[style2_idx])
cosine_result_sum['Var'] = sum(cosine_result[variety_idx])

D = cosine_result_sum
plt.figure(figsize=(6,2))
plt.bar(range(len(D)), list(D.values()), align='center')
plt.xticks(range(len(D)), list(D.keys()), rotation='vertical')
# # for python 2.x:
# plt.bar(range(len(D)), D.values(), align='center')  # python 2.x
# plt.xticks(range(len(D)), D.keys())  # in python 2.x

plt.show()
