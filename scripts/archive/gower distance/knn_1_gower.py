import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def gower_numer_dist(category, idx1, idx2):
    """ numerical distance (dissimilarity) 
    d_i_j_f = |x1 - x2|/(max(X)-min(X))
    print(df[category][idx1], df[category][idx2])"""
    return np.abs(rw_df[category][idx1] - rw_df[category][idx2]) \
    /(rw_df[category].max() - rw_df[category].min())

def gower_qual_dist(category, idx1, idx2):
    """ qualitative distance (dissimilarity) - 1 if different; 0 if same
    print(df[category][idx1], df[category][idx2]) """
    return int(rw_df[category][idx1] != rw_df[category][idx2])

def gower_dist(idx):
    """ Gower distance between two products
    Source: https://towardsdatascience.com/clustering-on-mixed-type-data-8bbd0a2569c3
    Source: https://stat.ethz.ch/education/semesters/ss2012/ams/slides/v4.2.pdf
    Input: a list of two indices
    Sample use
    gower_dist([0, 1])"""
    [idx1, idx2] = idx

    categories = ['Price', 'Sugar', 'Alcohol', 'Sweetness', 'Style1', 'Style2', 'Variety', 'Madein_city', 'Madein_country', 'Brand']
    gower_dist_list = []
    for idx in range(3):
        gower_dist_list.append(gower_numer_dist(categories[idx], idx1, idx2))
        
    for idx in range(3,10):
        gower_dist_list.append(gower_qual_dist(categories[idx], idx1, idx2))

    return sum(gower_dist_list)/len(gower_dist_list)



with open('train_val_test.pickle', 'rb') as f:
    desc_idx_train, desc_idx_val, desc_idx_test = pickle.load(f)

desc_idx_test.extend(desc_idx_val)

rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
rw_df.columns
categories = ['Price', 'Sugar', 'Alcohol', 'Sweetness', 'Style1', 'Style2', 'Variety', 'Madein_city', 'Madein_country', 'Brand']



# rw_df.loc[idx, ['Name', 'Price', 'Sugar', 'Alcohol', 'Sweetness', 'Style1', 'Style2', 'Variety', 'Madein_city', 'Madein_country', 'Brand']]
# rw_df.loc[lowest_idx, ['Name', 'Price', 'Sugar', 'Alcohol', 'Sweetness', 'Style1', 'Style2', 'Variety', 'Madein_city', 'Madein_country', 'Brand']]

len(desc_idx_test)
desc_idx_test_pair = []
# Evaluate test set
for count, idx in enumerate(desc_idx_test):
    print(count)
    lowest_idx = -1
    lowest_score = 1000
    for idx_2 in range(len(rw_df)):
        if np.mod(idx_2, 500) == 0:
            print(idx_2)
        if idx_2 != idx:
            dist = gower_dist([idx, idx_2])
        if dist < lowest_score:
            lowest_score = dist
            lowest_idx = idx_2

    desc_idx_test_pair.append(idx_2)
    match_score = []
    for cat_idx, category in enumerate(categories):
        if cat_idx < 3:
            if np.abs(rw_df.loc[idx, category] - rw_df.loc[lowest_idx, category]) < 1:
                match_score.append(1)
            else:
                match_score.append(0)
        else:
            if rw_df.loc[idx, category] == rw_df.loc[lowest_idx, category]:
                match_score.append(1)
            else:
                match_score.append(0)
    if desc_idx_test.index(idx) == 0:
        match_score_indi_df = pd.DataFrame({'Name':idx, 'Score':[match_score]})
        match_score_sum_df = pd.DataFrame({'Name':idx, 'Score':[sum(match_score)]})
    else:
        match_score_indi_df = pd.concat([match_score_indi_df, pd.DataFrame({'Name':idx, 'Score':[match_score]})], ignore_index = True)
        match_score_sum_df = pd.concat([match_score_sum_df, pd.DataFrame({'Name':idx, 'Score':[sum(match_score)]})], ignore_index = True)


match_score_sum_df.to_excel('Gower_similarity.xlsx')

match_score_percent = match_score_sum_df.mean()[1]/10
print(match_score_percent)

