import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np
from timeit import default_timer as timer
from sklearn.model_selection import train_test_split
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Training doc2vec model iteration 3
# Changed strategy to work with smaller data set (i.e., LCBO df)
# Larger dataset is hard to iterate and visualize using t-sne (takes long time)
# Observations so far
# tags not very useful especially there is no clear label
# window size of 5 seems to capture the doc structure more than key words
# Need to focus on keywords so reduce the window size. Trying 2.
# Because of the smaller data set, reduce the vector size to 50
# Use lemmatization to make the distribution denser.
# Previous model had overall lower similarity score (0.534)
# Set train and test data
rw_mod_desc = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_mod_desc.pkl')
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
LCBO_id = rw_df['LCBO_id']
desc_token = list(rw_mod_desc['Cate_attached'])
LCBO_len = len(desc_token)


print(LCBO_len)
print(len(LCBO_id))

total_len = len(desc_token)

# Divide into train, validation, and test sets
desc_train, desc_temp, desc_idx_train, desc_idx_temp = train_test_split(desc_token, range(total_len), test_size=0.20, random_state=0)
desc_val, desc_test, desc_idx_val, desc_idx_test = train_test_split(desc_temp,desc_idx_temp,test_size = 0.5, random_state=0)

print(len(desc_train))
print(len(desc_val))
print(len(desc_test))


tagged_data = []
for idx, entry in zip(desc_idx_train, desc_train):
    print(idx)
    if np.mod(idx,500)==0:
        print(idx)
    tagged_data.append(TaggedDocument(entry, tags=[str(idx)]))


desc_train[0]


max_epochs = 50
vec_size = 25
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

model.save('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/v2_lcbo_d2v_50vec_2win_lemma.model')
model.save('C:/Users/diman/OneDrive/Work_temp/Insight/LargeModels/v2_lcbo_d2v_50vec_2win_lemma.model')
print('Model Saved')

model= Doc2Vec.load('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/v2_lcbo_d2v_50vec_2win_lemma.model')





# Test 1
rw_df_num = desc_idx_train[0]
total_num = rw_df_num
display_num = 10
similar_doc = model.docvecs.most_similar(str(total_num), topn=display_num)
print(similar_doc)
sim_found_num = int(similar_doc[0][0])

print(rw_df['Description'][rw_df_num])
print('\n')
print(rw_df['Description'][sim_found_num])

print(rw_df.loc[rw_df_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
print('\n')
print(rw_df.loc[sim_found_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])



# Test 2
rw_df_num = desc_idx_train[1]
total_num = rw_df_num
display_num = 10
similar_doc = model.docvecs.most_similar(str(total_num), topn=display_num)
print(similar_doc)
sim_found_num = int(similar_doc[0][0])

print(rw_df['Description'][rw_df_num])
print('\n')
print(rw_df['Description'][sim_found_num])

print(rw_df.loc[rw_df_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
print('\n')
print(rw_df.loc[sim_found_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])


# Test 3
rw_df_num = desc_idx_train[2]
total_num = rw_df_num
display_num = 10
similar_doc = model.docvecs.most_similar(str(total_num), topn=display_num)
print(similar_doc)
sim_found_num = int(similar_doc[0][0])

print(rw_df['Description'][rw_df_num])
print('\n')
print(rw_df['Description'][sim_found_num])

print(rw_df.loc[rw_df_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
print('\n')
print(rw_df.loc[sim_found_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])


# calculate average similarity score
similarity_score_list = []
for idx in desc_idx_train:
    if np.mod(idx,1000)==0:
        print(idx)
    similar_doc = model.docvecs.most_similar(str(idx))
    similarity_score_list.append(float(similar_doc[0][1]))

similarity_score_mean = np.mean(similarity_score_list)
print(similarity_score_mean)

# 0.62


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
print(match_score_percent)




