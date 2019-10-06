import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt




def display_closestwords_tsnescatterplot(model, word, size):
    
    arr = np.empty((0,size), dtype='f')
    word_labels = [word]
    close_words = model.similar_by_word(word)
    arr = np.append(arr, np.array([model[word]]), axis=0)
    for wrd_score in close_words:
        wrd_vector = model[wrd_score[0]]
        word_labels.append(wrd_score[0])
        arr = np.append(arr, np.array([wrd_vector]), axis=0)
        
    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(arr)
    x_coords = Y[:, 0]
    y_coords = Y[:, 1]
    plt.scatter(x_coords, y_coords)
    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.xlim(x_coords.min()+0.00005, x_coords.max()+0.00005)
    plt.ylim(y_coords.min()+0.00005, y_coords.max()+0.00005)
    plt.show()


display_closestwords_tsnescatterplot(model, 'Porsche 718 Cayman', 50)











# 2. https://stackoverflow.com/questions/40581010/how-to-run-tsne-on-word2vec-created-from-gensim



from gensim.models.word2vec import Word2Vec
from sklearn.manifold import TSNE
from sklearn.datasets import fetch_20newsgroups
import re
import matplotlib.pyplot as plt

# download example data ( may take a while)
train = fetch_20newsgroups()

def clean(text):
    """Remove posting header, split by sentences and words, keep only letters"""
    lines = re.split('[?!.:]\s', re.sub('^.*Lines: \d+', '', re.sub('\n', ' ', text)))
    return [re.sub('[^a-zA-Z]', ' ', line).lower().split() for line in lines]

sentences = [line for text in train.data for line in clean(text)]

model = Word2Vec(sentences, workers=4, size=100, min_count=50, window=10, sample=1e-3)

print (model.wv.most_similar('memory'))

X = model.wv[model.wv.vocab]

tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
plt.show()



# 3. https://www.kaggle.com/arthurtok/target-visualization-t-sne-and-doc2vec/notebook
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# Storing the question texts in a list
quora_texts = list(train_rebal["question_text"])



# Creating a list of terms and a list of labels to go with it
documents = [TaggedDocument(doc, tags=[str(i)]) for i, doc in enumerate(quora_texts)]

max_epochs = 100
alpha=0.025
model = Doc2Vec(documents,
                size=10, 
                min_alpha=0.00025,
                alpha=alpha,
                min_count=1,
#                 window=2, 
                workers=4)

# model.build_vocab(documents)

# for epoch in range(max_epochs):
#     print('iteration {0}'.format(epoch))
#     model.train(documents,
#                 total_examples=model.corpus_count,
#                 epochs=model.iter)
#     # decrease the learning rate
#     model.alpha -= 0.0002
#     # fix the learning rate, no decay
#     model.min_alpha = model.alpha

# Creating and fitting the tsne model to the document embeddings
tsne_model = TSNE(n_jobs=4,
                  early_exaggeration=4,
                  n_components=2,
                  verbose=1,
                  random_state=2018,
                  n_iter=300)
tsne_d2v = tsne_model.fit_transform(model.docvecs.vectors_docs)

# Putting the tsne information into sq
tsne_d2v_df = pd.DataFrame(data=tsne_d2v, columns=["x", "y"])
# tsne_tfidf_df.columns = ["x", "y"]
tsne_d2v_df["qid"] = train_rebal["qid"].values
tsne_d2v_df["question_text"] = train_rebal["question_text"].values
tsne_d2v_df["target"] = train_rebal["target"].values

output_notebook()
plot_d2v = bp.figure(plot_width = 800, plot_height = 700, 
                       title = "T-SNE applied to Doc2vec document embeddings",
                       tools = "pan, wheel_zoom, box_zoom, reset, hover, previewsave",
                       x_axis_type = None, y_axis_type = None, min_border = 1)

# colormap = np.array(["#6d8dca", "#d07d3c"])
colormap = np.array(["darkblue", "cyan"])

# palette = d3["Category10"][len(tsne_tfidf_df["asset_name"].unique())]
source = ColumnDataSource(data = dict(x = tsne_d2v_df["x"], 
                                      y = tsne_d2v_df["y"],
                                      color = colormap[tsne_d2v_df["target"]],
                                      question_text = tsne_d2v_df["question_text"],
                                      qid = tsne_d2v_df["qid"],
                                      target = tsne_d2v_df["target"]))

plot_d2v.scatter(x = "x", 
                   y = "y", 
                   color="color",
                   legend = "target",
                   source = source,
                   alpha = 0.7)
hover = plot_d2v.select(dict(type = HoverTool))
hover.tooltips = {"qid": "@qid", 
                  "question_text": "@question_text", 
                  "target":"@target"}

show(plot_d2v)




