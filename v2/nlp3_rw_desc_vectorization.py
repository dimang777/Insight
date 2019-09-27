import pandas as pd
import nltk
from nltk.corpus import stopwords
stoplist = set(stopwords.words('english'))
import re
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
# Source: https://github.com/BadreeshShetty/Natural-Language-Processing-NLP-for-Machine-Learning/blob/master/NLP.ipynb

# Vectorization


rw_desc_df_preprocessed_v1 = pd.read_excel('rw_desc_df_preprocessed_v1.xlsx')
rw_desc_df_preprocessed_v1.shape
rw_desc_df_preprocessed_v1.columns
data_count = rw_desc_df_preprocessed_v1.count(axis = 0)
rw_desc_df_preprocessed_v1.count(axis = 0)


# Word to bag

ps = nltk.PorterStemmer()

def clean_text(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [ps.stem(word) for word in tokens if word not in stoplist]
    return text

count_vect = CountVectorizer(analyzer=clean_text)
X_counts = count_vect.fit_transform(rw_desc_df_preprocessed_v1['Description'])
print(X_counts.shape)
print(count_vect.get_feature_names())

X_counts_df = pd.DataFrame(X_counts.toarray(), columns=count_vect.get_feature_names())
X_counts_df.columns
X_counts_df.head(10)


# N-grams

ngram_vect = CountVectorizer(ngram_range=(2,2),analyzer=clean_text) # It applies only bigram vectorizer
X_counts = ngram_vect.fit_transform(rw_desc_df_preprocessed_v1['Description'])
print(X_counts.shape)
print(ngram_vect.get_feature_names())

X_counts_df2 = pd.DataFrame(X_counts.toarray(), columns=ngram_vect.get_feature_names())
X_counts_df2.columns
X_counts_df2.head(10)

# TF-IDF

tfidf_vect = TfidfVectorizer(analyzer=clean_text)
X_tfidf = tfidf_vect.fit_transform(rw_desc_df_preprocessed_v1['Description'])
print(X_tfidf.shape)
print(tfidf_vect.get_feature_names())







