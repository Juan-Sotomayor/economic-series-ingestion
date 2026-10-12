import os

from src.application.use_cases.import_series import ImportEconomicSeries
from src.infrastructure.providers.bacen import BacenAdapter
from src.infrastructure.database.postgres_repository import PostgresRepository


def main() -> None:
    dsn = os.environ["DATABASE_URL"]
    series_id = os.environ.get("SERIES_ID", "11")

    provider = BacenAdapter()
    repository = PostgresRepository(dsn)

    repository.create_table()

    use_case = ImportEconomicSeries(
        provider=provider,
        repository=repository,
    )

    quantidade = use_case.execute(series_id)

    print(f"Ingestão concluída: {quantidade} observações processadas.")


if __name__ == "__main__":
    main()