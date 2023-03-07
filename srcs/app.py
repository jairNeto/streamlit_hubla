# srcs/streamlit_app/app.py
import streamlit as st
import pandas as pd
import joblib
from model import get_top_k_similar_indices, get_top_k_similar_indices_faiss
from utils import get_results, get_sections, insert_feedback
from templates import search_result, get_section_template
import openai

def on_option_selected(search, section_title, section_url):
    option = st.session_state.feedback_section
    print(f'Option selected: {option}')
    insert_feedback(search, section_title, section_url, False, option)
    # Do something with selected option

def main():
    openai.api_key = st.secrets['open_ai_key']
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
            section_url = sections[i][0]
            section_title = sections[i][1]
            section_content = sections[i][2]
            st.write(get_section_template(i, section_url, section_title, section_content),
                     unsafe_allow_html=True)
            
            
            if st.button("👍", key=f"👍{i}"):
                insert_feedback(search, section_title, section_url, True)
                st.write(f"Obrigado")
        
            if st.button("👎", key=f"👎{i}"):
                options = hubla_df['section_title'].unique().tolist()
                st.selectbox('Qual a seção correta?', options, index=0, on_change=on_option_selected, args=(search, section_title, section_url), key='feedback_section')
                

    # if search:
    #     index, sims = get_top_k_similar_indices(search, k, tfidf, cleaned_hubla_df_tfidf)
    #     results = get_results(index, sims, cleaned_hubla_df)

    #     for i in range(k):
    #         st.write(search_result(i, results[i][0], results[i][1], results[i][2], results[i][3]),
    #                  unsafe_allow_html=True)

if __name__ == '__main__':
    main()