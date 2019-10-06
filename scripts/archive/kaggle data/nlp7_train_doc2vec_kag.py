import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np

# This particular model has been deleted accidentally.
# It didn't work.


# =============================================================================
# kag_desc_prepro = pd.read_pickle('../data/cleaned/kag_desc_prepro.pkl')
# desc_token_kag = list(kag_desc_prepro['Desc_lemmatized'])
# desc_token = list(kag_desc_prepro['Desc_lemmatized'])
# kag_len = len(desc_token_kag)
# 
# rw_desc_prepro = pd.read_pickle('../data/cleaned/rw_desc_df_prepro.pkl')
# rw_df = pd.read_excel('../data/for_models/rw_df_mvp_v2.xlsx')
# LCBO_id = rw_df['LCBO_id']
# desc_token_LCBO = list(rw_desc_prepro['Desc_lemmatized'])
# LCBO_len = len(desc_token_LCBO)
# 
# print(kag_len)
# print(LCBO_len)
# print(len(LCBO_id))
# 
# desc_token.extend(desc_token_LCBO)
# total_len = len(desc_token)
# 
# 
# 
# tagged_data = []
# for idx, _data in enumerate(desc_token):
#     if np.mod(idx,1000)==0:
#         print(idx)
#     if idx < kag_len:
#         tagged_data.append(TaggedDocument(_data, tags=[str(idx), '']))
#     else:
#         tagged_data.append(TaggedDocument(_data, tags=[str(idx), LCBO_id[idx-kag_len]]))
# 
# 
# 
# 
# 
# max_epochs = 50
# vec_size = 25
# alpha = 0.025
# window_size = 5
# num_workers = 4
# minimun_count = 2
# model = Doc2Vec(vector_size = vec_size,
#                 window = window_size,
#                 alpha = alpha,
#                 min_alpha = 0.00025,
#                 min_count = minimun_count,
#                 dm = 1,
#                 workers = num_workers,
#                 epochs = max_epochs)
#   
# model.build_vocab(tagged_data)
# 
# for epoch in range(max_epochs):
#     print('iteration {0}'.format(epoch))
#     model.train(tagged_data,
#                 total_examples = model.corpus_count,
#                 epochs = model.epochs)
#     # decrease the learning rate
#     model.alpha -= 0.0002
#     # fix the learning rate, no decay
#     # model.min_alpha = model.alpha
# 
# model.save('../models/kag_d2v.model')
# print('Model Saved')
# 
# 
# model= Doc2Vec.load('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/kag_d2v_25vec_lem.model')
# 
# 
# # Test 1
# 
# similar_doc = model.docvecs.most_similar('129975')
# print(similar_doc)
# 
# rw_df[['Name', 'Madein_country', 'Madein_city', 'Variety']][rw_df['LCBO_id']=='V155713'].index
# 
# rw_df['Description'][0]
# rw_df['Description'][704]
# 
# rw_df.loc[0, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
# rw_df.loc[704, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
# # Maybe little
# 
# 
# # Test 2
# similar_doc = model.docvecs.most_similar('129976')
# print(similar_doc)
# 
# rw_df[rw_df['LCBO_id']=='L524520'].index
# 
# rw_df['Description'][1]
# rw_df['Description'][1013]
# 
# rw_df.loc[1, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
# rw_df.loc[1013, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
# # Not really
# 
# 
# # Test 3
# similar_doc = model.docvecs.most_similar('129977')
# print(similar_doc)
# 
# rw_df[rw_df['LCBO_id']=='V473116'].index
# 
# rw_df['Description'][2]
# rw_df['Description'][2097]
# 
# rw_df.loc[2, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
# rw_df.loc[2097, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
# # Not really
# 
# 
# test_data = desc_token_LCBO[0]
# v1 = model.infer_vector(test_data)
# print("V1_infer", v1)
# 
# # to find most similar doc using tags
# similar_doc = model.docvecs.most_similar('129976')
# print(similar_doc)
# 
# 
# # to find vector of doc in training data using tags or in other words, printing the vector of document at index 1 in training data
# print(model.docvecs['1'])
# 
# 
# 
#
# 
# =============================================================================

