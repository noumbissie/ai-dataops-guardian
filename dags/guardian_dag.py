from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Importation des modules métiers
from src.processors.pii_cleaner import PIICleaner
from src.database.vector_store import QdrantGuardianStore

default_args = {
    'owner': 'dataops_guardian',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}


def run_ai_dataops_pipeline():
    """
    Tâche principale : Ingestion, Nettoyage PII et Chargement vectoriel sécurisé.
    """
    cleaner = PIICleaner()
    # Dans Docker Airflow, la base Qdrant s'appelle 'qdrant' (nom du service docker-compose)
    store = QdrantGuardianStore(host="qdrant", port=6333)

    # Simulation de données brutes arrivant dans le pipeline
    incoming_documents = [
        {
            "raw_text": "Note RH : Contrat de Sarah Martin (email: s.martin@email.com, tel: 06 99 88 77 66) validé.",
            "source": "HR_Portal"
        },
        {
            "raw_text": "Note RH : Contrat de Sarah Martin (email: s.martin@email.com, tel: 06 99 88 77 66) validé.",
            "source": "HR_Portal_Duplicate"
        }
    ]

    for doc in incoming_documents:
        # 1. Étape de nettoyage PII
        cleaned_text, pii_stats = cleaner.clean_text(doc["raw_text"])
        print(f"[Data Quality] PII détectés : {pii_stats}")

        # 2. Étape d'ingestion vectorielle avec déduplication
        success, info = store.check_duplicate_and_upsert(
            text=cleaned_text,
            metadata={"source": doc["source"], "pii_masked_count": sum(pii_stats.values())}
        )
        
        if success:
            print(f"[Ingestion SUCCESS] Document inséré avec l'ID : {info}")
        else:
            print(f"[DataOps ALERT] Document rejeté : {info}")


with DAG(
    'ai_dataops_guardian_pipeline',
    default_args=default_args,
    description='Pipeline de contrôle qualité de données et d ingestion RAG sécurisée',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    guardian_process_task = PythonOperator(
        task_id='process_and_guard_documents',
        python_callable=run_ai_dataops_pipeline,
    )