#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pathlib import Path
import os
import pandas as pd
import xml.etree.ElementTree as ET
import spacy
import numpy as np
import itertools
from concurrent.futures import ProcessPoolExecutor
import pickle


# In[6]:


terms=[]
with open('Additional Metaphors.txt', 'r') as f:
     lines = f.readlines()
     for line in lines:
        terms.append(line.split('\n')[0])
terms = [(" " + x + " ").lower() for x in terms]


# In[ ]:





# In[3]:


directory = "Processed/"
files = Path(directory).glob('*.txt')
files = list(files)
top100 = list(itertools.islice(files, 0,100))
zipped = list([top100[0:25],top100[25:50],top100[50:75],top100[75:100]])


# In[8]:


def my_function3(files):    
    term_freq ={}
    for file in files:
        name =  os.path.basename(file)
        term_freq[name] = []
        print(f'starting for {name}')
        with open(file,'r') as f:
            lines = f.readlines()
            for line in lines:
                doclst = {}
                m = line.split(' ',1)[1]
                for word in terms:
                    c = m.count(word)
                    if c>0:
                        doclst[word] = c
                term_freq[name].append(doclst)           
    return term_freq


# In[9]:


with ProcessPoolExecutor(max_workers=4) as exe:
    results = exe.map(my_function3,zipped)


# In[10]:


k = list(results)
term_freq = {**k[0],**k[1],**k[2],**k[3]}


# In[11]:


my_files = [os.path.basename(file) for file in top100]


# In[12]:


with open('mwe_100000.pkl', 'rb') as f:
    top100000 = pickle.load(f)
with open('tokens_final.pkl', 'rb') as f:
    MWE = pickle.load(f)


# In[13]:


i=0
mwe_dict = {}
for key in top100000:
    mwe_dict[key] = i
    i=i+1

i=0
term_dict = {}
for key in set(terms):
    term_dict[key] = i
    i=i+1


# In[14]:


matrix = np.zeros((len(mwe_dict),len(term_dict)))


# In[15]:


for file in my_files:
    mwe_lst = MWE[file]
    term_lst = term_freq[file]
    for i in range(0,30000):
        d1 = mwe_lst[i]
        d2 = term_lst[i]
        if (len(d1)>0 and len(d2)>0):
            for mwe in d1:
                if mwe in mwe_dict:
                    for t in d2:
                        matrix[mwe_dict[mwe],term_dict[t]] +=d1[mwe]*d2[t]


# In[16]:


reverse_dict_mwe = {mwe_dict[k]:k for k in mwe_dict.keys()}
reverse_dict_terms = {term_dict[k]:k for k in term_dict.keys()}


# In[17]:


clusters = []
with open('out.output_100000.tsv.I35', 'r') as f:
     lines = f.readlines()
     for line in lines:
        clusters.append(line.split('\t'))


# In[18]:


term_cluster = {}
for col in range(matrix.shape[1]):
    arr = matrix[:,col]
    term_cluster[reverse_dict_terms[col]] = []
    for cluster in clusters:
        s = 0
        for mwe in cluster:
            if mwe in mwe_dict:
                if (arr[mwe_dict[mwe]]>2):
                    s+=1
        term_cluster[reverse_dict_terms[col]].append(s)


# In[19]:


with open('term_cluster_add.pkl', 'wb') as f:
    pickle.dump(term_cluster, f)


# In[20]:


my_dict = {}
for term in term_cluster:
    lst =[]
    for idx,elem in enumerate(term_cluster[term]):
        lst.append(elem/len(clusters[idx]))
    my_dict[term] = lst


# In[21]:


new_dict = {}
for term in my_dict:
    lst=[]
    for idx,elem in enumerate(my_dict[term]):
        if elem >0.5:
            lst.append(idx)
    new_dict[term] = lst


# In[22]:


count =0
for term in new_dict:
    if len(new_dict[term])>1:
        count+=1
print(count)


# In[23]:


part_dict ={}
for term in term_cluster:
    flag = False
    for idx,elem in enumerate(term_cluster[term]):
        if elem >=1:
            flag =True
    part_dict[term] = flag


# In[24]:


count = 0
for term in part_dict:
    if ((part_dict[term] == True)):
        count+=1
print(count)


# In[ ]:




