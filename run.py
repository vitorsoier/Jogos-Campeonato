from jogos.jogos import CbfJogos

crawler = CbfJogos(CbfJogos.SERIEA_URL)
j = crawler.executer()
print(j)
