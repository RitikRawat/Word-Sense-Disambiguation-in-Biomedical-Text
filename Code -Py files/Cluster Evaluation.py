#!/usr/bin/env python
# coding: utf-8

# In[31]:


import pandas as pd
import xml.etree.ElementTree as ET
import spacy
import numpy as np
from pathlib import Path
import itertools
from concurrent.futures import ProcessPoolExecutor
import os
import pickle


# In[32]:


with open('term_cluster_final.pkl', 'rb') as f:
    term_cluster = pickle.load(f)


# In[3]:


with open('clusters100000.pkl', 'rb') as f:
    clusters = pickle.load(f)


# In[4]:


with open('term_f_corpus.pkl', 'rb') as f:
    term_f = pickle.load(f)


# In[33]:


candidates = {}
for term in term_cluster:
    candidates[term] = np.flip(np.argsort(term_cluster[term]))


# In[34]:


candidates


# In[32]:


term_f = {k: v for k, v in sorted(term_f.items(), key=lambda item: item[1],reverse=True)}


# In[33]:


term_f


# In[25]:


candidates[' japanese ']


# In[28]:


[clusters[i] for i in candidates[' oak ']]


# In[500]:


clusters[527]


# In[29]:


len(clusters)


# In[100]:


[len(clusters[i]) for i in range(0,5)]


# In[20]:


np.average([len(clusters[i]) for i in range(len(clusters))])


# In[99]:


np.average([len(clusters[i]) for i in range(5,len(clusters))])


# In[101]:


len([i for i in range(len(clusters)) if len(clusters[i]) ==1])


# In[23]:


np.sum([len(clusters[i]) for i in range(len(clusters))])


# In[501]:


len(term_f)


# In[24]:


term_cluster[' japanese ']


# In[12]:


clusters[578]


# In[38]:


my_dict = {}
for term in term_cluster:
    lst =[]
    for idx,elem in enumerate(term_cluster[term]):
        lst.append(elem/len(clusters[idx]))
    my_dict[term] = lst


# In[56]:


term_cluster[' japanese '][375]


# In[106]:


clusters[1000]


# In[46]:


[1 if x>0.5 else 0 for x in my_dict[' japanese ']].count(1)


# In[42]:


new_dict = {}
for term in my_dict:
    lst=[]
    for idx,elem in enumerate(my_dict[term]):
        if elem >0.5:
            lst.append(idx)
    new_dict[term] = lst


# In[50]:


new_dict[' japanese ']


# In[58]:


count =0
for term in new_dict:
    if len(new_dict[term])>1:
        count+=1


# In[59]:


count


# In[60]:


len(new_dict)


# In[97]:


161/182


# In[67]:


least = { ' synapsis ': 204,
 ' chestnut ': 195,
 ' heregulin ': 169,
 ' louse ': 169,
 ' alligator ': 167,
 ' cardiac pacemaker ': 163,
 ' boom ': 160,
 ' strep ': 156,
 ' pleuropneumonia ': 139,
 ' lymphogranulomatosis ': 136,
 ' arteriovenous anastomoses ': 111,
 ' staph ': 109,
 ' haemophilus ducreyi ': 101}


# In[85]:


count = 0
for term in new_dict:
    if len(new_dict[term])>1:
        count+=1
        print(term)


# In[86]:


count


# In[306]:


len(new_dict[' sex '])


# In[255]:


part_dict ={}
for term in term_cluster:
    flag = False
    for idx,elem in enumerate(term_cluster[term]):
        if elem >=1:
            flag =True
    part_dict[term] = flag


# In[256]:


part_dict


# In[91]:


new_dict[' entitle ']


# In[248]:


count = 0
for term in part_dict:
    if ((part_dict[term] == True) and term_f[term] >100):
        count+=1


# In[249]:


count


# In[257]:


no_appear = []


# In[258]:


for term in list(part_dict):
    if ((part_dict[term] ==False) or term_f[term] <100):
        part_dict.pop(term,None)
        no_appear.append(term)


# In[259]:


len(part_dict)


# In[98]:


len(clusters)


# In[222]:


MSH = []


# In[223]:


with open('MSH WSD/benchmark_mesh.txt', 'r') as f:
     lines = f.readlines()
     for line in lines:
        MSH.append(line.split('\t')[0])


# In[224]:


MSH


# In[225]:


MSH_terms = []
for word in MSH:
    if len(word)>3:
        MSH_terms.append(word)


# In[226]:


len(MSH)


# In[227]:


MSH_terms = [(" " + x + " ").lower() for x in MSH_terms]


# In[169]:


MSH_terms


# In[172]:


for term in MSH_terms:
    if term not in part_dict:
        MSH_terms.remove(term)


# In[242]:


part_dict


# In[241]:


len(MSH_terms)


# In[229]:


count = 0
for term in MSH_terms:
    if len(new_dict[term])>1:
        count+=1
print(count)


# In[178]:


76/88


# In[196]:


NLM=[]
with open('NLM.txt', 'r') as f:
     lines = f.readlines()
     for line in lines:
        NLM.append(line.split('\n')[0])


# In[197]:


len(NLM)


# In[198]:


NLM = [(" " + x + " ").lower() for x in NLM]


# In[245]:


for term in NLM:
    if term not in part_dict:
        print(term)


# In[199]:


count = 0
for term in NLM:
    if len(new_dict[term])>1:
        count+=1
print(count)


# In[240]:


term_f


# In[264]:


prof = []
with open('Professor_list.txt', 'r') as f:
     lines = f.readlines()
     for line in lines:
        prof.append(line.split(' ')[0])


# In[265]:


prof = list(set(prof))
prof = [x.replace('\n','') for x in prof]


# In[266]:





# In[267]:


prof


# In[268]:


len(prof)


# In[269]:


prof = [(" " + x + " ").lower() for x in prof]


# In[236]:


count = 0
for term in prof:
    if len(new_dict[term])>1:
        count+=1
print(count)


# In[277]:


not_count = 0
for term in prof:
    if term not in part_dict:
       not_count+=1


# In[ ]:





# In[279]:


len(prof) - not_count


# In[237]:


39/54


# In[261]:


len(no_appear)


# In[271]:


msh =0
nlm=0
p = 0
for term in no_appear:
    if term in NLM:
        print(f'NLM : {term}')
        nlm+=1
    elif term in MSH_terms:
        print(f'MSH : {term}')
        msh+=1
    elif term in prof:
        print(f'prof : {term}')
        p+=1
    else:
        print(f'UK : {term}')


# In[281]:


sp = [' amber ',
' jade ',
' rust ',
' turquoise ',
' gold ',
' silver ',
' waltz ',
' tango ',
' foxtrot ',
' rumba ',
' polka ',
' chicken ',
' tuna ',
' lamb ',
' English ',
' Spanish ',
' French ',
' Dutch ',
' alligator ',
' rabbit ',
' mink ',
' oak ',
' pine ',
' maple ',
' chestnut ']


# In[285]:


sp = [x.lower() for x in sp]


# In[ ]:





# In[288]:


not_count = 0
for term in sp:
    if term not in part_dict:
       not_count+=1
len(sp) - not_count


# In[287]:


count = 0
for term in sp:
    if len(new_dict[term])>1:
        count+=1
print(count)


# In[289]:


homo = []
with open('homonymy.txt', 'r') as f:
     lines = f.readlines()
     for line in lines:
        homo.append(line.split(' ')[0])
homo = list(set(homo))
homo = [x.replace('\n','') for x in homo]
homo = [(" " + x + " ").lower() for x in homo]


# In[290]:


len(homo)


# In[301]:


not_count = 0
for term in homo:
    if term not in part_dict:
       not_count+=1
print(len(homo) - not_count)

count = 0
for term in homo:
    if len(new_dict[term])>1:
        count+=1
print(count)


# In[299]:


meta = []
with open('metaphors.txt', 'r') as f:
     lines = f.readlines()
     for line in lines:
        meta.append(line.split(' ')[0])
meta = list(set(meta))
meta = [x.replace('\n','') for x in meta]
meta = [(" " + x + " ").lower() for x in meta]


# In[302]:


not_count = 0
for term in meta:
    if term not in part_dict:
       not_count+=1
print(len(homo) - not_count)

count = 0
for term in meta:
    if len(new_dict[term])>1:
        count+=1
print(count)


# In[304]:


for term in meta:
    if term not in part_dict:
        print(term)


# In[ ]:




