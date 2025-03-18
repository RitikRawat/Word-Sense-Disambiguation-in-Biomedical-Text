#!/usr/bin/env python
# coding: utf-8

# In[106]:


MSH = []


# In[107]:


NLM=[]
with open('NLM.txt', 'r') as f:
     lines = f.readlines()
     for line in lines:
        NLM.append(line.split('\n')[0])


# In[108]:


with open('MSH WSD/benchmark_mesh.txt', 'r') as f:
     lines = f.readlines()
     for line in lines:
        MSH.append(line.split('\t')[0])


# In[109]:


Prof = []


# In[110]:


with open('Professor_list.txt', 'r') as f:
     lines = f.readlines()
     for line in lines:
        Prof.append(line.split(' ')[0])


# In[111]:


Prof = [x.replace('\n','') for x in Prof]


# In[112]:


Prof = list(set(Prof))


# In[113]:


len(MSH)


# In[114]:


len(Prof)


# In[115]:


len(NLM)


# In[116]:


terms = []


# In[117]:


for word in MSH:
    if len(word)>3:
        terms.append(word)


# In[118]:


terms


# In[119]:


len(terms)


# In[120]:


terms.extend(Prof)


# In[121]:


terms.extend(NLM)


# In[122]:


len(terms)


# In[123]:


terms = [(" " + x + " ").lower() for x in terms]


# In[124]:


terms.sort()


# In[126]:


from collections import Counter
[k for k,v in Counter(terms).items() if v>1]


# In[97]:


terms= list(set(terms))


# In[125]:


len(terms)


# In[102]:


with open('term_f_corpus.pkl', 'rb') as f:
    term_f = pickle.load( f)


# In[104]:


for term in term_f:
    if term not in terms:
        print(term)


# In[1]:


import pandas as pd
import xml.etree.ElementTree as ET
import spacy
import numpy as np
from pathlib import Path
import itertools
from concurrent.futures import ProcessPoolExecutor
import os
import pickle


# In[11]:


directory = "Processed/"
files = Path(directory).glob('*.txt')
files = list(files)


# In[12]:


top100 = list(itertools.islice(files, 0,100))


# In[13]:


top100.sort()


# In[26]:


zipped = list([top100[0:25],top100[25:50],top100[50:75],top100[75:100]])


# In[27]:


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


# In[28]:


with ProcessPoolExecutor(max_workers=4) as exe:
    results = exe.map(my_function3,zipped)


# In[29]:


k = list(results)


# In[153]:


k


# In[30]:


term_freq = {**k[0],**k[1],**k[2],**k[3]}


# In[31]:


term_freq['228.txt']


# In[32]:


terms_f = {x:0 for x in terms}


# In[33]:


for doc in term_freq:
    lst = term_freq[doc]
    for dic in lst:
        for key in dic:
           terms_f[key]+= dic[key]


# In[95]:


len(terms_f)


# In[ ]:


term_freq['1.txt']


# In[35]:


with open('term_freq.pkl', 'wb') as f:
    pickle.dump(term_freq, f)


# In[99]:


with open('term_f_corpus.pkl', 'wb') as f:
    pickle.dump(terms_f, f)


# In[10]:


with open('tokens_final.pkl', 'rb') as f:
    MWE = pickle.load(f)


# In[4]:


with open('mwe_100000.pkl', 'rb') as f:
    top100000 = pickle.load(f)


# In[3]:


with open('term_freq.pkl', 'rb') as f:
    term_freq = pickle.load(f)


# In[168]:


top50000


# In[14]:


my_files = [os.path.basename(file) for file in top100]


# In[5]:


i=0
mwe_dict = {}
for key in top100000:
    mwe_dict[key] = i
    i=i+1


# In[33]:


i=0
term_dict = {}
for key in set(terms):
    term_dict[key] = i
    i=i+1


# In[39]:


mwe_dict['following discharge']


# In[7]:


term_freq


# In[205]:


mwe_dict['catch - up']


# In[54]:


matrix = np.zeros((len(mwe_dict),len(term_dict)))


# In[199]:


matrix[3,552]


# In[58]:


len(mwe_dict)


# In[59]:


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


# In[60]:


reverse_dict_mwe = {mwe_dict[k]:k for k in mwe_dict.keys()}
reverse_dict_terms = {term_dict[k]:k for k in term_dict.keys()}


# In[61]:


matrix


# In[62]:


clusters = []
with open('out.output_100000.tsv.I35', 'r') as f:
     lines = f.readlines()
     for line in lines:
        clusters.append(line.split('\t'))


# In[49]:


for i in range(-20,-1):
    print(len(clusters[i]))


# In[63]:


def weird_division(n, d):
    return n / d if d else 0


# In[72]:


term_cluster = {}


# In[65]:


for col in range(matrix.shape[1]):
    arr = matrix[:,col]
    term_cluster[reverse_dict_terms[col]] = []
    for cluster in clusters:
        s = 0
        for mwe in cluster:
            if mwe in mwe_dict:
                s+=(arr[mwe_dict[mwe]])
        s = weird_division(s,len(cluster))
        term_cluster[reverse_dict_terms[col]].append(s)


# In[ ]:


term cluste


# In[73]:


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


# In[252]:


term_cluster['arm']


# In[74]:


term_cluster[' japanese ']


# In[88]:


np.argsort(term_cluster[' cold '])[-10:]


# In[92]:


clusters[773]


# In[292]:


sorted_term_cluster = {}


# In[293]:


for key in term_cluster:
   sorted_term_cluster[key] = sorted(term_cluster[key], reverse=True)


# In[300]:


sorted_term_cluster[' cold ']


# In[238]:


mwe_dict


# In[246]:


overall =0
for cluster in clusters:
    for mwe in cluster:
        if mwe not in top50000:
            overall+=1


# In[247]:


overall


# In[75]:


with open('term_cluster_final.pkl', 'wb') as f:
    pickle.dump(term_cluster, f)


# In[5]:


with open('term_cluster.pkl', 'rb') as f:
    term_cluster = pickle.load(f)


# In[51]:


with open('clusters100000.pkl', 'wb') as f:
        pickle.dump(clusters,f)


# In[ ]:




