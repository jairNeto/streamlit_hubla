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
