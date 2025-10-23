# 📦 Imports Airflow et fonctions personnalisées
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
from ml_tasks import run_training, fail_task  # ← Fonctions métier

# ⚙️ Paramètres par défaut du DAG
default_args = {
    "owner": "Amina",
    "start_date": datetime(2023, 1, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
    "email": ["amina.abd.75@gmail.com"],  # Pour l'envoi des notifications
    "email_on_failure": True,
    "email_on_retry": False,
    "email_on_success": True,
}

# 🧠 Fonctions SQL exécutées via PostgresHook
def create_intermediate_table():
    hook = PostgresHook(postgres_conn_id="postgres_default")
    hook.run("""
        CREATE TABLE IF NOT EXISTS intermediate_data (
            id SERIAL PRIMARY KEY,
            "Daily Time Spent on Site" FLOAT,
            "Age" FLOAT,
            "Area Income" FLOAT,
            "Daily Internet Usage" FLOAT,
            "Male" BOOLEAN,
            "Clicked on Ad" BOOLEAN,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

def create_intermediate_temp_table():
    hook = PostgresHook(postgres_conn_id="postgres_default")
    hook.run("""
        DROP TABLE IF EXISTS intermediate_data_temp;
        CREATE TABLE intermediate_data_temp (
            id SERIAL PRIMARY KEY,
            "Daily Time Spent on Site" FLOAT,
            "Age" FLOAT,
            "Area Income" FLOAT,
            "Daily Internet Usage" FLOAT,
            "Male" BOOLEAN,
            "Clicked on Ad" BOOLEAN,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

# 🚀 Définition du DAG principal
with DAG(
    dag_id="train_model_dag",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["ML", "training"],
) as dag:

    # 🧱 Création de la table principale
    create_intermediate_table_task = PythonOperator(
        task_id="create_intermediate_table",
        python_callable=create_intermediate_table,
    )

    # 🧱 Création de la table temporaire
    create_intermediate_temp_table_task = PythonOperator(
        task_id="create_intermediate_temp_table",
        python_callable=create_intermediate_temp_table,
    )

    # 🤖 Entraînement du modèle
    train_task = PythonOperator(
        task_id="train_model_task",
        python_callable=run_training,
    )

    # 📧 Test d'envoi d'email en cas d'échec
    test_email = PythonOperator(
        task_id="email_failure",
        python_callable=fail_task,
    )

    # 🔗 Dépendances entre les tâches
    create_intermediate_table_task >> create_intermediate_temp_table_task >> train_task >> test_email
