import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np
from timeit import default_timer as timer
from sklearn.model_selection import train_test_split
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pickle

# Training doc2vec model iteration 4
# Remove description altogether
# inclusion of description didn't increase the accuracy
# Because of the smaller data set, reduce the vector size to 50
# Previous model had overall lower similarity score (0.62)

rw_mod_desc = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_mod_desc.pkl')
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
LCBO_id = rw_df['LCBO_id']
desc_token = list(rw_mod_desc['Cate_only_nodesc'])
LCBO_len = len(desc_token)

print(LCBO_len)
print(len(LCBO_id))

total_len = len(desc_token)

# Divide into train, validation, and test sets
desc_train, desc_temp, desc_idx_train, desc_idx_temp = train_test_split(desc_token, range(total_len), test_size=0.20, random_state=0)
desc_val, desc_test, desc_idx_val, desc_idx_test = train_test_split(desc_temp,desc_idx_temp,test_size = 0.5, random_state=0)
with open('train_val_test.pickle', 'wb') as f:
    pickle.dump([desc_idx_train, desc_idx_val, desc_idx_test], f)

tagged_data = []
for idx, entry in zip(desc_idx_train, desc_train):
    print(idx)
    if np.mod(idx,500)==0:
        print(idx)
    tagged_data.append(TaggedDocument(entry, tags=[str(idx)]))

# Create df
dummy = ''
Model_tuning_df_idx = 0
Model_tuning_df = pd.DataFrame({'max_epochs':dummy, 'vec_size':dummy, \
    'alpha':dummy, 'window_size':dummy, \
    'num_workers':dummy, 'minimun_count':dummy, \
    'dm_select':dummy, 'match_score_percent':dummy, \
    'similarity_score_mean':dummy}, index=[Model_tuning_df_idx])

for dm_select in range(0,2):
    for window_size in range(1, 6):
        for minimun_count in range(1,4):
        
            max_epochs = 50
            vec_size = 20
            alpha = 0.025
            # window_size = 2
            num_workers = 4
            # minimun_count = 1
            # dm_select = 1 # 1: PV-DM; 0:
            model = Doc2Vec(vector_size = vec_size,
                            window = window_size,
                            alpha = alpha,
                            min_alpha = 0.00025,
                            min_count = minimun_count,
                            dm = dm_select,
                            workers = num_workers,
                            epochs = max_epochs)
              
            model.build_vocab(tagged_data)
            
            for epoch in range(max_epochs):
                start = timer()
                print('iteration {0}'.format(epoch))
                model.train(tagged_data,
                            total_examples = model.corpus_count,
                            epochs = model.epochs)
                # decrease the learning rate
                model.alpha -= 0.0002
                # fix the learning rate, no decay
                # model.min_alpha = model.alpha
                duration = timer() - start
                print(duration)
            
            model_name = 'v3_' + 'e' + str(max_epochs) + '_' + 'v' + str(vec_size) + '_' \
                + 'w' + str(window_size) + '_' + 'c' + str(minimun_count) + '_' \
                + 'd' + str(dm_select)
            
            model.save('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/'+model_name+'.model')
            model.save('C:/Users/diman/OneDrive/Work_temp/Insight/LargeModels/'+model_name+'.model')
            print('Model Saved')
            
            # model= Doc2Vec.load('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/v3_nodesc_d2v_50vec_2win_lemma.model')
            
            
            
            # Test 1
            # rw_df_num = desc_idx_train[0]
            # total_num = rw_df_num
            # display_num = 10
            # similar_doc = model.docvecs.most_similar(str(total_num), topn=display_num)
            # print(similar_doc)
            # sim_found_num = int(similar_doc[0][0])
            
            # print(rw_df['Description'][rw_df_num])
            # print('\n')
            # print(rw_df['Description'][sim_found_num])
            
            # print(rw_df.loc[rw_df_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
            # print('\n')
            # print(rw_df.loc[sim_found_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
            
            
            
            # calculate average similarity score
            similarity_score_list = []
            for idx in desc_idx_train:
                if np.mod(idx,1000)==0:
                    print(idx)
                similar_doc = model.docvecs.most_similar(str(idx))
                similarity_score_list.append(float(similar_doc[0][1]))
            
            similarity_score_mean = np.mean(similarity_score_list)
            print(similarity_score_mean)
            
            # 0.7985
            
            
            doc_tags = list(model.docvecs.doctags.keys())
            X = model[doc_tags]
            
            tsne = TSNE(n_components=2)
            X_tsne = tsne.fit_transform(X)
            df = pd.DataFrame(X_tsne, index=doc_tags, columns=['x', 'y'])
            
            # Pinot Grigio
            plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
            plt.show()
            
            
            # Similarity measurement
            categories = ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']
            
            # Evaluate test set
            for idx, test_data in zip(desc_idx_test, desc_test):
                v1 = model.infer_vector(test_data)
                sims = model.docvecs.most_similar([v1])
                sim_best = int(sims[0][0])
                print(idx)
                match_score = []
                for category in categories:
                    if rw_df.loc[idx, category] == rw_df.loc[sim_best, category]:
                        match_score.append(1)
                    else:
                        match_score.append(0)
                if desc_idx_test.index(idx) == 0:
                    match_score_indi_df = pd.DataFrame({'Name':idx, 'Score':[match_score]})
                    match_score_sum_df = pd.DataFrame({'Name':idx, 'Score':[sum(match_score)]})
                else:
                    match_score_indi_df = pd.concat([match_score_indi_df, pd.DataFrame({'Name':idx, 'Score':[match_score]})], ignore_index = True)
                    match_score_sum_df = pd.concat([match_score_sum_df, pd.DataFrame({'Name':idx, 'Score':[sum(match_score)]})], ignore_index = True)
            
            
            
            match_score_percent = match_score_sum_df.mean()[1]/10
            Model_tuning_df_idx += 1
            Model_tuning_df = pd.concat([Model_tuning_df, pd.DataFrame({\
                'max_epochs':max_epochs, 'vec_size':vec_size, \
                'alpha':alpha, 'window_size':window_size, \
                'num_workers':num_workers, 'minimun_count':minimun_count, \
                'dm_select':dm_select, 'match_score_percent':match_score_percent, \
                'similarity_score_mean':similarity_score_mean}, index=[Model_tuning_df_idx])])



