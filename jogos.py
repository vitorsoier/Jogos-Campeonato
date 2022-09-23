import requests
import pandas as pd
from bs4 import BeautifulSoup

class Crawler:

    def obtem_html(self, url):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        response = requests.get(url = url , headers= header, verify= False)
        return response.content

class CbfJogos(Crawler):

    SERIEA_URL = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a'
    SERIEB_URL = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-b'

    def lista_jogos(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        jogos = soup.find('div', attrs= {'data-slide-index':'27'})
        return jogos

    def organiza_jogos(self, lista):
        jogos = lista.find_all('li')
        for jogo in jogos:
            data_id = jogo.find('span', attrs= {'partida-desc text-1 color-lightgray p-b-15 block uppercase text-center'}).get_text()
            data = data_id.split(' - ')
        return data

    def executer(self, url):
        conteudo = self.obtem_html(url)
        lista = self.lista_jogos(conteudo)
        jogos = self.organiza_jogos(lista)
        return jogos

crawler = CbfJogos()
saida = crawler.executer(CbfJogos.SERIEA_URL)
print(saida)