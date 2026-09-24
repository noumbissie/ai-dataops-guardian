import re
from typing import Dict, Any, Tuple

class PIICleaner:

    """
    Nettoyeur de données sensibles (PII - Personally Identifiable Information).
    Combine des expressions régulières ultra-rapides pour la conformité RGPD.
    """

    def __init__(self):
        # Motifs Regex pour les PII courantes
        self.patterns = {
            "IBAN": r"[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}",
            "SEC_SOC": r"[12]\s?\d{2}\s?(?:0[1-9]|1[0-2])\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}",
            "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "PHONE": r"\b(?:\+33|0)[1-9](?:[\s.-]?\d{2}){4}\b",
        }

    def clean_text(self, text: str) -> Tuple[str, Dict[str, int]]:
        """
        Masque les PII dans le texte et retourne le texte nettoyé 
        ainsi que le décompte des éléments anonymisés pour l'observabilité.
        """
        cleaned_text = text
        stats = {}

        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, cleaned_text)
            count = len(matches)
            if count > 0:
                stats[pii_type] = count
                # Remplacement anonymisé
                cleaned_text = re.sub(pattern, f"<{pii_type}_MASKED>", cleaned_text)

        return cleaned_text, stats


# --- Test rapide d'exécution local ---
if __name__ == "__main__":
    cleaner = PIICleaner()
    
    sample_document = """
    Compte-rendu de réunion :
    L'employé Jean Dupont (email: j.dupont@entreprise.fr, tel: 06 12 34 56 78) 
    a soumis son RIB FR7612345678901234567890123 pour le virement mensuel.
    """

    cleaned, metrics = cleaner.clean_text(sample_document)
    
    print("--- TEXTE ANONYMISÉ ---")
    print(cleaned)
    print("\n--- MÉTRIQUES DE MASQUAGE (DATAOPS) ---")
    print(metrics)    