import json
from datetime import datetime
from decimal import Decimal
from urllib.request import urlopen

from src.domain.entities import Observation


class BacenAdapter:

    def get_observations(
        self, series_id: str
    ) -> list[Observation]:

        if not series_id.isdecimal():
            raise ValueError("O código SGS deve ser numérico")

        url = (
            "https://api.bcb.gov.br/dados/serie/"
            f"bcdata.sgs.{series_id}/dados/ultimos/10"
            "?formato=json"
        )

        with urlopen(url, timeout=15) as response:
            dados = json.load(response)

        observations = []

        for registro in dados:
            observation = Observation(
                series_id=series_id,
                date=datetime.strptime(
                    registro["data"], "%d/%m/%Y"
                ).date(),
                value=Decimal(registro["valor"]),
            )

            observations.append(observation)

        return observations