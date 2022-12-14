import datetime as dtm
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from unicodedata import normalize as nm
from urllib import response
class Crawler:
    content = None

    def __init__(self, url):
        self.url = url

    def obtem_html(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.inicio_coleta= self.registra_time()
        response = requests.get(url=self.url, headers=header, verify=False)
        response.encoding = 'UTF-8'
        self.content = response.text
        self.fim_coleta = self.registra_time()

    def registra_time(self):
      time = dtm.datetime.now()                    
      return time.strftime("%Y-%m-%d %H:%M:%S.%f") 

class CbfJogos(Crawler):
    SITES = {
    'serie-a' : 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a',
    'serie-b' : 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-b'
    }

    def lista_jogos(self):
        self.obtem_html()
        soup = BeautifulSoup(self.content, 'html.parser')
        response = {
            "origem": "cbf",
            "serie": 'Serie-' + self.url[-1].upper(),
            "url": self.url,
            "request_at": self.inicio_coleta,
            "coleted_at": self.fim_coleta,
            "jogos": []
        }
        rodadas = soup.select('div.swiper-slide')
        for rodada in rodadas:
            response['jogos'].extend(self.organiza_jogos(rodada))
        return response
      
    def remove_acentos(self, str):
      str_sem_acentos = nm('NFKD', str).encode('ASCII', 'ignore').decode('ASCII')
      return str_sem_acentos

    def extractor_data_id(self, jogo):
        text = jogo.find('span', attrs={
            'partida-desc text-1 color-lightgray p-b-15 block uppercase text-center'}).get_text()
        data_id = re.sub(r"^\s+", "", text,
                         flags=re.UNICODE | re.MULTILINE)
        data_id = data_id.replace('\r\n', '').split('-')
        data = data_id[0].split(', ')[1]
        id = data_id[1]
        id = re.search("[0-9]+", id)[0]
        self.data = data
        self.id = id

    def extractor_rodada(self, lista):
        rodada = lista.find('h3').get_text()
        rodada = re.search("[0-9]+", rodada)[0]
        self.rodada = rodada

    def extractor_local_jogo(self, lista):
        local = lista.find('span', attrs={
                           'partida-desc text-1 color-lightgray block uppercase text-center'}).get_text()
        local = re.sub(r"^\s+", "", local,
                       flags=re.UNICODE | re.MULTILINE)
        local = re.sub("\n[a-z]+ [a-z]+ [a-z]+ [a-z]+\n|\n[a-z]+ [a-z]+ [a-z]+\n", "", local,
                       flags=re.UNICODE | re.IGNORECASE)
        local = self.remove_acentos(local)
        self.local = local

    def extractor_mandante(self, lista):
        info_mandante = lista.find('div', attrs={'time pull-left'})
        nome = info_mandante.find('img')['title'].split(' - ')[0]
        nome = self.remove_acentos(nome)
        imagem = info_mandante.find('img')['src']
        sigla = info_mandante.get_text()
        sigla = re.sub(r"^\s+", "", sigla,
                       flags=re.UNICODE | re.MULTILINE).replace('\n', '')
        mandante = {'nome': nome, 'imagem_url': imagem, 'sigla': sigla}
        self.mandante = mandante

    def extractor_visitante(self, lista):
        info_mandante = lista.find('div', attrs={'time pull-right'})
        nome = info_mandante.find('img')['title'].split(' - ')[0]
        nome = self.remove_acentos(nome)
        imagem = info_mandante.find('img')['src']
        sigla = info_mandante.get_text()
        sigla = re.sub(r"^\s+", "", sigla,
                       flags=re.UNICODE | re.MULTILINE).replace('\n', '')
        visitante = {'nome': nome, 'imagem_url': imagem, 'sigla': sigla}
        self.visitante = visitante

    def extractor_placar(self, lista):
        placar = lista.find(
            'span', attrs={'bg-blue color-white label-2'})
        if placar is None:
            placar = []
        else:
            placar = placar.get_text().split(' x ')
        self.placar = placar

    def extractor_detalhes(self, lista):
        infos = lista.find('span', attrs ={'partida-desc text-1 color-lightgray block uppercase text-center'})
        link = infos.find('a')['href']
        self.link_detalhes = link

    def info_jogos(self, jogo):
        self.extractor_local_jogo(jogo)
        self.extractor_data_id(jogo)
        self.extractor_mandante(jogo)
        self.extractor_visitante(jogo)
        self.extractor_placar(jogo)
        self.extractor_detalhes(jogo)

    def organiza_jogos(self, lista):
        json = []
        jogos = lista.find_all('li')
        self.extractor_rodada(lista)
        for jogo in jogos:
            self.info_jogos(jogo)
            data = {'rodada': self.rodada, 'id': self.id, 'data_jogo': self.data,
                'local_jogo': self.local, 'mandante': self.mandante, 'visitante': self.visitante,
                'placar': self.placar, "link_detalhes": self.link_detalhes
            }
            json.append(data)
        return json

    def executer(self):
        jogos = self.lista_jogos()
        #jogos = self.organiza_jogos(lista)
        return jogos
