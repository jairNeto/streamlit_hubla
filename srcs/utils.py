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
