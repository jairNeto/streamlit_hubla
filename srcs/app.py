# srcs/streamlit_app/app.py
import streamlit as st
import pandas as pd
import joblib
from model import get_top_k_similar_indices
from utils import get_results
from templates import search_result

def main():
    st.title('Pesquisa na KB de Hubla')
    search = st.text_input('Entre com o texto da pesquisa:')
    k = st.number_input('Entre com o número de seções que a pesquisa vai retornar:', 
                        min_value=1, max_value=10, value=3, step=1)
    cleaned_hubla_df = pd.read_csv('data/cleaned_hubla_df.csv')
    cleaned_hubla_df_tfidf = joblib.load('data/cleaned_hubla_df_tfidf.pkl')
    tfidf = joblib.load('data/tfidf.pkl')
    

    if search:
        index, sims = get_top_k_similar_indices(search, k, tfidf, cleaned_hubla_df_tfidf)
        results = get_results(index, sims, cleaned_hubla_df)

        for i in range(k):
            st.write(search_result(i, results[i][0], results[i][1], results[i][2], results[i][3]),
                     unsafe_allow_html=True)

if __name__ == '__main__':
    main()