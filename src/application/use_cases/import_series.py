from src.application.ports.data_provider import DataProvider
from src.application.ports.repository import ObservationRepository


class ImportEconomicSeries:
    def __init__(
        self,
        provider: DataProvider,
        repository: ObservationRepository,
    ) -> None:
        self.provider = provider
        self.repository = repository

    def execute(self, series_id: str) -> int:
        observations = self.provider.get_observations(series_id)

        self.repository.save_all(observations)

        return len(observations)