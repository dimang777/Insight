""" This script trains doc2vec model using the preprocessed description data
Used 90% of the data as the training set
"""
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np
from timeit import default_timer as timer
from sklearn.model_selection import train_test_split

rw_mod_desc = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_mod_desc_v2.pkl')
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
LCBO_id = rw_df['LCBO_id']
desc_token = list(rw_mod_desc['Desc_lemmatized'])
total_len = len(desc_token)

# Generate train and test sets
# Validation set combined with the train set since not used
desc_train, desc_temp, desc_idx_train, desc_idx_temp = train_test_split(desc_token, range(total_len), test_size=0.20, random_state=0)
desc_val, desc_test, desc_idx_val, desc_idx_test = train_test_split(desc_temp,desc_idx_temp,test_size = 0.5, random_state=0)
desc_idx_train.extend(desc_idx_val)
desc_train.extend(desc_val)

# Generate tagged data
tagged_data = []
for idx, entry in zip(desc_idx_train, desc_train):
    print(idx)
    if np.mod(idx,500)==0:
        print(idx)
    tagged_data.append(TaggedDocument(entry, tags=[str(idx)]))

# model hyperparameters
max_epochs = 50
vec_size = 50
alpha = 0.025
window_size = 2
num_workers = 4
minimun_count = 1
dm_select = 0 # 1: PV-DM; 0:PV-DBOW
model = Doc2Vec(vector_size = vec_size,
                window = window_size,
                alpha = alpha,
                min_alpha = 0.00025,
                min_count = minimun_count,
                dm = dm_select, 
                workers = num_workers,
                epochs = max_epochs)
  
model.build_vocab(tagged_data)

# Train
for epoch in range(max_epochs):
    start = timer()
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples = model.corpus_count,
                epochs = model.epochs)
    # decrease the learning rate
    model.alpha -= 0.0002
    duration = timer() - start
    print(duration)


# Save
model_name = 'Desc_encoding_model_' + 'e' + str(max_epochs) + '_' + 'v' + str(vec_size) + '_' \
                + 'w' + str(window_size) + '_' + 'c' + str(minimun_count) + '_' \
                + 'd' + str(dm_select)
model.save('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/'+model_name+'.model')
model.save('C:/Users/diman/OneDrive/Work_temp/Insight/LargeModels/'+model_name+'.model')

# Code for displaying each case
index = 0
idx, test_data = desc_idx_test[index], desc_test[index]


v1 = model.infer_vector(test_data)
sims = model.docvecs.most_similar([v1])
sim_best = int(sims[0][0])

print(rw_df['Description'][desc_idx_test[index]])
print('\n')
print(rw_df['Description'][sim_best])

print(rw_df.loc[desc_idx_test[index], ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
print('\n')
print(rw_df.loc[sim_best, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])

