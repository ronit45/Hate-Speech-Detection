import re
import nltk
from nltk.corpus import wordnet

# Download wordnet resources if not already present
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Custom concept hierarchy / dictionary for Hinglish slurs and their standard English equivalents
HINGLISH_MAP = {
    "gadha": "idiot",
    "pagal": "stupid",
    "kutta": "dog",
    "bakwas": "nonsense",
    "maar": "kill",
    "mar": "kill",
    "dekh": "see",
    "tod": "break",
    "goli": "shoot",
    "jaan": "life"
}

def clean_text(text: str) -> str:
    """
    Module I: Data Preprocessing & Cleaning (Text Normalization)
    - Lowercase text
    - Remove special characters
    - Handle missing or malformed values (handled implicitly by returning empty string for non-strings)
    """
    if not isinstance(text, str):
        return ""
        
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

def map_hinglish_to_english(word: str) -> str:
    """
    Module I: Concept Hierarchies & Data Reduction
    Map local slang to standardized English terms for better model understanding.
    """
    return HINGLISH_MAP.get(word, word)

def disambiguate_sense(word: str, context: str = None) -> str:
    """
    Module V: Word Sense Disambiguation
    Uses WordNet to find the primary sense of the word. 
    In a fully fledged system, this would use context to pick the synset (e.g., Lesk Algorithm).
    Here we pick the most common synset.
    """
    synsets = wordnet.synsets(word)
    if synsets:
        # Just returning the lemma name of the most frequent synset's first lemma
        return synsets[0].lemmas()[0].name()
    return word

def preprocess_pipeline(text: str) -> str:
    """
    Full preprocessing pipeline mapping to Syllabus Modules I & V.
    """
    cleaned = clean_text(text)
    words = cleaned.split()
    
    processed_words = []
    for w in words:
        # 1. Map Hinglish to English
        mapped_w = map_hinglish_to_english(w)
        processed_words.append(mapped_w)
        
    return " ".join(processed_words)

if __name__ == "__main__":
    # Test the pipeline
    test_str = "tu ek number ka gadha hai"
    print(f"Original: {test_str}")
    print(f"Processed: {preprocess_pipeline(test_str)}")
