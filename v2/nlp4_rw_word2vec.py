import pandas as pd
import nltk
from nltk.corpus import stopwords
stoplist = set(stopwords.words('english'))
import re
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer



# Word2Vec
rw_desc_df_raw_v1 = pd.read_pickle('rw_desc_df_raw_v1.pkl')

# rw_desc_df_preprocessed_v1 = pd.read_excel('rw_desc_df_preprocessed_v1.xlsx')
rw_df = pd.read_excel('rw_df_mvp_v2.xlsx')
rw_df.shape

rw_desc_df_raw_v1 ['Desc_lemmatized'][0][10]
desc_token = list(rw_desc_df_raw_v1 ['Desc_lemmatized'])

desc_token[200]
names = rw_df['Name'][2]
rw_desc_df_raw_v1['Desc_lemmatized'].str.len().mean()

len(desc_token)
len(desc_token[1][2])


if False:
    from gensim.models import Word2Vec
    model_rw = Word2Vec(sentences=desc_token, size=25, window=5, min_count=2, workers=4, sg=1)
else:
    from gensim.models import FastText
    model_rw = FastText(sentences=desc_token, size=25, window=5, min_count=2, workers=4,sg=1)

model_rw.similarity('12 Linajes Reserva 2012', '13th Street Burger Blend Gamay Pinot Noir VQA')

model_rw.save("word2vec_model_test.model")

# model_rw_load = Word2Vec.load("word2vec_model_test.model")

model_rw.wv.most_similar('dri fruit')
model_rw.wv.vectors.shape


len(model_rw.wv.vocab)
model_rw.wv.vocab

model_rw.vocabulary
model_rw.wv.similarity('dri', 'fruit')

