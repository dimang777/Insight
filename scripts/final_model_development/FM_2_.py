from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from gensim.models.doc2vec import Doc2Vec, TaggedDocument



# Load doc2vec
max_epochs = 50
vec_size = 50
alpha = 0.025
window_size = 2
num_workers = 4
minimun_count = 1
dm_select = 0 # 1: PV-DM; 0:PV-DBOW

model_name = 'FM_v1_' + 'e' + str(max_epochs) + '_' + 'v' + str(vec_size) + '_' \
                + 'w' + str(window_size) + '_' + 'c' + str(minimun_count) + '_' \
                + 'd' + str(dm_select)

model= Doc2Vec.load('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/' +model_name +'.model')




rw_mod_desc = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_mod_desc_v2.pkl')
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
LCBO_id = rw_df['LCBO_id']
desc_token = list(rw_mod_desc['Desc_lemmatized'])
LCBO_len = len(desc_token)
total_len = len(desc_token)

desc_train, desc_temp, desc_idx_train, desc_idx_temp = train_test_split(desc_token, range(total_len), test_size=0.20, random_state=0)
desc_val, desc_test, desc_idx_val, desc_idx_test = train_test_split(desc_temp,desc_idx_temp,test_size = 0.5, random_state=0)

desc_idx_train.extend(desc_idx_val)
desc_train.extend(desc_val)

# generate vector df
for idx in range(total_len):
    if idx == 0:
        d2v_list = [model.infer_vector(desc_token[idx])]
    else:
        d2v_list.append(model.infer_vector(desc_token[idx]))


d2v_df = pd.DataFrame(d2v_list)

d2v_df.to_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/d2v_df.pkl')





