import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import uuid


URL = 'https://pro.cloudhumans.com/preview/Suporte-Hubla'

def get_results(indexes, sims, df):
  i = 0
  response = []
  for _, row in df.iloc[indexes].iterrows():
    # print(f'Seção {row.section_title} com similaridade de {sims[i]:.2f}%')
    url = f'{URL}?section={row.section_id}'
    response.append([url, row.section_title, row.clean_content, sims[i]])
    i += 1
  
  return response

def get_sections(indexes, df):
  i = 0
  sections = []
  for _, row in df.iloc[indexes].iterrows():
    url = f'{URL}?section={row.section_id}'
    sections.append([url, row.section_title, row.clean_content])
    i += 1
  
  return sections

def get_collection(collection_name: str):
    json_string = st.secrets['firestore_secret']
    FIREBASE_SECRET = json.loads(json_string)

    cred = credentials.Certificate(FIREBASE_SECRET)
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    return db.collection(collection_name)

def insert_feedback(question: str,
                    section: str,
                    section_url:str,
                    is_correct:bool,
                    correct_section:str = '',
                    collection_name='hubla_kb') -> None:
    run_id = str(uuid.uuid4())
    doc_ref = get_collection(collection_name).document(run_id)
    doc_ref.set({
        u'pergunta': question,
        u'seção': section,
        u'seção_url': section_url,
        u'is_correct': is_correct,
        u'correct_section': correct_section,
        u'created_at': firestore.SERVER_TIMESTAMP,
    })