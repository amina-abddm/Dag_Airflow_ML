# 🧠 Airflow ML Training Pipeline

Ce projet met en place un pipeline de machine learning orchestré avec **Apache Airflow**, exécuté dans un environnement **Dockerisé**, et connecté à une base de données **PostgreSQL**. Il automatise la préparation des données, l'entraînement d'un modèle, et la gestion des erreurs avec alertes email.

---

## 📁 Structure du projet

```bash

Dag_Airflow_ML/
├── dags/
│ ├── train_model_dag.py # DAG principal orchestrant le pipeline ML
│ ├── get-data.py # Script de récupération des données
│ └── ml_tasks.py # Fonctions Python : entraînement, création de tables, échec simulé
│
├── config/
│ └── airflow.cfg # Configuration Airflow personnalisée
│
├── data/
│ └── advertising.csv # Jeu de données source pour l’entraînement
│
├── logs/ # Logs générés par Airflow (créés au runtime)
│
├── ml_logistical_regression/
│ └── train_model.py # Script d’entraînement du modèle de régression logistique
│
├── output/
│ └── model.pkl # Modèle entraîné sauvegardé
│
├── plugins/ # Plugins Airflow personnalisés
│
├── requirements.txt # Dépendances Python (Airflow, providers, etc.)
├── docker-compose.yaml # Stack Docker : Airflow, Postgres, Redis, etc.
├── .env # Variables d’environnement (si utilisé)
├── .venv/ # Environnement virtuel Python (non versionné)
├── README.md # Documentation du projet
└── .gitignore # Fichiers/dossiers à exclure du versionnement

```

---

## 🚀 Fonctionnalités

- Création automatique de tables dans PostgreSQL (`intermediate_data`, `intermediate_data_temp`)
- Entraînement d’un modèle ML via une fonction Python personnalisée
- Simulation d’échec pour tester l’envoi d’email
- Notifications par email en cas d’échec ou de succès
- Architecture modulaire avec `PythonOperator` et `PostgresHook`

---

## ⚙️ Prérequis

- Python 3.12
- Docker & Docker Compose
- Apache Airflow 3.1
- Provider PostgreSQL : `apache-airflow-providers-postgres==6.3.0`

---

## 🛠️ Installation

```bash
# 1. Cloner le projet
git clone <url-du-repo>
cd Dag_Airflow_ML

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer les services Airflow + Postgres
docker compose up --build
```

## 🌐 Interface Airflow

- Accès via navigateur : http://localhost:8080 Identifiants par défaut :
- Login : airflow
- Mot de passe : airflow

## 🧪 Déclencher le DAG

```bash
docker compose exec airflow-scheduler airflow dags trigger train_model_dag
```

Ou via l’interface Airflow → DAGs → train_model_dag → ▶️

## 📬 Notifications email

- En cas d’échec, un email est envoyé à : ...@gmail.com
- SMTP doit être configuré dans airflow.cfg ou via les variables d’environnement

## ⚠️ Problèmes fréquents

- ***Erreur : `Connection refused` vers Postgres**  
  → Vérifier que le service `postgres` est bien lancé dans Docker.

- ***Airflow ne trouve pas le DAG**  
  → Vérifier que le dossier `dags/` est bien monté dans `docker-compose.yaml`.

## 🔮 Évolutions prévues

- Intégration d’un modèle de validation automatique des performances
- Ajout d’un dashboard Streamlit pour visualiser les résultats
- Automatisation du déploiement du modèle entraîné

## 👩‍💻 Auteur

Projet développé par Amina dans le cadre de sa reconversion professionnelle en data/ML. Objectif : maîtriser l’orchestration de workflows ML avec Airflow + Docker + PostgreSQL.