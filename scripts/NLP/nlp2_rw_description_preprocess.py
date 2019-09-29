import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
stoplist = set(stopwords.words('english'))
import string
import re
# Source: https://github.com/BadreeshShetty/Natural-Language-Processing-NLP-for-Machine-Learning/blob/master/NLP.ipynb


#Function to remove Punctuation
def remove_punct(text):
    text_nopunct = "".join([char for char in text if char not in string.punctuation])# It will discard all punctuations
    return text_nopunct

# Function to Tokenize words
def tokenize(text):
    tokens = re.split('\W+', text) #W+ means that either a word character (A-Za-z0-9_) or a dash (-) can go there.
    return tokens

# Function to remove Stopwords
def remove_stopwords(tokenized_list):
    text = [word for word in tokenized_list if word not in stoplist]# To remove all stopwords
    return text

def stemming(tokenized_text):
    ps = nltk.PorterStemmer()
    text = [ps.stem(word) for word in tokenized_text]
    return text

def lemmatizing(tokenized_text):
    wn = nltk.WordNetLemmatizer()
    text = [wn.lemmatize(word) for word in tokenized_text]
    return text


if __name__ == '__main__':
    
    # string.punctuation
    rw_desc_df_raw_v1 = pd.read_excel('rw_desc_df_raw_v1.xlsx')
    rw_desc_df_raw_v1['Desc_nopunct'] = rw_desc_df_raw_v1['Description'].\
        apply(lambda x: remove_punct(x))

    # Tokenize
    #We convert to lower as Python is case-sensitive.
    rw_desc_df_raw_v1['Desc_tokenized'] = rw_desc_df_raw_v1['Desc_nopunct'].\
        apply(lambda x: tokenize(x.lower()))

   # Remove stop words
    rw_desc_df_raw_v1['Desc_nostop'] = rw_desc_df_raw_v1['Desc_tokenized'].\
        apply(lambda x: remove_stopwords(x))

    # Stemmer
    rw_desc_df_raw_v1['Desc_stemmed'] = rw_desc_df_raw_v1['Desc_nostop'].\
        apply(lambda x: stemming(x))

    # Lemmatizing
    rw_desc_df_raw_v1['Desc_lemmatized'] = rw_desc_df_raw_v1['Desc_stemmed'].\
        apply(lambda x: lemmatizing(x))

    rw_desc_df_raw_v1.to_pickle('rw_desc_df_prepro.pkl')
    # Saving to excel completely ruins the dataframe and list of strs
    



