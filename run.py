from jogos.jogos import CbfJogos
import json

crawler = CbfJogos(CbfJogos.SITES['serie-a'])
j = crawler.executer()
print(json.dumps(j, indent=2))
