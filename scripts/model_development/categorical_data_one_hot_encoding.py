""" Encode categorical variables using one hot encoding and generate weight 
vector for the cosine similarity
# Iteration notes
# version 1
# weight_cate = {'Madein_city':1,'Madein_country':1, 'Brand': 0.6, 'Sweetness': 0.7, \
#           'Style1': 0.8, 'Style2': 0.8, 'Variety': 0.95}
# version 2
# weight_cate = {'Madein_city':1,'Madein_country':1, 'Brand': 0.5, 'Sweetness': 0.6, \
#           'Style1': 0.7, 'Style2': 0.7, 'Variety': 0.95}
"""
import pandas as pd
import pickle

# Load data
rw_df_ohe = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')

# Iteration 3
weight_cate = {'Madein_city':1,'Madein_country':1, 'Brand': 0.5, 'Sweetness': 0.6, \
          'Style1': 0.7, 'Style2': 0.7, 'Variety': 1}
weight_cate_vec_dict = {}
weight_cate_vec_list = []


# Madein_city
Variable = 'Madein_city'
rw_df_ohe[Variable] = pd.Categorical(rw_df_ohe[Variable])
rw_df_ohe = pd.concat([rw_df_ohe, pd.get_dummies(rw_df_ohe[Variable], prefix = 'Cit')], axis=1)
weight_cate_vec_dict[Variable] = [weight_cate[Variable]] * pd.get_dummies(rw_df_ohe[Variable], prefix = 'Cit').shape[1]
weight_cate_vec_list.extend(weight_cate_vec_dict[Variable])
rw_df_ohe = rw_df_ohe.drop([Variable], axis = 1)
print(Variable)

# Madein_country
Variable = 'Madein_country'
rw_df_ohe[Variable] = pd.Categorical(rw_df_ohe[Variable])
rw_df_ohe = pd.concat([rw_df_ohe, pd.get_dummies(rw_df_ohe[Variable], prefix = 'Cou')], axis=1)
weight_cate_vec_dict[Variable] = [weight_cate[Variable]] * pd.get_dummies(rw_df_ohe[Variable], prefix = 'Cit').shape[1]
weight_cate_vec_list.extend(weight_cate_vec_dict[Variable])
rw_df_ohe = rw_df_ohe.drop([Variable], axis = 1)
print(Variable)

# Brand
Variable = 'Brand'
rw_df_ohe[Variable] = pd.Categorical(rw_df_ohe[Variable])
rw_df_ohe = pd.concat([rw_df_ohe, pd.get_dummies(rw_df_ohe[Variable], prefix = 'Bra')], axis=1)
weight_cate_vec_dict[Variable] = [weight_cate[Variable]] * pd.get_dummies(rw_df_ohe[Variable], prefix = 'Cit').shape[1]
weight_cate_vec_list.extend(weight_cate_vec_dict[Variable])
rw_df_ohe = rw_df_ohe.drop([Variable], axis = 1)
print(Variable)

# Sweetness
Variable = 'Sweetness'
rw_df_ohe[Variable] = pd.Categorical(rw_df_ohe[Variable])
rw_df_ohe = pd.concat([rw_df_ohe, pd.get_dummies(rw_df_ohe[Variable], prefix = 'Swe')], axis=1)
weight_cate_vec_dict[Variable] = [weight_cate[Variable]] * pd.get_dummies(rw_df_ohe[Variable], prefix = 'Cit').shape[1]
weight_cate_vec_list.extend(weight_cate_vec_dict[Variable])
rw_df_ohe = rw_df_ohe.drop([Variable], axis = 1)
print(Variable)

# Style1
Variable = 'Style1'
rw_df_ohe[Variable] = pd.Categorical(rw_df_ohe[Variable])
rw_df_ohe = pd.concat([rw_df_ohe, pd.get_dummies(rw_df_ohe[Variable], prefix = 'St1')], axis=1)
weight_cate_vec_dict[Variable] = [weight_cate[Variable]] * pd.get_dummies(rw_df_ohe[Variable], prefix = 'Cit').shape[1]
weight_cate_vec_list.extend(weight_cate_vec_dict[Variable])
rw_df_ohe = rw_df_ohe.drop([Variable], axis = 1)
print(Variable)

# Style2
Variable = 'Style2'
rw_df_ohe[Variable] = pd.Categorical(rw_df_ohe[Variable])
rw_df_ohe = pd.concat([rw_df_ohe, pd.get_dummies(rw_df_ohe[Variable], prefix = 'St2')], axis=1)
weight_cate_vec_dict[Variable] = [weight_cate[Variable]] * pd.get_dummies(rw_df_ohe[Variable], prefix = 'Cit').shape[1]
weight_cate_vec_list.extend(weight_cate_vec_dict[Variable])
rw_df_ohe = rw_df_ohe.drop([Variable], axis = 1)

# Variety
Variable = 'Variety'
rw_df_ohe[Variable] = pd.Categorical(rw_df_ohe[Variable])
rw_df_ohe = pd.concat([rw_df_ohe, pd.get_dummies(rw_df_ohe[Variable], prefix = 'Var')], axis=1)
weight_cate_vec_dict[Variable] = [weight_cate[Variable]] * pd.get_dummies(rw_df_ohe[Variable], prefix = 'Cit').shape[1]
weight_cate_vec_list.extend(weight_cate_vec_dict[Variable])
rw_df_ohe = rw_df_ohe.drop([Variable], axis = 1)
print(Variable)

# Save
rw_df_ohe.to_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_df_ohe.pkl')

with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_cate_vec_dict.pkl', 'wb') as f:
    pickle.dump([weight_cate_vec_dict, weight_cate_vec_list], f)


