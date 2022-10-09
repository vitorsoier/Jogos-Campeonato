from jogos.jogos import CbfJogos
import json

crawler = CbfJogos(CbfJogos.SERIEA_URL)
j = crawler.executer()
print(json.dumps(j, indent=2))
