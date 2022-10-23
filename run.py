from jogos.jogos import CbfJogos
import json

crawler = CbfJogos('A')
j = crawler.executer()
print(json.dumps(j, indent=2))
