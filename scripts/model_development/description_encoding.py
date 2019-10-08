""" This script generates the encoded vector from doc2vec model for each 
product.
"""
import pandas as pd
from gensim.models.doc2vec import Doc2Vec

# Load doc2vec model
max_epochs = 50
vec_size = 50
alpha = 0.025
window_size = 2
num_workers = 4
minimun_count = 1
dm_select = 0 # 1: PV-DM; 0:PV-DBOW
model_name = 'Desc_encoding_model_' + 'e' + str(max_epochs) + '_' + 'v' + str(vec_size) + '_' \
                + 'w' + str(window_size) + '_' + 'c' + str(minimun_count) + '_' \
                + 'd' + str(dm_select)
model= Doc2Vec.load('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/' +model_name +'.model')

# Load preprocessed description data and the product dataframe
rw_mod_desc = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_mod_desc_v2.pkl')
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
LCBO_id = rw_df['LCBO_id']
desc_token = list(rw_mod_desc['Desc_lemmatized'])
total_len = len(desc_token)

# generate vector df
for idx in range(total_len):
    if idx == 0:
        d2v_list = [model.infer_vector(desc_token[idx])]
    else:
        d2v_list.append(model.infer_vector(desc_token[idx]))

d2v_df = pd.DataFrame(d2v_list)
d2v_df.to_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/d2v_df.pkl')





