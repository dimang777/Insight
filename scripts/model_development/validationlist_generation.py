""" This file generates the 100 questions for the validation of the product
"""
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import numpy as np
import random



# Import dataframes
rw_df = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/for_models/rw_df_mvp_v3.xlsx')
winetales_cos_dist_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/LargeData/winetales_cos_dist_df_v2.pkl')
winetales_df = pd.read_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/winetales_df.pkl')
with open('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/weight_vec.pkl', 'rb') as handle:
    [weight_vec] = pickle.load(handle)
total_len = winetales_df.shape[0]

_, desc_temp, desc_idx_train, desc_idx_temp = train_test_split(range(total_len), range(total_len), test_size=0.20, random_state=0)
_, _, desc_idx_val, desc_idx_test = train_test_split(desc_temp,desc_idx_temp,test_size = 0.5, random_state=0)
desc_idx_train.extend(desc_idx_val)



# Products from the test set to generate recommendations
random.seed(0)
desc_idx_test_rand100 = random.sample(range(len(desc_idx_test)), 100)
validation100_input_idx = [desc_idx_test[i] for i in desc_idx_test_rand100]

# Random products to be used for the multiple choice options
random.seed(1)
desc_idx_train_rand200 = random.sample(range(len(desc_idx_train)), 200)
random200_idx = [desc_idx_train[i] for i in desc_idx_train_rand200]

# Generate the position of the answers
random.seed(2)
# mod is add just to create more variability in the answers
question_answers = [np.mod(random.randint(1,6),3) for idx in range(100)]


# Generate recommendations
use_pricerange_flag = True
withinrange_flag = True
range_selected = 10
validation100_recomm_list = []
for input_idx in validation100_input_idx:
    winetales_cos_dist_df[input_idx].sort_values().index
    price_entered = rw_df.loc[input_idx, 'Price']
    dist_sorted_df = winetales_cos_dist_df[input_idx].sort_values()
    price_sorted_df = rw_df.loc[dist_sorted_df.index, 'Price']

    # When the items within the range are less then 4 including the input wine,
    # ignore the range. Look at the closest 30 items. 30 is an assumption that
    # there are at least 30 same varietals
    if sum(price_sorted_df[:30].between(price_entered - range_selected, price_entered + range_selected)) < 4 and use_pricerange_flag:
        withinrange_flag = False
        validation100_recomm_list.append(list(dist_sorted_df.index[1:4]))

    else:
        validation100_recomm_list.append(list(\
            dist_sorted_df[price_sorted_df.between(price_entered - 10, price_entered + 10)].index[1:4]))

# Generate a text file of questionnaire
with open('Validation Questions.txt', 'w', encoding='utf-8') as text_file:
    for idx in range(len(validation100_input_idx)):
        print('\nQuestion '+str(idx+1)+'\n', file=text_file)
        for recomm_idx in range(3):
            print('\nWine ' + str(recomm_idx+1)+'\n', file=text_file)
            print(rw_df.loc[validation100_recomm_list[idx][recomm_idx] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']], file=text_file)
        # mix up the answer and the random choices
        if question_answers[idx] == 0:
            print('\nA)'+'\n', file=text_file)
            print(rw_df.loc[validation100_input_idx[idx] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']], file=text_file)
            print('\nB)'+'\n', file=text_file)
            print(rw_df.loc[random200_idx[idx*2] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']], file=text_file)
            print('\nC)'+'\n', file=text_file)
            print(rw_df.loc[random200_idx[idx*2+1] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']], file=text_file)
        elif question_answers[idx] == 1:
            print('\nA)'+'\n', file=text_file)
            print(rw_df.loc[random200_idx[idx*2] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']], file=text_file)
            print('\nB)'+'\n', file=text_file)
            print(rw_df.loc[validation100_input_idx[idx] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']], file=text_file)
            print('\nC)'+'\n', file=text_file)
            print(rw_df.loc[random200_idx[idx*2+1] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']], file=text_file)
        else:
            print('\nA)'+'\n', file=text_file)
            print(rw_df.loc[random200_idx[idx*2] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']], file=text_file)
            print('\nB)'+'\n', file=text_file)
            print(rw_df.loc[random200_idx[idx*2+1] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']], file=text_file)
            print('\nC)'+'\n', file=text_file)
            print(rw_df.loc[validation100_input_idx[idx] , ['Name', 'LCBO_id', 'Madein_country', 'Madein_city', 'Variety', 'Sugar', 'Alcohol', 'Brand', 'Style1', 'Style2']], file=text_file)


