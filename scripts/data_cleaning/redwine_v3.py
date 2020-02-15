import pandas as pd

class RedWine:
    def __init__(self, pkltoload, hashtablepkl):
        """
        Use pickle to load
        Example: rw_mvp = RedWine('rw_df_mvp_v2.xlsx')

        """
        self.__df = pd.read_pickle(pkltoload)
        self.__df_hashtable = pd.read_pickle(hashtablepkl)

    def get_idx_w_id(self, id_to_find):
        """
        Returns the index of a product with id_to_find
        Input: id_to_find - string - e.g., L806, V100221
        Output: index within the df
        Example: rw_df_mvp.get_productinfo_in_dict(rw_df_mvp.get_idx_w_id('L419945'))
        """

        return int(self.__df[self.__df['LCBO_id']==id_to_find].index[0])

    def get_recommendations(self, product_idx_or_id, price_range = -1):
        """
        cosine similarity between for all pairs given a product - access hash table
        Input: id of the product
        Output: a list of three product indices for recommendation
        Examples
        1. get_recommendations(product_idx)
        2. recommedations, sorted_list = rw_mvp.get_recommendations(product_idx, True)
        """
        # If the input is id, convert it to index
        if isinstance(product_idx_or_id, str):
            product_idx = self.get_idx_w_id(product_idx_or_id)
        elif isinstance(product_idx_or_id, int):
            product_idx = product_idx_or_id

        withinrange_flag = True # Searching within range or range is not set
        if price_range == -1:
            use_pricerange_flag = False
            recommedation_list = list(self.__df_hashtable[product_idx].sort_values().index[1:4])
        else:
            # Generate recommendations
            use_pricerange_flag = True
            range_selected = price_range

            price_entered = self.__df.loc[product_idx, 'Price']
            dist_sorted_df = self.__df_hashtable[product_idx].sort_values()
            price_sorted_df = self.__df.loc[dist_sorted_df.index, 'Price']
        
            # When the items within the range are less then 4 including the input wine,
            # ignore the range. Look at the closest 30 items. 30 is an assumption that
            # there are at least 30 same varietals
            if sum(price_sorted_df.head(30).between(price_entered - range_selected, price_entered + range_selected)) < 4 and use_pricerange_flag:
                withinrange_flag = False
                recommedation_list = list(dist_sorted_df.index[1:4])
        
            else:
                recommedation_list = list(dist_sorted_df[price_sorted_df.between(price_entered - 10, price_entered + 10)].index[1:4])

        return withinrange_flag, tuple(recommedation_list)

    def check_ifavailable(self, product_idx_or_id):
        """
        Check if the input product is in database
        Input: id of the product
        Output: boolean on whether the id is found in the database
        """

        if product_idx_or_id in list(self.__df['LCBO_id']):
            return True
        else:
            return False

    def get_product_info(self, idx):
        """
        Example: rw_df_mvp.get_productinfo_in_dict(rw_df_mvp.get_idx_w_id('L419945'))
        """
        columns_to_show = ['LCBO_id', 'Price', 'Name', 'Size', 'Alcohol',
       'Madein_city', 'Madein_country', 'Brand', 'Sugar', 'Sweetness',
       'Style1', 'Style2', 'Variety', 'URL','Pic_src']
        print(self.__df.loc[idx, columns_to_show])

    def get_columns(self):
        """
        Example: rw_mvp = RedWine('rw_df_mvp_v2.xlsx')
                 rw_mvp.get_columns()

        """
        print(self.__df.columns)

    def get_productinfo_in_dict(self, idx):
        columns_to_show = ['LCBO_id', 'Price', 'Name', 'Size', 'Alcohol',
       'Madein_city', 'Madein_country', 'Brand', 'Sugar', 'Sweetness',
       'Style1', 'Style2', 'Variety', 'URL','Pic_src']

        values = self.__df.loc[idx, columns_to_show]

        data = {}
        for i, column in enumerate(columns_to_show):
            data[column] = values[i]

        return data

    def get_url(self, idx):
        return self.__df['URL'][idx]

    def get_pic_src(self, idx):
        return self.__df['Pic_src'][idx]


if __name__ == '__main__':
    None
    # Test code
    rw = RedWine('./rw_df_mvp_v3.pkl', './winetales_cos_dist_df_v2.pkl')
    rw.get_productinfo_in_dict(rw.get_idx_w_id('L419945'))
    rw.get_productinfo_in_dict(rw.get_idx_w_id('L68924'))
    rw.check_ifavailable('L68924')
