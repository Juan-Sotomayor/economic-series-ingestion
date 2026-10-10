import json
from urllib.request import urlopen

URL = (
    "https://api.bcb.gov.br/dados/serie/"
    "bcdata.sgs.11/dados/ultimos/10?formato=json"
)

with urlopen(URL, timeout=15) as response:
    dados = json.load(response)

print(f"Registros recebidos: {len(dados)}")

for registro in dados[:3]:
    print(registro)