# srcs/streamlit_app/app.py
import streamlit as st
import pandas as pd
import joblib
from model import get_top_k_similar_indices, get_top_k_similar_indices_faiss
from utils import get_results, get_sections
from templates import search_result, get_section_template

def main():
    st.title('Pesquisa na KB de Hubla')
    search = st.text_input('Entre com o texto da pesquisa:')
    k = st.number_input('Entre com o número de seções que a pesquisa vai retornar:', 
                        min_value=1, max_value=10, value=3, step=1)
    # cleaned_hubla_df = pd.read_csv('data/cleaned_hubla_df.csv')
    # cleaned_hubla_df_tfidf = joblib.load('data/cleaned_hubla_df_tfidf.pkl')
    # tfidf = joblib.load('data/tfidf.pkl')

    hubla_df = pd.read_csv('data/hubla_df_faiss.csv')
    search_index = joblib.load('data/search_index.pkl')

    if search:
        index = get_top_k_similar_indices_faiss(search, search_index, hubla_df, k)
        sections = get_sections(index, hubla_df)
        for i in range(k):
            st.write(get_section_template(i, sections[i][0], sections[i][1], sections[i][2]),
                     unsafe_allow_html=True)
    

    # if search:
    #     index, sims = get_top_k_similar_indices(search, k, tfidf, cleaned_hubla_df_tfidf)
    #     results = get_results(index, sims, cleaned_hubla_df)

    #     for i in range(k):
    #         st.write(search_result(i, results[i][0], results[i][1], results[i][2], results[i][3]),
    #                  unsafe_allow_html=True)

if __name__ == '__main__':
    main()