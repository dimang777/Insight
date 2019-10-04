import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np
from timeit import default_timer as timer

# Training doc2vec model iteration 2

kag_folder = 'C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/'


kag_df_essential = pd.read_excel(kag_folder + 'kag_df_essential.xlsx')
kag_desc_prepro = pd.read_pickle(kag_folder + 'kag_desc_prepro.pkl')
desc_token_kag = list(kag_desc_prepro['Desc_nostop'])
desc_token = list(kag_desc_prepro['Desc_nostop']) # Later combined with LCBO df
kag_len = len(desc_token_kag)


rw_desc_prepro = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_desc_df_prepro.pkl') # mvp_v3 compliant
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
LCBO_id = rw_df['LCBO_id']
desc_token_LCBO = list(rw_desc_prepro['Desc_nostop'])
LCBO_len = len(desc_token_LCBO)

print(kag_len)
print(LCBO_len)
print(len(LCBO_id))

desc_token.extend(desc_token_LCBO)
total_len = len(desc_token)

idx=0
kag_df_essential.columns

tagged_data = []
for idx, entry in enumerate(desc_token):
    if np.mod(idx,1000)==0:
        print(idx)
    if idx < kag_len:
        tagged_data.append(TaggedDocument(entry, tags=[kag_df_essential['province'][idx], kag_df_essential['variety'][idx], str(idx)]))
    else:
        tagged_data.append(TaggedDocument(entry, tags=[rw_df['Madein_city'][idx-kag_len], rw_df['Variety'][idx-kag_len], str(idx)]))





max_epochs = 50
vec_size = 100 # Previous setup - 25
alpha = 0.025
window_size = 5
num_workers = 4
minimun_count = 1 # Previous setup - 2
model = Doc2Vec(vector_size = vec_size,
                window = window_size,
                alpha = alpha,
                min_alpha = 0.00025,
                min_count = minimun_count,
                dm = 1, # PV-DM
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

model.save('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/kag_d2v_v1_100vec_5win_stopword.model')
model.save('C:/Users/diman/OneDrive/Work_temp/Insight/LargeModels/kag_d2v_v1_100vec_5win_stopword.model')
print('Model Saved')

model= Doc2Vec.load('C:/Users/diman/OneDrive/Work_temp/Insight/LargeModels/kag_d2v_v1_100vec_5win_stopword.model')



# Test 1

similar_doc = model.docvecs.most_similar('129976')
print(similar_doc)

rw_df['Description'][1]
rw_df['Description'][132751-kag_len]

rw_df.loc[1, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
rw_df.loc[132751-kag_len, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
# not really


# Test 2
similar_doc = model.docvecs.most_similar('129977')
print(similar_doc)

rw_df['Description'][129977-kag_len]
rw_df['Description'][130693-kag_len]

rw_df.loc[129977-kag_len, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
rw_df.loc[130693-kag_len, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
# different


# Test 3
similar_doc = model.docvecs.most_similar('129978')
print(similar_doc)

rw_df['Description'][129978-kag_len]
rw_df['Description'][130693-kag_len]

rw_df.loc[129977-kag_len, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
rw_df.loc[130693-kag_len, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']]
# Not really


# Test 4
rw_df_num = 4
total_num = kag_len + rw_df_num
display_num = 100
similar_doc = model.docvecs.most_similar(str(total_num), topn=display_num)
print(similar_doc)
sim_found_num = 130994

print(rw_df['Description'][rw_df_num])
print('\n')
print(rw_df['Description'][sim_found_num-kag_len])

print(rw_df.loc[rw_df_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
print('\n')
print(rw_df.loc[sim_found_num-kag_len, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
# different


# Test 5
rw_df_num = 5
total_num = kag_len + rw_df_num
display_num = 100
similar_doc = model.docvecs.most_similar(str(total_num), topn=display_num)
print(similar_doc)
sim_found_num = 132370

print(rw_df['Description'][rw_df_num])
print('\n')
print(rw_df['Description'][sim_found_num-kag_len])

print(rw_df.loc[rw_df_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
print('\n')
print(rw_df.loc[sim_found_num-kag_len, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
# different


# Test 6
rw_df_num = 6
total_num = kag_len + rw_df_num
display_num = 100
similar_doc = model.docvecs.most_similar(str(total_num), topn=display_num)
print(similar_doc)
sim_found_num = int(similar_doc[0][0])
similar_doc[0][1]

if sim_found_num < kag_len:

    print(rw_df['Description'][rw_df_num])
    print('\n')
    print(kag_df_essential['description'][sim_found_num])
    
    print(rw_df.loc[rw_df_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
    print('\n')
    print(kag_df_essential.loc[sim_found_num, ['region_1', 'province', 'country', 'variety', 'winery']])
else:
    print(rw_df['Description'][rw_df_num])
    print('\n')
    print(rw_df['Description'][sim_found_num-kag_len])
    
    print(rw_df.loc[rw_df_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
    print('\n')
    print(rw_df.loc[sim_found_num-kag_len, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
# different


# calculate average similarity score
similarity_score_list = []
for idx in range(0, total_len, 100):
    if np.mod(idx,1000)==0:
        print(idx)
    similar_doc = model.docvecs.most_similar(str(idx))
    similarity_score_list.append(float(similar_doc[0][1]))

similarity_score_mean = np.mean(similarity_score_list)
print(similarity_score_mean)

# similarity score are quite low - 0.534


#t-sne
# =============================================================================
# doc_tags = list(model.docvecs.doctags.keys())
# X = model[doc_tags]
# 
# tsne = TSNE(n_components=2)
# X_tsne = tsne.fit_transform(X)
# df = pd.DataFrame(X_tsne, index=doc_tags, columns=['x', 'y'])
# 
# # Pinot Grigio
# plotScatter(keyword="Pinot Grigio")
# 
# 
# # another version
# X = model.wv[model.wv.vocab]
# 
# tsne = TSNE(n_components=2)
# X_tsne = tsne.fit_transform(X)
# 
# plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
# plt.show()
# 
# =============================================================================


