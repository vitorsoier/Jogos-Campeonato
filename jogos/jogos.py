import json
import re
from urllib import response
import requests
import pandas as pd
from bs4 import BeautifulSoup
from jogos.utils import formater


class Crawler:
    content = None

    def __init__(self, url):
        self.url = url

    def obtem_html(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        response = requests.get(url=self.url, headers=header, verify=False)
        self.content = response.content
        # validar se o conteudo existe, caso não oq fazer?


class CbfJogos(Crawler):

    SERIEA_URL = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a'
    SERIEB_URL = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-b'

    def lista_jogos(self):
        self.obtem_html()
        soup = BeautifulSoup(self.content, 'html.parser')
        response = {
            "origem": "cbf",
            "serie": "serie-a",
            "url": self.url,
            "data_coleta": "<data_da_coleta>",
            "jogos": []
        }
        rodadas = soup.find_all('div', attrs={'data-slide-index'})
        for rodada in rodadas:
            response['jogos'].update(self.organiza_jogos(rodada))
        return response

    def extractor_data_id(self, jogo):
        text = jogo.find('span', attrs={
            'partida-desc text-1 color-lightgray p-b-15 block uppercase text-center'}).get_text()
        data_id = re.sub(r"^\s+", "", text,
                         flags=re.UNICODE | re.MULTILINE)
        data_id = data_id.replace('\r\n', '').split('-')
        data = data_id[0]
        id = data_id[1]
        id = re.search("[0-9]{3}", id)[0]
        return data, id

    def extractor_rodada(self, lista):
        rodada = lista.find('h3').get_text()
        return rodada

    def organiza_jogos(self, lista):
        json = []
        jogos = lista.find_all('li')
        rodada = self.extractor_rodada(lista)
        for jogo in jogos:
            data, id = self.extractor_data_id(jogo)
            data = {'data_jogo': data, 'id': id, 'rodada': rodada}
            json.append(data)
        return json

    def executer(self):
        jogos = self.lista_jogos()
        #jogos = self.organiza_jogos(lista)
        return jogos
