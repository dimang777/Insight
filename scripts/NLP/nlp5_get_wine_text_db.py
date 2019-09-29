import pandas as pd
import nltk
import re
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


kag_df_raw = pd.read_excel('../data/raw/winemag-data-130k-v2.xlsx')

kag_df_raw.columns
kag_df_essential = kag_df_raw[['country', 'description', 'points', 'province',\
                               'region_1', 'variety', 'winery']]
kag_df_description = kag_df_raw['description']


kag_df_essential.to_excel('../data/cleaned/kag_df_essential.xlsx')
kag_df_description.to_excel('../data/cleaned/kag_df_description.xlsx')




