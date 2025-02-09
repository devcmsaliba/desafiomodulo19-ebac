import requests
from requests.exceptions import HTTPError
import pandas as pd
from bs4 import BeautifulSoup
import csv

robots_url = 'https://github.com/robots.txt'
robots_response = requests.get(robots_url)
print('Conteúdo do robots.txt:\n', robots_response.text)

URL = 'https://github.com/trending'
headers = {'User-Agent': 'Mozilla/5.0'}

try:
  response = requests.get(URL, headers=headers)
  response.raise_for_status()
  print("Requisição bem-sucedida!")
  conteudo = response.text
except HTTPError as exc:
  print('Erro ao acessar GitHub Trending:', exc)
  conteudo = None

if conteudo:
  soup = BeautifulSoup(conteudo, 'html.parser')
  print(soup.prettify())
  projects = soup.find_all('article', class_='Box-row', limit=10)
  print(projects)

top10_projects = []

# Iterar sobre os projetos encontrados
for ranking, project in enumerate(projects, start=1):

  # Extrair name, obtém o texto dentro da tag(get_text), remove espaços extras (strip=True), remove / ou , (replace).
  name = project.find('h2', class_='h3')
  name = name.get_text(strip=True).replace('/', '') if name else 'N/A'

  # Extrair language
  language = project.find('span', itemprop='programmingLanguage')
  language = language.get_text(strip=True) if language else 'N/A'

  # Extrair stars
  stars_tag = project.find_all('a', class_='Link--muted')
  stars = stars_tag[0].get_text(strip=True).replace(',', '') if len(stars_tag) > 0 else 'N/A'

  # Extrair stars_today
  stars_today = project.find('span', class_='d-inline-block float-sm-right')
  stars_today = stars_today.get_text(strip=True).split()[0].replace(',', '') if stars_today else 'N/A'

  # Extrair forks considerando que ele vem após stars
  forks = stars_tag[1].get_text(strip=True).replace(',', '') if len(stars_tag) > 1 else 'N/A'

  # Adicionar dados do projeto à lista
  top10_projects.append([ranking, name, language, stars, stars_today, forks])

# Exibir os dados extraídos
for project in top10_projects:
  print(project)

with open('github.csv', mode='w', newline='', encoding='utf8') as arquivo:
  writer = csv.writer(arquivo, delimiter=';')
  writer.writerow(['ranking', 'project', 'language', 'stars', 'stars_today', 'forks'])
  writer.writerows(top10_projects)

print(f'Os dados dos 10 projetos mais populares foram salvos com sucesso em github.csv')

top10_projects_df = pd.read_csv('github.csv')
top10_projects_df