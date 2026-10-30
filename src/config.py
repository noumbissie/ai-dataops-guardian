import os
from dotenv import load_dotenv

# Chargement des variables du fichier .env si présent
load_dotenv()

class Settings:
    """Configuration centralisée de l'application."""
    
    # Qdrant Vector DB
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", 6333))
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "enterprise_knowledge")
    
    # Paramètres de déduplication & modèle
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", 0.89))
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

settings = Settings()