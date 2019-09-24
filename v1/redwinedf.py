import pandas as pd
import numpy as np

class RedWineDF:
    def __init__(self, exceltoload):
      self.__df = pd.read_excel(exceltoload)

    def _gower_numer_dist(self, category, idx1, idx2):
    # numerical distance (dissimilarity) 
    # d_i_j_f = |x1 - x2|/(max(X)-min(X))
        # print(df[category][idx1], df[category][idx2])
        return np.abs(self.__df[category][idx1] - self.__df[category][idx2]) \
        /(self.__df[category].max() - self.__df[category].min())

    def _gower_qual_dist(self, category, idx1, idx2):
    # qualitative distance (dissimilarity) - 1 if different; 0 if same
        # print(df[category][idx1], df[category][idx2])
        return int(self.__df[category][idx1] != self.__df[category][idx2])
    
    def _gower_dist(self, idx):
        # Gower distance between two products
        # Source: https://towardsdatascience.com/clustering-on-mixed-type-data-8bbd0a2569c3
        # Source: https://stat.ethz.ch/education/semesters/ss2012/ams/slides/v4.2.pdf
        # input: a list of two indices
        # Sample use
        # _gower_dist([0, 1])
        [idx1, idx2] = idx
        categories = ['Price', 'Sugar', 'Alcohol', 'Sweetness', 'Style1', 'Style2', 'Variety']
        gower_dist_list = []
        for idx in range(3):
            gower_dist_list.append(self._gower_numer_dist(categories[idx], idx1, idx2))
            
        for idx in range(3,7):
            gower_dist_list.append(self._gower_qual_dist(categories[idx], idx1, idx2))

        return sum(gower_dist_list)/len(gower_dist_list)
    
    def get_idx_w_id(self, id_to_find):
        # Returns the index of a product with id_to_find
        # Input: id_to_find - string - e.g., L806, V100221
        # Output: index within the df

        return int(self.__df[self.__df['LCBO_id']==id_to_find].index[0])

    def get_recommendations(self, product_idx_or_id):
        # Gower distance between for all pairs given a product
        # Input: index or id of the product
        # Output: a list of three product indices for recommendation
        # Sample use
        # get_recommendations(product_idx)

        # If the input is id, convert it to index
        if isinstance(product_idx_or_id, str):
            product_idx = self.get_idx_w_id(product_idx_or_id)
        elif isinstance(product_idx_or_id, int):
            product_idx = product_idx_or_id


        for idx in range(len(self.__df)):
            if product_idx != idx:
                if not np.mod(idx, 200):
                    print(str(int(idx/len(self.__df)*100)) + '%')
                elif idx+1 == len(self.__df):
                    print('100%')
                
                columns = ('Num', 'Gower_dist')
                data = {}   
        
            data[columns[0]] = [idx]
            data[columns[1]] = [self._gower_dist((product_idx, idx))]
        
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

        return tuple(recommedation_list)

    def display_product(self, idx):
        columns_to_show = ['LCBO_id', 'Name', 'Price', 'Sugar', 'Alcohol', 'Sweetness', 'Style1', 'Style2', 'Variety']
        print(self.__df.loc[idx, columns_to_show])

    def display_columns(self):
        print(self.__df.head())

    def get_productinfo_in_dict(self, idx):
        columns_to_show = ['LCBO_id', 'Name', 'Price', 'Sugar', 'Alcohol', 'Sweetness', 'Style1', 'Style2', 'Variety']

        values = self.__df.loc[idx, columns_to_show]

        data = {}
        for i, column in enumerate(columns_to_show):
            data[column] = values[i]

        return data


if __name__ == '__main__':

    product_idx = 1
    rw_df_mvp = RedWineDF('rw_df_mvp.xlsx')

    # recommedations = rw_df_mvp.get_recommendations(1)


    # rw_df_mvp.display_product(product_idx)
    # rw_df_mvp.display_product(recommedations[0])
    # rw_df_mvp.display_product(recommedations[1])
    # rw_df_mvp.display_product(recommedations[2])

    list(rw_df_mvp.get_productinfo_in_dict(product_idx).keys())[0]
    list(rw_df_mvp.get_productinfo_in_dict(product_idx).items())[0]
    list(rw_df_mvp.get_productinfo_in_dict(product_idx).values())[0]

    # recommedations = rw_df_mvp.get_recommendations('L419945')
    # rw_df_mvp.display_product(rw_df_mvp.get_idx_w_id('L419945'))
    # rw_df_mvp.display_product(recommedations[0])
    # rw_df_mvp.display_product(recommedations[1])
    # rw_df_mvp.display_product(recommedations[2])
