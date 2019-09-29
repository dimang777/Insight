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
    text = [word for word in tokenized_list if word not in stoplist] # To remove all stopwords
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
    rw_mod_desc = pd.read_excel('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_mod_desc.xlsx')
    rw_mod_desc['Desc_nopunct'] = rw_mod_desc['Description'].\
        apply(lambda x: remove_punct(x))

    # Tokenize
    #We convert to lower as Python is case-sensitive.
    rw_mod_desc['Desc_tokenized'] = rw_mod_desc['Desc_nopunct'].\
        apply(lambda x: tokenize(x.lower()))

   # Remove stop words
    rw_mod_desc['Desc_nostop'] = rw_mod_desc['Desc_tokenized'].\
        apply(lambda x: remove_stopwords(x))

    # Stemmer
    rw_mod_desc['Desc_stemmed'] = rw_mod_desc['Desc_nostop'].\
        apply(lambda x: stemming(x))

    # Lemmatizing
    rw_mod_desc['Desc_lemmatized'] = rw_mod_desc['Desc_stemmed'].\
        apply(lambda x: lemmatizing(x))

    rw_mod_desc.to_pickle('C:/Users/diman/OneDrive/Work_temp/Insight/Git_Workspace/data/cleaned/rw_desc_df_prepro.pkl')
    # Saving to excel completely ruins the dataframe and list of strs




