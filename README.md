#AI-DataOps-Guardian

> Enterprise-grade Data Quality, PII Masking & Semantic Deduplication Engine for RAG Infrastructure.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Qdrant](https://img.shields.io/badge/VectorDB-Qdrant-red)
![Airflow](https://img.shields.io/badge/Orchestrator-Apache%20Airflow-green)
![Docker](https://img.shields.io/badge/Infrastructure-Docker%20Compose-blue)


## Problem Statement

Deploying Generative AI (RAG) at scale introduces two critical engineering challenges:
1. **Data Contamination & PII Leakage:** Sensitive user data (emails, phones, IBANs) sent to LLMs via vector stores violate GDPR/compliance.
2. **Cost & Latency Explosion:** Re-embedding duplicate or near-duplicate documents wastes API compute costs and pollutes search accuracy.


##Architecture Overview

```text
[ Raw Data Ingestion ] 
         │
         ▼
[ PII Masking Engine ] ──► (Regex / Presidio: PHONE, MAIL, IBAN )
         │
         ▼
[ FastEmbed Vectorization ]
         │
         ▼
[ Semantic Deduplication ] ──► (Qdrant HNSW Similarity Check >= 95%)
    ├── Duplicate ──► [ REJECT & ALERT ]
    └── New Data  ──► [ UPSERT TO QDRANT ]

##Quickstart

docker-compose up -d 

access services : 

-Qdrant Dashboard : http://localhost:6333/dashboard

-Airflow Web UI : http://localhost:8080 (credentials: airflow / airflow)

##Key Technical Features

Deterministic PII Masking: Anonymizes sensitive tags (<EMAIL_MASKED>, <PHONE_MASKED>, <IBAN_MASKED>) before embedding.

HNSW Semantic Deduplication: Uses Qdrant cosine distance to detect and block duplicates at index-time.

Production-Ready Orchestration: Airflow DAG handling retries, execution isolation, and DataOps logging.
