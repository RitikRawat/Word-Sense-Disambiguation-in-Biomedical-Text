# 🧬 Word Sense Disambiguation in Biomedical Text

A CS598 Topics in AI project exploring scalable and domain-specific Word Sense Disambiguation (WSD) using large-scale PubMed data and graph-based clustering.

---

## 📖 Introduction

**Word Sense Disambiguation (WSD)** is a core Natural Language Processing (NLP) task focused on identifying the correct sense of a word based on its context. Many words have multiple meanings — WSD helps machines understand which meaning is intended in any given sentence.

For example:
- “He hit the ball with the **bat**.” (sports equipment)
- “I saw a **bat** in the cave.” (flying mammal)

In the biomedical domain, WSD becomes even more complex due to:
- **Highly specialized terminology**
- **Dense and technical sentence structures**
- **Limited annotated datasets**
- **Ambiguous abbreviations and domain-specific meanings**

### Types of Ambiguity:
- **Homonymy**: unrelated senses (e.g., *bat* – animal vs. equipment)
- **Metaphor**: figurative extensions (e.g., *snake* – reptile vs. sly person)
- **Systematic Polysemy**: semantically related senses (e.g., *oak* – tree vs. wood)

---

## 🧪 Methodology

This project uses approximately **16 million PubMed articles** to extract semantic relationships from biomedical text and perform **Word Sense Disambiguation (WSD)** via clustering techniques.

### 🔹 Co-occurrence Network Construction

- **Data Source**: Titles and abstracts from PubMed articles.
- **Tokens**: Initially ~2 billion singleton tokens extracted using SciSpacy.
- **MWEs**: Top 100,000 **Multi-Word Expressions (MWEs)** selected based on Mean Reciprocal Rank (MRR).
- **Rationale**: MWEs are assumed to be less ambiguous and serve as semantic anchors.

### 🔹 Clustering with Markov Clustering (MCL)

- **Clustering Technique**: Markov Clustering simulates random walks on the graph to form clusters based on flow.
- **Cluster Types Explored**:
  - **Singleton Clusters**: Based only on single-token words.
  - **Mixed Clusters**: Based on both MWEs and singletons.
  - **Hybrid Clusters** *(Final choice)*: Built using only MWEs; ambiguous singletons are added later.

### 🔹 Disambiguating Terms

To assign ambiguous terms to clusters:
- The term must co-occur with MWEs in a cluster at least twice.
- Two assignment strategies:
  - **Approach A**: Co-occurs with a majority of MWEs in the cluster.
  - **Approach B**: Co-occurs with more than one MWE.

Terms that appear in multiple clusters are assumed to express multiple senses.

---

## 📊 Results

- **Clusters Created**: 2648 clusters (Inflation factor: 3.5)
- **Avg. Cluster Size**: ~37 terms (excluding 5 largest clusters: ~25.9)
- **Ambiguous Terms Evaluated**: 217  
  - From: NLM WSD (50), MSH WSD (96), Dr. Krovetz’s list (93)

### 📈 Disambiguation Accuracy

| Dataset             | Terms Used | Ambiguity Captured |
|---------------------|------------|---------------------|
| NLM WSD             | 44/50      | 86.36%              |
| MSH WSD             | 49/50      | 100%                |
| Dr. Krovetz's List  | 60/93      | 73.33%              |

### 📘 Ambiguity Type Breakdown (from Dr. Krovetz’s list)

| Ambiguity Type        | Terms Used | Ambiguity Captured |
|------------------------|------------|---------------------|
| Homonymy              | 18/25      | 77.77%              |
| Metaphor              | 24/43      | 62.5%               |
| Systematic Polysemy   | 18/25      | 83.33%              |

---

## ⚠️ Limitations

- **Limited Scope**: Depends heavily on a fixed MWE list, potentially missing new or infrequent expressions.
- **Ambiguous Clusters**: Clusters composed only of MWEs may lack contextual meaning.
- **Manual Evaluation Dependency**: Relies on human-annotated terms for validating disambiguation accuracy.
- **Scalability**: Full dataset (~16M articles, 2B tokens) was computationally infeasible to process with available resources.
- **No Overlapping Clusters**: MCL cannot assign terms to multiple clusters by default, limiting nuance.

---

## 🔮 Future Work

- **Combine MWEs & Singletons**: Incorporate both into a unified clustering model.
- **Ambiguity Type Classification**: Automatically label each sense type (e.g., metaphor vs. homonymy).
- **Improve Scalability**: Use larger computational resources to handle the full corpus.
- **Adapt to Biomedical Evolution**: Automatically update clusters with new biomedical discoveries and terminology.
- **Multilingual WSD**: Extend to biomedical literature in other languages.
- **Overlapping Clustering Algorithms**: Explore alternatives like Link Clustering or Overlapping Partitioning.
- **General + Biomedical Hybrid Model**: Merge both domains to create a robust, all-purpose WSD model.

---

## 📄 References

- **PubMed Central** — Biomedical corpus source  
- **MSH WSD Dataset** — Standard WSD benchmark  
- **NLM WSD Terms** — Manually annotated dataset  
- **Dr. Krovetz’s Ambiguity List** — Expert-curated word sense examples  
- **SciSpacy** — Biomedical NLP toolkit  
- **Markov Clustering** — https://micans.org/mcl/

---

> 📚 For full details, see the [Final Report.pdf](./Final%20Report.pdf)
