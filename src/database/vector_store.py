import uuid
from typing import List, Dict, Any, Tuple
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding

class QdrantGuardianStore:
    """
    Gestionnaire de base vectorielle Qdrant avec contrôle de déduplication sémantique.

    """

    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = "enterprise_knowledge"):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name

        self.embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Initialise la collection dans Qdrant si elle n'existe pas."""
        collections = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in collections:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            print(f"Collection '{self.collection_name}' créée avec succès.")

    def _generate_embedding(self, text: str) -> List[float]:
        """Convertit le texte en un vecteur numérique de dimension 384."""
        embeddings = list(self.embedding_model.embed([text]))
        return embeddings[0].tolist()

    def check_duplicate_and_upsert(self, text: str, metadata: Dict[str, Any], threshold: float = 0.95) -> Tuple[bool, str]:
        """
        Vérifie si le document existe déjà de manière sémantique.
        Si la similarité > threshold, le document est rejeté (doublon).
        Sinon, il est inséré dans Qdrant.
        """
        vector = self._generate_embedding(text)

        # Recherche de similarité dans Qdrant
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=1
        )

        # Si un vecteur similaire existe déjà à plus de 'threshold' %
        if search_result and search_result[0].score >= threshold:
            existing_id = search_result[0].id
            return False, f"DOUBLON DÉTECTÉ (Similarité: {search_result[0].score:.2%}, ID existant: {existing_id})"

        # Insertion du nouveau document
        point_id = str(uuid.uuid4())
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={"text": text, **metadata}
                )
            ]
        )
        return True, point_id


# --- Test d'exécution ---
if __name__ == "__main__":
    store = QdrantGuardianStore()

    doc_1 = "Rapport financier Q1 : Les revenus ont augmenté de 15 % au premier trimestre 2026."
    metadata = {"source": "finance_dept", "author": "DataOps Team"}

    print("--- 1er ESSAI : Insertion du document initial ---")
    status, msg = store.check_duplicate_and_upsert(doc_1, metadata)
    print(f"Résultat : {status} | Info : {msg}")

    print("\n--- 2ème ESSAI : Tentative d'insertion d'un document similaire ---")
    doc_2 = "Rapport financier Q1 : Les revenus ont progressé de 15 % au cours du 1er trimestre 2026."
    status, msg = store.check_duplicate_and_upsert(doc_2, metadata)
    print(f"Résultat : {status} | Info : {msg}")