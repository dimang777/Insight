""" This script trains doc2vec model using the preprocessed description data
Used 90% of the data as the training set
"""
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np
from timeit import default_timer as timer
from sklearn.model_selection import train_test_split
import pickle

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

tuning_dict = {}
for dm_select in range(2):
    for minimum_count in range(1,4):
        for window_size in range(1,6):
            # model hyperparameters
            max_epochs = 50
            vec_size = 50
            alpha = 0.025
            # window_size = 2
            num_workers = 4
            # minimum_count = 1
            # dm_select = 0 # 1: PV-DM; 0:PV-DBOW
            model = Doc2Vec(vector_size = vec_size,
                            window = window_size,
                            alpha = alpha,
                            min_alpha = 0.00025,
                            min_count = minimum_count,
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
                            + 'w' + str(window_size) + '_' + 'c' + str(minimum_count) + '_' \
                            + 'd' + str(dm_select)
            # model.save('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/'+model_name+'.model')
            model.save('C:/Users/diman/OneDrive/Work_temp/Insight/LargeModels/tuning/'+model_name+'.model')
            
            
            # Evaluate test set
            cos_sim = []
            for idx, test_data in zip(desc_idx_test, desc_test):
                v1 = model.infer_vector(test_data)
                sims = model.docvecs.most_similar([v1])
                sim_best_sum = 0
                for idx_similar in range(10):
                    sim_best_sum += sims[idx_similar][1]
        
                cos_sim.append(sim_best_sum/10)
            
            tuning_dict[model_name] = np.mean(cos_sim)


with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/tuning_dict.pkl', 'wb') as f:
    pickle.dump([tuning_dict], f)

with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/tuning_dict.pkl', 'rb') as f:
    tuning_dict = pickle.load(f)



