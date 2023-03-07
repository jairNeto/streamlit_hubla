import numpy as np
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
nltk.download(['punkt', 'stopwords', 'rslp'])

def fit_tfidf(processos, stopw,
              min_df=3, max_df=0.97, max_features=2000, ngram_range=(1,1), tfidf_col='clean_content'):
  tfidf = TfidfVectorizer(
      min_df = min_df, #5
      max_df = max_df, #0.95
      max_features = max_features, #8000
      stop_words = stopw,
      ngram_range=ngram_range
  )
  tfidf.fit(processos[tfidf_col])

  return tfidf

def get_top_k_similar_indices(text, k, tfidf, df_tfidf):
    # transform the input text to a tfidf vector
    text_tfidf = tfidf.transform([text])

    # calculate cosine similarity between the input text and all the documents in the corpus
    similarity_matrix = cosine_similarity(text_tfidf, df_tfidf)

    # get the indices of the top k similar vectors
    top_k_indices = np.argsort(similarity_matrix[0])[::-1][:k]

    # get the similarity scores of the top k similar vectors
    top_k_similarities = similarity_matrix[0][top_k_indices]

    return top_k_indices, top_k_similarities


def get_top_k_similar_indices_faiss(text, search_index, df, k):
    resp = search_index.similarity_search(text, k=k)
    indexes = []
    for i in range(k):
      indexes.append(df[df['clean_content'] == resp[i].page_content].index[0])
    
    return indexes

def get_sections_faiss(text, search_index, df, k=3):
  indexes = get_top_k_similar_indices_faiss(text, search_index, df, k)
  return df.iloc[indexes].section_id.values


