import pandas as pd
import numpy as np
import itertools

def gower_numer_dist(df, category, idx1, idx2):
# numerical distance (dissimilarity) 
# d_i_j_f = |x1 - x2|/(max(X)-min(X))
    # print(df[category][idx1], df[category][idx2])
    return np.abs(df[category][idx1] - df[category][idx2]) \
    /(df[category].max() - df[category].min())
    
def gower_qual_dist(df, category, idx1, idx2):
# qualitative distance (dissimilarity) - 1 if different; 0 if same
    # print(df[category][idx1], df[category][idx2])
    return int(df[category][idx1] != df[category][idx2])
    
def gower_dist(df, idx):
    # Gower distance
    # Source: https://towardsdatascience.com/clustering-on-mixed-type-data-8bbd0a2569c3
    # Source: https://stat.ethz.ch/education/semesters/ss2012/ams/slides/v4.2.pdf
    # Sample use
    # gower_dist(rw_df_mvp, [0, 1])
    [idx1, idx2] = idx
    categories = ['Price', 'Sugar', 'Alcohol', 'Sweetness', 'Style1', 'Style2', 'Variety']
    gower_dist_list = []
    for idx in range(3):
        gower_dist_list.append(gower_numer_dist(df, categories[idx], idx1, idx2))
        
    for idx in range(3,7):
        gower_dist_list.append(gower_qual_dist(df, categories[idx], idx1, idx2))
    # print(gower_dist_list)
    return sum(gower_dist_list)/len(gower_dist_list)

rw_df_mvp = pd.read_excel('rw_df_mvp.xlsx')

# sample space
    
# =============================================================================
# for idx, pair in enumerate(itertools.combinations(range(len(rw_df_mvp)),2)):
#     print(idx)
#     columns = ('Num0', 'Num1', 'Gower_dist')
#     data = {}   
#     gower_dist_result = gower_dist(rw_df_mvp, pair)
#     
#     data[columns[0]] = [pair[0]]
#     data[columns[1]] = [pair[1]]
#     data[columns[2]] = [gower_dist]
#     
#     if idx == 0:
#         gower_dist_df = pd.DataFrame(data)
#     else:
#         gower_dist_df = pd.concat([gower_dist_df, pd.DataFrame(data)])        
# 
# =============================================================================

columns_to_show = ['Name', 'Price', 'Sugar', 'Alcohol', 'Sweetness', 'Style1', 'Style2', 'Variety']

product_idx = 1
print(rw_df_mvp.loc[product_idx, columns_to_show])

for idx in range(len(rw_df_mvp)):
    if product_idx != idx:
        if not np.mod(idx, 200):
            print(str(int(idx/len(rw_df_mvp)*100)) + '%')
        elif idx+1 == len(rw_df_mvp):
            print('100%')
        
        columns = ('Num', 'Gower_dist')
        data = {}   

    data[columns[0]] = [idx]
    data[columns[1]] = [gower_dist(rw_df_mvp, (product_idx, idx))]

    if idx == 0:
        gower_dist_one = pd.DataFrame(data)
    else:
        gower_dist_one = pd.concat([gower_dist_one, pd.DataFrame(data)])       


gower_dist_one_sorted = gower_dist_one.sort_values(by=['Gower_dist'])
sorted_list_gower = gower_dist_one_sorted['Gower_dist'].to_numpy()

sorted_list_num = gower_dist_one_sorted['Num'].to_numpy()
recommedation_list = []

idx = 0
count = 0
while count < 3:
    # print('idx' + str(idx))
    if sorted_list_gower[idx] != 0:
        # print('count'+str(count))
        recommedation_list.append(sorted_list_num[idx])
        count = count + 1
    idx = idx + 1        

print(rw_df_mvp.loc[product_idx, columns_to_show])
print(rw_df_mvp.loc[recommedation_list[0], columns_to_show])
print(rw_df_mvp.loc[recommedation_list[1], columns_to_show])
print(rw_df_mvp.loc[recommedation_list[2], columns_to_show])


 