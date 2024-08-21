import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# abrir o navegador
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# URL da página de filmes em lançamento
url = 'https://www.imdb.com/calendar/?ref_=nv_mv_cal'

# Adicionando esse cabeçalho para que seja possível acessar a página do IMDB
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Acessando o html da página
html_content = soup.text

# Acesasndo a parte da página que possui todos os filmes
lista_filmes = soup.find(class_='ipc-page-section ipc-page-section--base')
print("Esse é o trecho do HTML da lista de filmes:")
print(lista_filmes.prettify())

# Retorna uma lista com todos os filmes que existem dentro do componente supracitado
todos_filmes = lista_filmes.find_all(class_='ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-8c2b7f1f-0 dKSSmX');

# Printa cada elemento da lista de filmes (printando junto com um contador apenas para confirmar o número de filmes)
# Título, Data de Lançamento, Gênero(s) e o link para página da série.
i = 0;
for elemento in todos_filmes:
    print(i)
    i = i + 1

    # Acessando cada filme da lista
    print(elemento)

    # Necessário acessar o link desse elemento
    elemento_do_filme = elemento.find(class_='ipc-metadata-list-summary-item__t',)

    # Acessando o nome do filme que é o elemento de texto da tag a (TITULO)
    nome_do_filme = elemento_do_filme.get_text()
    print(nome_do_filme)

    url_base = 'https://www.imdb.com/'
    link_do_filme= elemento_do_filme['href']
    link_completo = urljoin(url_base, link_do_filme)

    print('Esse é o link da página do filme: ')
    print(link_completo)

    print('Esse é o nome do filme, que é um botão e entra no link do filme (logo abaixo): ')
    print(nome_do_filme)
    # print('Esse é o link da página do filme: ')
    # print(link_do_filme['href'])
    driver.get(link_completo)

    print("Esse é o conteudo do HTML da página do filme respectivo")
    response_dois = requests.get(link_completo, headers=headers)
    soup_dois = BeautifulSoup(response_dois.content, 'html.parser')
    html_page_filme = soup_dois.text
    print(soup_dois.prettify())
    informacoes_filme = soup_dois.find('h1', class_='sc-d8941411-0 dxeMrU')
    print(informacoes_filme)
    # print("Esse é o HTML da página:")
    # print(html_page_filme)
    sleep(15)

    sleep(15)

    # Criar um json com todos os dados


# print(soup.prettify())

