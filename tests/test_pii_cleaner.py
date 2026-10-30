import pytest
from src.processors.pii_cleaner import PIICleaner

def test_email_masking():
    cleaner = PIICleaner()
    raw_text = "Contacter jean.dupont@test.com pour la suite."
    cleaned, stats = cleaner.clean_text(raw_text)
    
    # Vérifications (Assertions)
    assert "<EMAIL_MASKED>" in cleaned
    assert "jean.dupont@test.com" not in cleaned
    assert stats.get("EMAIL") == 1

def test_phone_masking():
    cleaner = PIICleaner()
    raw_text = "Numéro : 06 12 34 56 78."
    cleaned, stats = cleaner.clean_text(raw_text)
    
    assert "<PHONE_MASKED>" in cleaned
    assert "06 12 34 56 78" not in cleaned
    assert stats.get("PHONE") == 1