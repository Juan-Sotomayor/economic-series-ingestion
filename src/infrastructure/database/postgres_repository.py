import psycopg

from src.domain.entities import Observation


class PostgresRepository:

    def __init__(self, dsn: str):
        self.dsn = dsn

    def create_table(self) -> None:
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS observations (
                        series_id TEXT NOT NULL,
                        observation_date DATE NOT NULL,
                        value NUMERIC NOT NULL,

                        PRIMARY KEY (series_id, observation_date)
                    )
                """)

    def save_all(
        self, observations: list[Observation]
    ) -> None:

        if not observations:
            return

        query = """
            INSERT INTO observations (
                series_id,
                observation_date,
                value
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (series_id, observation_date)
            DO UPDATE SET value = EXCLUDED.value
        """

        rows = [
            (obs.series_id, obs.date, obs.value)
            for obs in observations
        ]

        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, rows)