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
    # Pronouns / Generic
    "tu": "you", "tera": "your", "teri": "your", "mera": "my", "meri": "my",
    "main": "i", "hum": "we", "iska": "his", "iski": "her", "isko": "him",
    "woh": "he", "yeh": "this", "tujhe": "you", "tum": "you", "sab": "all",
    "unko": "them", "inko": "them", "idhar": "here", "udhar": "there",
    "yahan": "here", "wahan": "there", "kahan": "where", "kaun": "who",
    "kya": "what", "kaise": "how", "kab": "when", "kyun": "why",
    
    # Nouns & Family
    "bhai": "brother", "bhaiya": "brother", "baap": "father", "maa": "mother",
    "behan": "sister", "dost": "friend", "ghar": "house", "walo": "family",
    "log": "people", "banda": "guy", "ladka": "boy", "ladki": "girl",
    "raat": "night", "din": "day", "aaj": "today", "kal": "tomorrow",
    "sakal": "face", "muh": "face", "zuban": "tongue", "aukat": "status",
    "izzat": "respect", "sharam": "shame", "chacha": "uncle", "mama": "uncle",
    "padosi": "neighbor", "bacha": "child", "billi": "cat", "kutta": "dog",
    "kutti": "dog", "aurat": "woman", "aadmi": "man",
    
    # Adjectives / Insults / Cyberbullying
    "pagal": "idiot", "gadha": "idiot", "bewakoof": "idiot", "buddhu": "idiot",
    "chutiya": "idiot", "chutiye": "idiot", "nalayak": "loser", "nalla": "loser", 
    "chapri": "loser", "gawar": "uneducated", "bhikhari": "beggar", "chor": "thief", 
    "dhokebaaz": "fraud", "kamina": "scoundrel", "kaminay": "scoundrel",
    "harami": "bastard", "sala": "bastard", "fattu": "coward", "faltu": "useless",
    "bekaar": "useless", "ghatiya": "disgusting", "mc": "motherfucker", 
    "bc": "sisterfucker", "maderchod": "motherfucker", "bhenchod": "sisterfucker",
    "bhosdike": "asshole", "gaandu": "asshole", "lodu": "asshole", 
    "bharwa": "pimp", "raand": "whore", "randi": "whore", "tharki": "pervert",
    "chamcha": "sycophant", "dalal": "broker", "jhantu": "pubic", "tatti": "shit",
    "besharam": "shameless", "ganda": "dirty", "bakwas": "nonsense", 
    "bakchodi": "bullshit", "randirona": "crying", 
    "mast": "great", "badhiya": "great", "zabardast": "great", "khatarnak": "dangerous",
    "accha": "good", "bura": "bad", "thik": "okay", "kharab": "bad",
    
    # Verbs / Actions (Violence & Benign)
    "maar": "hit", "mar": "hit", "goli": "shoot", "gaad": "bury", "kat": "cut",
    "phek": "throw", "daba": "choke", "tod": "break", "suja": "swell",
    "khatam": "finish", "dekh": "see", "bol": "speak", "samajh": "understand",
    "dikh": "look", "reh": "stay", "udd": "fly", "phod": "break",
    "chaku": "knife", "bandook": "gun", "thappad": "slap", "lafa": "slap",
    "laat": "kick", "ghusa": "punch", "pel": "beat", "thok": "shoot",
    "uda": "blow", "phansi": "hang", "zehar": "poison",
    "kha": "eat", "pee": "drink", "so": "sleep", "jaa": "go", "aa": "come",
    "chal": "walk", "bhag": "run", "ruk": "stop", "sun": "listen",
    "padh": "read", "likh": "write", "khel": "play", "mil": "meet",
    "ro": "cry", "has": "laugh",
    
    # Adverbs / Modifiers
    "hamesha": "always", "kabhi": "never", "bilkul": "totally", "ekdum": "totally",
    "maha": "huge", "sabse": "most", "bada": "big", "zinda": "alive",
    "akela": "alone", "chup": "quiet", "bahut": "very", "thora": "little",
    "jaldi": "fast", "dheere": "slow", "bahar": "outside", "andar": "inside"
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
