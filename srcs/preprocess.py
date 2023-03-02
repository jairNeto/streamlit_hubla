import re
import nltk
from nltk.corpus import stopwords
nltk.download(['punkt', 'stopwords', 'rslp'])


def letra_minuscula(texto):
  return texto.lower()

def sanitize_text(texto):
  texto = re.sub(r'[^\w\s]', '', texto)
  texto = re.sub(r'==.*?==+', '', texto)
  texto = texto.replace('\n', '')
  return texto

def remove_parenteses(texto):
  return re.sub(r'\((.*?)\)', '', str(texto))

def remove_separator(texto):
  texto = texto.replace('_separator_', '')
  return texto

def get_words_from_file(filepath: str) -> set:
  with open(filepath) as file:
      lines = file.readlines()
      words_list = [line.rstrip() for line in lines]
  
  return set(words_list)

def remove_stopwords(text: str, custom_stopwords_path: str='', personal_names_path: str='') -> str:

  stop_words = set(stopwords.words("portuguese"))

  if custom_stopwords_path:
    custom_stopwords_set = get_words_from_file(custom_stopwords_path)
    stop_words = set(stop_words).union(custom_stopwords_set)
  
  if personal_names_path:
    custom_personal_name_set = get_words_from_file(personal_names_path)
    stop_words = set(stop_words).union(custom_personal_name_set)

  texto = [word for word in text.split() if word not in stop_words]
  return ' '.join(texto)


def nlp_data_cleaning(processos,
                      pre_process_col='INTEIRO_TEOR'):
  
  #NLP
  processos.fillna('', inplace=True)
  colunasString = [pre_process_col]
  for item in colunasString:
    processos[item] = processos[item].astype(str)
    processos[item] = processos[item].apply(letra_minuscula)
    processos[item] = processos[item].apply(remove_separator)
    processos[item] = processos[item].apply(sanitize_text)
    processos[item] = processos[item].apply(remove_parenteses)
    processos[item] = processos[item].apply(remove_stopwords)
   
  processos = processos.drop(['Unnamed: 0'], axis=1, errors='ignore')

  return processos
