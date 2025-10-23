import os
import requests
from airflow.sdk import task
from airflow.providers.postgres.hooks.postgres import PostgresHook

@task
def get_data():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/advertising.csv"))
    os.makedirs(os.path.dirname(data_path), exist_ok=True)

    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    conn = postgres_hook.get_conn()
    cur = conn.cursor()
    with open(data_path, "r") as file:
        cur.copy_expert(
            "COPY intermediate_data_temp FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
            file,
        )
    conn.commit()
