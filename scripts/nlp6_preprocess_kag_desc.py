import pandas as pd
from nlp2_rw_description_preprocess import remove_punct, tokenize, remove_stopwords, stemming, lemmatizing



kag_desc_prepro = pd.read_excel('../data/cleaned/kag_df_description.xlsx')

# Code used for exception handling
to_correct = []
if 0:
    for idx in range(len(kag_desc_prepro['description'])):
        if type(kag_desc_prepro['description'][idx]) == int:
            print(idx)
            to_correct.append(idx)
        if type(kag_desc_prepro['description'][idx]) == float:
            print(idx)
            to_correct.append(idx)

# Exception handling
kag_desc_prepro['description'][18882] = ''
kag_desc_prepro['description'][51398] = ''

kag_desc_prepro['Desc_nopunct'] = kag_desc_prepro['description'].apply(lambda x: remove_punct(x))

kag_desc_prepro['Desc_tokenized'] = kag_desc_prepro['Desc_nopunct'].apply(lambda x: tokenize(x.lower())) #We convert to lower as Python is case-sensitive.

kag_desc_prepro['Desc_nostop'] = kag_desc_prepro['Desc_tokenized'].apply(lambda x: remove_stopwords(x))

kag_desc_prepro['Desc_stemmed'] = kag_desc_prepro['Desc_nostop'].apply(lambda x: stemming(x))

kag_desc_prepro['Desc_lemmatized'] = kag_desc_prepro['Desc_stemmed'].apply(lambda x: lemmatizing(x))

kag_desc_prepro.to_pickle('../data/cleaned/kag_desc_prepro.pkl')





