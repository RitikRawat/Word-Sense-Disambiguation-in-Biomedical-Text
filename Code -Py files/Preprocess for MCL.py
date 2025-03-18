#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import pickle
import itertools
import gc
import markov_clustering as mc
from time import perf_counter


# In[2]:


with open('tokens_final.pkl', 'rb') as f:
    MWE = pickle.load(f)


# In[3]:


len(MWE)


# In[9]:


vocab = {}
for f in MWE:
    lst = MWE[f]
    for dic in lst:
        for word in dic:
            if word not in vocab:
                vocab[word] = dic[word]
            else:
                vocab[word] += dic[word]


# In[10]:


vocab = {k: v for k, v in sorted(vocab.items(), key=lambda item: item[1],reverse=True)}


# In[11]:


vocab


# In[16]:


top5000 = {k:vocab[k] for k in list(vocab.keys())[0:5000]}


# In[36]:


with open('mwe_5000.pkl', 'rb') as f:
    top5000 = pickle.load(f)


# In[102]:


with open('mwe_30000.pkl', 'rb') as f:
    top30000 = pickle.load(f)


# In[142]:


with open('mwe_50000.pkl', 'rb') as f:
    top50000 = pickle.load(f)


# In[3]:


with open('mwe_final.pkl', 'rb') as f:
    mwe_final = pickle.load(f)


# In[3]:


vocab = []
for dic in MWE[0:30000]:
    vocab.append(list(dic.keys()))


# In[4]:


vocab = list(set(list(itertools.chain(*vocab))))


# In[6]:


i=0
vocab_dict = {}
for key in mwe_final:
    vocab_dict[key] = i
    i=i+1
    if (i == 100000):
        break


# In[ ]:





# In[11]:


matrix = np.zeros((len(vocab_dict),len(vocab_dict)))


# In[9]:


edgelist ={}
for key in vocab_dict:
    edgelist[key] = []


# In[ ]:





# In[147]:


ti = 0
for key in MWE:
    dic_lst = MWE[key]
    for dic in dic_lst:
        if len(dic)>1:
            ti+=1
ti


# In[12]:


for key in MWE:
    dic_lst = MWE[key]
    for dic in dic_lst:
        if len(dic)>1:
            lst = list(dic.keys())
    #         lst2 = []
    #         for token in lst:
    #             if token in vocab_dict:
    #                 lst2.append(token)
    #         if len(lst2)>1:|
            for a, b in itertools.combinations(lst, 2):
                if ((a in vocab_dict) and (b in vocab_dict)):
                    matrix[vocab_dict[a],vocab_dict[b]] += dic[a]*dic[b]
                    matrix[vocab_dict[b],vocab_dict[a]] += dic[a]*dic[b]


# In[9]:


for row in matrix:
    for item in row:
        if item <3:
            item =0


# In[15]:


reverse_dict = {vocab_dict[k]:k for k in vocab_dict.keys()}


# In[14]:


reverse_dict[30011]


# In[19]:


edgelist = []


# In[ ]:


for i in range(len(matrix)):
    for j in range(len(matrix)):
        if matrix[i][j] >0:
            with open("output_100000.tsv",'a') as f:
                f.write(f'{reverse_dict[i]}\t{reverse_dict[j]}\t{matrix[i][j]}\n')
                matrix[i][j] = 0


# In[ ]:


df = pd.DataFrame.from_records(edgelist)


# In[ ]:


print("s\tb")


# In[ ]:


df.head()


# In[ ]:


df.to_csv("output_100000.tsv", sep="\t", index=None,header = False)


# In[1]:


clusters=[]


# In[160]:


with open('out.output_50000.tsv.I30', 'r') as f:
     lines = f.readlines()
     for line in lines:
        clusters.append(line.split('\t'))


# In[116]:


len(list(itertools.chain(*clusters)))


# In[168]:





# In[125]:


len(set(list(itertools.chain(*clusters))))


# In[120]:


mm = set()


# In[121]:


for cluster in clusters:
    for item in cluster:
        if item in mm:
            print(item)
        else:
            mm.add(item)


# In[117]:


clusters[260]


# In[122]:


count =0


# In[123]:


for row in matrix:
    if(sum(row)==0):
        count+=1


# In[124]:


count


# In[20]:


del matrix


# In[25]:


with open('mwe_100000.pkl','wb') as f:
    pickle.dump(mwe_final[0:100000],f)


# In[ ]:




