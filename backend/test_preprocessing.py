import sys
import os
import pytest

# Add parent directory to path to import preprocessing
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocessing import clean_text, map_hinglish_to_english, preprocess_pipeline

def test_clean_text_basic():
    assert clean_text("Hello World!") == "hello world"
    assert clean_text("UPPERCASE") == "uppercase"
    assert clean_text("Special @#$ Characters &*()") == "special  characters"

def test_clean_text_nan():
    # Should handle non-string inputs safely by returning empty string
    assert clean_text(None) == ""
    assert clean_text(float('nan')) == ""

def test_map_hinglish_to_english():
    assert map_hinglish_to_english("gadha") == "idiot"
    assert map_hinglish_to_english("maar") == "kill"
    assert map_hinglish_to_english("randomword") == "randomword"

def test_preprocess_pipeline():
    # Verify WordNet logic is removed and it doesn't over-translate
    # e.g., "I will kill you" should remain "i will kill you", not "iodine volition..."
    res = preprocess_pipeline("I will kill you")
    assert res == "i will kill you"
    
    # Verify Hinglish translation still works
    res2 = preprocess_pipeline("tu ek gadha hai")
    assert "idiot" in res2
