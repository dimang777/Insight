import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np
from timeit import default_timer as timer
from sklearn.model_selection import train_test_split


# Training doc2vec model iteration 3
# Changed strategy to work with smaller data set (i.e., LCBO df)
# Larger dataset is hard to iterate and visualize using t-sne (takes long time)
# Observations so far
# tags not very useful especially there is no clear label
# window size of 5 seems to capture the doc structure more than key words
# Need to focus on keywords so reduce the window size. Trying 2.
# Because of the smaller data set, reduce the vector size to 25
# Use lemmatization to make the distribution denser.
# Previous model had overall lower similarity score (0.534)
# Set train and test data
rw_mod_desc = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_mod_desc.pkl')
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v2.xlsx')
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
vec_size = 50
alpha = 0.025
window_size = 2
num_workers = 4
minimun_count = 1
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

model.save('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/v2_lcbo_d2v_50vec_2win_lemma.model')
model.save('C:/Users/diman/OneDrive/Work_temp/Insight/LargeModels/v2_lcbo_d2v_50vec_2win_lemma.model')
print('Model Saved')

model= Doc2Vec.load('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/models/v2_lcbo_d2v_50vec_2win_lemma.model')



desc_idx_train

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


# Test 4
indices_w_high_score = []
for count, idx in enumerate(desc_idx_train):
    if idx != 1859 and idx != 2696:
        rw_df_num = idx
        total_num = rw_df_num
        display_num = 2
        similar_doc = model.docvecs.most_similar(str(total_num), topn=display_num)
        # print(similar_doc)
        if similar_doc[0][1] > 0.75:
            sim_found_num = int(similar_doc[0][0])
            print(similar_doc[0])
            indices_w_high_score.append([count, idx, similar_doc[0]])

same_product = []

item_num = 4
if rw_df['Name'][indices_w_high_score[item_num][1]] != \
    rw_df['Name'][int(indices_w_high_score[item_num][2][0])]:
        rw_df_num = indices_w_high_score[item_num][1]
        sim_found_num = int(indices_w_high_score[item_num][2][0])
else:
    print('same product')
    print(indices_w_high_score[item_num][2][1])
    print(rw_df['Name'][indices_w_high_score[item_num][1]])
    print(rw_df['Name'][int(indices_w_high_score[item_num][2][0])])
    same_product.append([indices_w_high_score[item_num][1], int(indices_w_high_score[item_num][2][0])])
    rw_df_num = indices_w_high_score[item_num][1]
    sim_found_num = int(indices_w_high_score[item_num][2][0])

print(rw_df['Description'][rw_df_num])
print('\n')
print(rw_df['Description'][sim_found_num])

print(rw_df.loc[rw_df_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
print('\n')
print(rw_df.loc[sim_found_num, ['Name', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2', 'Price']])
# different


model.docvecs.similarity('Ontario', '129978')

test_data = desc_token_LCBO[0]
v1 = model.infer_vector(test_data)
print("V1_infer", v1)

# to find most similar doc using tags
similar_doc = model.docvecs.most_similar('129976')
print(similar_doc)


# to find vector of doc in training data using tags or in other words, printing the vector of document at index 1 in training data
print(model.docvecs['1'])

# similarity score are quite low



doc_tags = list(model.docvecs.doctags.keys())
X = model[doc_tags]

tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)
df = pd.DataFrame(X_tsne, index=doc_tags, columns=['x', 'y'])

# Pinot Grigio
plotScatter(keyword="Pinot Grigio")


# another version
X = model.wv[model.wv.vocab]

tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
plt.show()



