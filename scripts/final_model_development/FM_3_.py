from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from scipy.spatial.distance import cosine

d2v_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/d2v_df.pkl')

rw_df_ohe_numeric = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_df_ohe.pkl')
rw_df_ohe_numeric = rw_df_ohe_numeric.drop(['Price', 'Size', 'LCBO_id', 'Name', 'Description', 'Pic_src', 'URL', 'Unnamed: 0'], axis = 1)
print(rw_df_ohe_numeric.columns)

with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/Weight_Cate_vec_dict.pkl', 'rb') as handle:
    [weight_cate_vec_dict, weight_cate_vec_list] = pickle.load(handle)

weight_num_vec_dict = {'Alcohol': 0.5, 'Sugar': 0.6}
weight_text_vec_dict = {'Desc_Vec': [0.5]*50}

weight_vec = weight_text_vec_dict['Desc_Vec']

weight_vec.append(weight_num_vec_dict['Alcohol'])
weight_vec.append(weight_num_vec_dict['Sugar'])

weight_vec.extend(weight_cate_vec_list)

winetales_df = pd.concat([d2v_df, rw_df_ohe_numeric], axis=1)

winetales_df.to_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/winetales_df.pkl')


with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_vec.pkl', 'wb') as f:
    pickle.dump([weight_vec], f)


