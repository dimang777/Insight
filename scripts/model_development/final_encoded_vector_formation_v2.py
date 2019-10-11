""" This script generates the final weight vector for weighted cosine 
similarity and the fully encoded vector for each product and turned into
dataframe called winetales_df
"""
import pandas as pd
import pickle

# Load
d2v_df = pd.read_pickle(\
    'C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/d2v_df.pkl')
rw_df_ohe_numeric = pd.read_pickle(\
    'C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_df_ohe.pkl')
# Drop unnecessary columns
rw_df_ohe_numeric = rw_df_ohe_numeric.drop(\
    ['Price', 'Size', 'LCBO_id', 'Name', 'Description', 'Pic_src', 'URL', \
     'Unnamed: 0'], axis = 1)
with open(\
    'C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/Weight_Cate_vec_dict.pkl', 'rb')\
    as handle:
    [weight_cate_vec_dict, weight_cate_vec_list] = pickle.load(handle)

# Normalize numerical variables
Variable = 'Alcohol'
rw_df_ohe_numeric[Variable] = \
    (rw_df_ohe_numeric[Variable] - rw_df_ohe_numeric[Variable].min())/  \
    (rw_df_ohe_numeric[Variable].max() - rw_df_ohe_numeric[Variable].min())

Variable = 'Sugar'
rw_df_ohe_numeric[Variable] = \
    (rw_df_ohe_numeric[Variable] - rw_df_ohe_numeric[Variable].min())/  \
    (rw_df_ohe_numeric[Variable].max() - rw_df_ohe_numeric[Variable].min())

# Numerical and text weights
weight_num_vec_dict = {'Alcohol': 0.5, 'Sugar': 0.6}
weight_text_vec_dict = {'Desc_Vec': [0.5]*50} # 50 is the vector size

# Form the weight vector
weight_vec = weight_text_vec_dict['Desc_Vec']
weight_vec.append(weight_num_vec_dict['Alcohol'])
weight_vec.append(weight_num_vec_dict['Sugar'])
weight_vec.extend(weight_cate_vec_list)

# Fully encoded vector for all products saved in dataframe
winetales_df = pd.concat([d2v_df, rw_df_ohe_numeric], axis=1)

# Save
winetales_df.to_pickle(\
    'C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/winetales_df_v2.pkl')
with open(\
    'C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_vec.pkl', 'wb')\
    as f:
    pickle.dump([weight_vec], f)


