#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import xml.etree.ElementTree as ET
import spacy
import numpy as np
from pathlib import Path
import os


# In[18]:


files = Path("Tokens/").glob('*.txt')


# In[19]:


freq ={}


# In[20]:


curr =0
for file in files:
    curr+=1
    name =  os.path.basename(file)
    with open(file,'r') as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split()
            for token in tokens:
                if token in freq:
                    freq[token]+=1
                else:
                    freq[token] =1
    print(f'{curr} : {name}')


# In[21]:


len(freq)


# In[25]:


freq = {k: v for k, v in sorted(freq.items(), key=lambda item: item[1],reverse=True)}


# In[27]:


del freq['-']


# In[30]:


freq


# In[37]:


terms =[]
for idx,key in enumerate(freq):
    terms.append(key)
    if idx==49999:
        break


# In[38]:


terms


# In[ ]:





# In[39]:


terms = [(" " + x + " ").lower() for x in terms]


# In[2]:


import pandas as pd
import xml.etree.ElementTree as ET
import spacy
import numpy as np
from pathlib import Path
import itertools
from concurrent.futures import ProcessPoolExecutor
import os
import pickle


# In[41]:


directory = "Processed/"
files = Path(directory).glob('*.txt')
files = list(files)


# In[42]:


top100 = list(itertools.islice(files, 0,100))


# In[45]:


zipped = list([top100[0:25],top100[25:50],top100[50:75],top100[75:100]])


# In[46]:


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


# In[47]:


with ProcessPoolExecutor(max_workers=4) as exe:
    results = exe.map(my_function3,zipped)


# In[48]:


k = list(results)
term_freq = {**k[0],**k[1],**k[2],**k[3]}


# In[67]:


with open('term_freq_50000.pkl', 'wb') as f:
    pickle.dump(term_freq, f)


# In[61]:


my_files = [os.path.basename(file) for file in top100]


# In[60]:


my_files


# In[50]:


with open('mwe_100000.pkl', 'rb') as f:
    top100000 = pickle.load(f)


# In[51]:


with open('tokens_final.pkl', 'rb') as f:
    MWE = pickle.load(f)


# In[52]:


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


# In[62]:


matrix = np.zeros((len(mwe_dict),len(term_dict)))


# In[63]:


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


# In[64]:


reverse_dict_mwe = {mwe_dict[k]:k for k in mwe_dict.keys()}
reverse_dict_terms = {term_dict[k]:k for k in term_dict.keys()}


# In[4]:


clusters = []
with open('out.output_100000.tsv.I35', 'r') as f:
     lines = f.readlines()
     for line in lines:
        clusters.append(line.split('\t'))


# In[66]:


term_cluster = {}


# In[68]:


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


# In[69]:


with open('term_cluster_50000.pkl', 'wb') as f:
    pickle.dump(term_cluster, f)


# In[70]:


with open('terms_50000.pkl', 'wb') as f:
    pickle.dump(terms, f)


# In[ ]:





# In[3]:


with open('term_cluster_50000.pkl', 'rb') as f:
    term_cluster = pickle.load(f)


# In[5]:


my_dict = {}
for term in term_cluster:
    lst =[]
    for idx,elem in enumerate(term_cluster[term]):
        lst.append(elem/len(clusters[idx]))
    my_dict[term] = lst


# In[6]:


new_dict = {}
for term in my_dict:
    lst=[]
    for idx,elem in enumerate(my_dict[term]):
        if elem >0.5:
            lst.append(idx)
    new_dict[term] = lst


# In[8]:


count =0
for term in new_dict:
    if len(new_dict[term])>1:
        count+=1
print(count)


# In[9]:


part_dict ={}
for term in term_cluster:
    flag = False
    for idx,elem in enumerate(term_cluster[term]):
        if elem >=1:
            flag =True
    part_dict[term] = flag


# In[11]:


count = 0
for term in part_dict:
    if ((part_dict[term] == True)):
        count+=1
print(count)


# In[12]:


25642/49674


# In[ ]:


terms = []

