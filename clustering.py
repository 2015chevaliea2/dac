#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data = pd.read_csv("amazon_livres.txt", sep="\t", dtype=str, encoding="ISO-8859-1")


# In[3]:


data = data[['ASIN', 'ISBN', 'TITLE', 'AUTHOR', 'PUBLISHER', 'PUBLICATION_DATE', 'PARUTION_ID']]
data = data[data['AUTHOR'].notnull()]
data = data[data['TITLE'].notnull()]
data.rename({'AUTHOR': 'AUTEUR', 'TITLE': 'TITRE'}, axis=1, inplace=True)


# In[4]:


import pre_processing.cleaning
import pre_processing.volume_number_detection
data['author'] = pre_processing.cleaning.clean_df_column(data.AUTEUR)
data['title'] = pre_processing.cleaning.clean_df_column(data.TITRE)


# In[5]:


def remove_short_words(string):
    output = str(string)
    string = string.split()
    output = output.split()
    for word in string:
        if len(word) <= 2:
            output.remove(word)
    return output


# In[6]:


data.drop(columns=['ASIN',
 'ISBN',
 'TITRE',
 'AUTEUR',
 'PUBLISHER',
 'PUBLICATION_DATE',
 'PARUTION_ID'], inplace=True)


# In[7]:


dat = data.copy()


# In[8]:


# enlever les mots de moins de 2 lettres
dat.author = dat.author.apply(lambda x: remove_short_words(x))
dat.title = dat.title.apply(lambda x: remove_short_words(x))


# In[9]:


import numpy as np
import pandas as pd
from tqdm import tqdm

def name_word(data):
    names = dict()
    words = dict()
    freqs = dict()
    for idx, row in data.iterrows():
        l_auth = row.author
        l_tit = row.title
        for auth in l_auth:
            if auth not in names.keys():
                names[auth] = [idx]
            else:    
                names[auth].append(idx)
            for wd in l_tit:
                if wd not in words.keys():
                    words[wd] = [idx]
                else:
                    words[wd].append(idx)
                
                if auth not in freqs.keys():
                    freqs[auth] = {wd: 1}
                else:
                    if wd not in freqs[auth].keys():
                        freqs[auth][wd] = 1
                    else:
                        freqs[auth][wd] += 1

    return names, words, freqs


_, _, names_words = name_word(dat)


# In[10]:


def word_name(data):
    words_names = dict()
    for idx, row in data.iterrows():
        l_auth = row.author
        l_tit = row.title
        for word in l_tit:
            for auth in l_auth:
                if word not in words_names.keys():
                    words_names[word] = {auth: 1}
                else:
                    if auth not in words_names[word].keys():
                        words_names[word][auth] = 1
                    else:
                        words_names[word][auth] += 1
    return words_names


words_names = word_name(dat)


# In[11]:


def name_name(data):
    names = dict()
    for idx, row in data.iterrows():
        l_auth = row.author
        for auth1 in l_auth:
            for auth2 in l_auth:
                if auth1 != auth2:
                    if auth1 not in names.keys():
                        names[auth1] = {auth2: 1}
                    else:
                        if auth2 not in names[auth1].keys():
                            names[auth1][auth2] = 1
                        else:
                            names[auth1][auth2] += 1
    return names

names_names = name_name(dat)


# In[12]:


def word_word(data):
    names = dict()
    for idx, row in data.iterrows():
        l_auth = row.title
        for auth1 in l_auth:
            for auth2 in l_auth:
                if auth1 != auth2:
                    if auth1 not in names.keys():
                        names[auth1] = {auth2: 1}
                    else:
                        if auth2 not in names[auth1].keys():
                            names[auth1][auth2] = 1
                        else:
                            names[auth1][auth2] += 1
    return names

words_words = word_word(dat)


# In[13]:


def create_graph(names_names, words_words, names_words, words_names):
    graph = names_names.copy()
    for word in words_words.keys():
        if word not in graph.keys():
            graph[word] = words_words[word]
        else:
            for wd in words_words[word].keys():
                if wd in graph[word].keys():
                    graph[word][wd] += words_words[word][wd]
                else:
                    graph[word][wd] = words_words[word][wd]
    for word in names_words.keys():
        if word not in graph.keys():
            graph[word] = names_words[word]
        else:
            for wd in names_words[word].keys():
                if wd in graph[word].keys():
                    graph[word][wd] += names_words[word][wd]
                else:
                    graph[word][wd] = names_words[word][wd]
    for word in words_names.keys():
        if word not in graph.keys():
            graph[word] = words_names[word]
        else:
            for wd in words_names[word].keys():
                if wd in graph[word].keys():
                    graph[word][wd] += words_names[word][wd]
                else:
                    graph[word][wd] = words_names[word][wd]
    return graph

graph = create_graph(names_names, words_words, names_words, words_names)


# In[14]:


def remove_diag(graph):
    clean_graph = dict(graph)
    for word in clean_graph.keys():
        if word in clean_graph[word].keys():
            del clean_graph[word][word]
    return clean_graph

clean_graph = remove_diag(graph)


# In[15]:


import pickle
pickle.dump(file=open('graph.pickle', 'wb'), obj=clean_graph)


# In[18]:


def create_word_index(graph):
    out = {}
    i = 0
    for word in graph.keys():
        out[word] = i
        i += 1
    return out

index = create_word_index(clean_graph)

pickle.dump(file=open('index.pickle', 'wb'), obj=index)


# In[19]:


def create_sparse_matrix(clean_graph, index):
    data = []
    row = []
    col = []
    for word in clean_graph.keys():
        for wd in clean_graph[word].keys():
            row.append(index[word])
            col.append(index[wd])
            data.append(clean_graph[word][wd])
    matrix = csr_matrix((data, (row, col)))
    return matrix
matrix = create_sparse_matrix(clean_graph, index)


# In[20]:


from sklearn.decomposition import IncrementalPCA
import pickle

chunk_size = 100
n = matrix.shape[0]

pca = IncrementalPCA(n_components=15, batch_size=100)

for i in range(0, n//chunk_size):
    rows = matrix[i*chunk_size : (i+1)*chunk_size].toarray()
    pca.partial_fit(rows)

pca.fit(matrix)

pickle.dump(file=open('pca.pickle', 'wb'), obj=pca)
pickle.dump(file=open('sparce_matrix.pickle', 'wb'), obj=matrix)
