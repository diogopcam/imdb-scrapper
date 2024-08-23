import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json

# Configurações do Selenium
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Iniciando uma colecao apenas para armazenar todos os filmes iterados
filmes = []

# Iniciando os atributos que sao colecoes

# URL da página de filmes em lançamento
url = 'https://www.imdb.com/calendar/?ref_=nv_mv_cal&region=BR'
driver.get(url)

# Espera para garantir que a página carregue completamente (ajuste conforme necessário)
time.sleep(5)

# Extraindo o HTML carregado pelo Selenium
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

# Acessando a parte da página que possui todos os filmes
lista_filmes = soup.find(class_='ipc-page-section ipc-page-section--base')

# Verificando se a lista de filmes foi encontrada
if lista_filmes:
    todos_filmes = lista_filmes.find_all(class_='ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-8c2b7f1f-0 dKSSmX')
    i = 0
    for elemento in todos_filmes:
        generos = []
        elenco = []

        print(i)
        i += 1

        # Acessando o nome de cada filme
        elemento_do_filme = elemento.find(class_='ipc-metadata-list-summary-item__t')

        if elemento_do_filme:

            # # Acessando o nome do filme
            # nome_do_filme = elemento_do_filme.get_text()

            print('Esses sao os generos do filme')
            ul_generos = elemento.find(
                class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base')

            if ul_generos:
                todos_generos = ul_generos.find_all('span')

                if todos_generos:
                    for gen in todos_generos:
                        genero = gen.get_text()
                        generos.append(genero)
                        print(gen.get_text())

            else:
                print('Nao existe o campo de generos')

            # Acessando a URL do filme
            url_base = 'https://www.imdb.com/'
            link_do_filme = elemento_do_filme['href']
            link_completo = urljoin(url_base, link_do_filme)
            print('Esse é o link da página do filme: ')
            print(link_completo)

            # Abrindo a página do filme
            driver.get(link_completo)
            # time.sleep(2)  # Ajuste o tempo conforme necessário

            # Obtendo o HTML da página do filme
            html_page_filme = driver.page_source
            soup_dois = BeautifulSoup(html_page_filme, 'html.parser')

            nome_do_filme = soup_dois.find(class_='hero__primary-text')
            nome_filme_txt = nome_do_filme.get_text()

            print('Esse é o nome do filme')
            print(nome_filme_txt)

            # Acessando o ano do filme
            informacoes_filme = soup_dois.find_all('a', class_='ipc-link ipc-link--baseAlt ipc-link--inherit-color')
            if len(informacoes_filme) > 4:
                ano_filme = informacoes_filme[4].text
                print('Esse é o ano do filme:')
                print(ano_filme)

            # Acessando a data de lançamento
            data_lancamento_txt = ""
            data_lancamento = soup_dois.find('div', class_='sc-5766672e-2 bizeKj')
            if data_lancamento:
                print('Essa é a data de lançamento completa:')
                data_lancamento_txt = data_lancamento.text
                print(data_lancamento_txt)

            # Acessando o elenco do filme
            lista_elenco = soup_dois.find('div',
                                          class_='ipc-shoveler ipc-shoveler--base ipc-shoveler--page0 title-cast__grid')

            # Verifica se o elemento foi encontrado
            if lista_elenco:
                todas_tags_a = lista_elenco.find_all('a', class_='sc-bfec09a1-1 KeEFX')

                if todas_tags_a:
                    print('Essa é a div que contém todos os membros do elenco')
                    print(lista_elenco.prettify())
                    print('Essas sao todas as tags <a> da div')
                    print(todas_tags_a)

                    # Printando todas as tags que possuem nome de alguém do elenco
                    for nome_ator in todas_tags_a:
                        nome = nome_ator.text
                        print(nome)
                        elenco.append(nome)
                else:
                    print("Elemento de elenco não encontrado. Continuando a execução do código...")

            componente_listas = soup_dois.find_all(class_='ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt')
            componente_diretor = componente_listas[1]
            nome_diretor = componente_diretor.find(class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
            print('Esse é o componente do diretor')
            nome_diretor_txt = nome_diretor.get_text()

            filme = {
                'nome': nome_filme_txt,
                'link_pagina': link_completo,
                'lancamento': data_lancamento_txt,
                'elenco': elenco,
                'diretor': nome_diretor_txt,
                'generos': generos
            }

            print('Esses sao os atributos do objeto filme: ')
            print(filme)

            filmes.append(filme)
else:
    print("Lista de filmes não encontrada")

print(filmes)

with open("filmes.json", "w") as arquivo_json:
    json.dump(filmes, arquivo_json, indent=4)

driver.quit()
