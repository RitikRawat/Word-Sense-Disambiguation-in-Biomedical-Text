#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import xml.etree.ElementTree as ET
import spacy
import numpy as np


# In[2]:


from time import perf_counter
import gc


# In[3]:


df = pd.read_csv("combined_medline.tsv", sep = "\t",header = None)


# In[2]:


MWE = []
with open('medline_mwes.srt','r') as file:
    lines = file.readlines()
    for line in lines:
        mwe = line.split(":",1)[0]
        MWE.append(mwe)


# In[3]:


len(MWE)


# In[4]:


df.columns = ['MWE','val1','val2']


# In[10]:


df = df[df['val1']>2]


# In[6]:


df = df[df['val2']>10]


# In[21]:


df30000 = df[0:30000]['MWE']


# In[26]:


df50000 = df[0:50000]['MWE']


# In[5]:


import pickle 

with open('mwe_final.pkl', 'wb') as f:
    pickle.dump(MWE, f)


# In[23]:


import pickle 

with open('mwe_30000.pkl', 'wb') as f:
    pickle.dump(df30000, f)


# In[57]:


import pickle 

with open('mwe_50000.pkl', 'wb') as f:
    pickle.dump(df50000, f)


# In[1]:


len(MWE_dict)


# In[5]:


MWE_dict = {}

for mwe in MWE:
    f = mwe.split()[0]
    if f in MWE_dict:
        MWE_dict[f].append(mwe)
    else:
        MWE_dict[f] = [mwe]


# In[7]:


len(MWE_dict)


# In[28]:


MWE_dict = {}

for mwe in df50000:
    f = mwe.split()[0]
    if len(mwe.split()) == 2 and (len(f)>2 and len(mwe.split()[1] )>2):
        if f in MWE_dict:
            MWE_dict[f].append(mwe)
        else:
            MWE_dict[f] = [mwe]


# In[58]:


len(MWE_dict)


# In[133]:


import pickle 

with open('mwe_dictionary.pkl', 'wb') as f:
    pickle.dump(MWE_dict, f)


# In[2]:


import gzip


# In[8]:


from pathlib import Path


# In[9]:


directory = "Medline/PubMed/"


# In[ ]:


files = Path(directory).glob('*.gz')


# In[ ]:


i = 1
j = 1
for file in files:
    with gzip.open(file,'r') as f:
        tree = ET.parse(f)
        for x in tree.iter(tag ='MedlineCitation'):
            text = ''
            title = ''
            for elem in x.iter('AbstractText'):
                text = elem.text
            for elem in x.iter('ArticleTitle'):
                title = elem.text
            final = str(i) + " - " + title.lower() + " " + text.lower() + "\n"
            with open(f'Processed/{j}.txt', "a") as text_file:
                text_file.write(final)
            i = i+1
    j=j+1        


# In[10]:


directory = "Processed/"
files = Path(directory).glob('*.txt')


# In[11]:


files = list(files)


# In[ ]:


files


# In[13]:


import itertools
top100 = list(itertools.islice(files, 0,100))


# In[14]:


zipped = list([top100[0:25],top100[25:50],top100[50:75],top100[75:100]])


# In[15]:


top100.sort()


# In[16]:


import os
os.path.basename(top100[0])


# In[85]:


def my_function(files):    
    mwe_tokens =[]
    for file in files:
        name =  os.path.basename(file)
        with open(file,'r') as f:
            lines = f.readlines()
            for line in lines:
                k = line.split(' ',1)[0]
                m = line.split(' ',1)[1]
                doc = nlp(m)
                filtered_tokens = [token.text for token in doc if not token.is_stop and len(token)>2]
                doclst = {}
                for word in filtered_tokens:
                    if word in MWE_dict:
                        lst = MWE_dict[word]
                        for mwe in lst:
                            c = m.count(mwe)
                            if c>0:
                                doclst[mwe] = c
                mwe_tokens.append(doclst)
                l = f'{k} - '
                for token in filtered_tokens:
                    l = l+ token + ' '
                l = l + '\n' 
                with open(f'Tokens/{name}','a') as ff:
                    ff.write(l)
    return mwe_tokens


# In[22]:


def my_function3(files):    
    mwe_tokens ={}
    for file in files:
        name =  os.path.basename(file)
        mwe_tokens[name] = []
        print(f'starting for {name}')
        with open(file,'r') as f:
            lines = f.readlines()
            for line in lines:
                m = line.split(' ',1)[1]
                doc = nlp(m)
                filtered_tokens = [token.text for token in doc if not token.is_stop and len(token)>2]
                doclst = {}
                for word in filtered_tokens:
                    if word in MWE_dict:
                        lst = MWE_dict[word]
                        for mwe in lst:
                            c = m.count(mwe)
                            if c>0:
                                doclst[mwe] = c
                mwe_tokens[name].append(doclst)
    return mwe_tokens


# In[18]:


from concurrent.futures import ProcessPoolExecutor


# In[ ]:


with ProcessPoolExecutor(max_workers=4) as exe:
    results = exe.map(my_function3,zipped)


# In[24]:


k = list(results)


# In[25]:


len(k)


# In[63]:


print('done')


# In[26]:


tokens_final = {**k[0],**k[1],**k[2],**k[3]}


# In[28]:


len(tokens_final)


# In[ ]:





# In[30]:


import pickle
with open('tokens_final.pkl', 'wb') as f:
    pickle.dump(tokens_final, f)


# In[131]:


merged = list(itertools.chain(*k))


# In[132]:


len(merged)


# In[134]:


with open('mwe_in_100.pkl', 'wb') as f:
    pickle.dump(merged, f)


# In[14]:


import pickle 


# In[15]:


with open('mwe_dictionary.pkl', 'rb') as f:
    MWE_dict = pickle.load(f)


# In[139]:


list(merged[0].keys())


# In[137]:


vocab = []


# In[180]:


vocab_short =[]


# In[182]:


vocab_short = list(set(list(itertools.chain(*vocab_short))))


# In[177]:


vocab_short


# In[187]:


matrix = np.zeros((len(vocab_short_dict),len(vocab_short_dict)))


# In[ ]:





# In[144]:


vocab = list(set(vocab))


# In[181]:


for dic in merged[0:30000]:
    vocab_short.append(list(dic.keys()))


# In[ ]:


vocab


# In[189]:


for dic in merged[0:30000]:
    if len(dic)>1:
        lst = list(dic.keys())
        for token in lst:
            for a, b in itertools.combinations(lst, 2):
                matrix[vocab_short_dict[a],vocab_short_dict[b]] += dic[a]*dic[b]
                matrix[vocab_short_dict[b],vocab_short_dict[a]] += dic[a]*dic[b]
    


# In[190]:


for row in matrix:
    for item in row:
        if item <3:
            item =0


# In[141]:


vocab = list(itertools.chain(*vocab))


# In[147]:


vocab_dict = {}
i = 0
for key in vocab:
  vocab_dict[key] = i
  i=i+1


# In[183]:


vocab_short_dict = {}
i = 0
for key in vocab_short:
  vocab_short_dict[key] = i
  i=i+1


# In[184]:


len(vocab_short_dict)


# In[154]:


len(set(vocab))


# In[145]:


gc.collect()


# In[191]:


import markov_clustering as mc


# In[21]:


nlp = spacy.load("en_core_sci_md")


# In[ ]:




