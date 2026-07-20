import os
import re
import pandas as pd
import numpy as np
import pickle
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import copy

# ==========================================
# 1. STANDALONE PREPROCESSING LOGIC
# ==========================================
# In Colab, we don't have access to external files, so we bundle the preprocessing here.

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
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

def preprocess_pipeline(text: str) -> str:
    cleaned = clean_text(text)
    words = cleaned.split()
    processed_words = [HINGLISH_MAP.get(w, w) for w in words]
    return " ".join(processed_words)

# ==========================================
# 2. COLAB FILE PATHS
# ==========================================
# Ensure you upload 'v2_training_dataset.csv' directly to your Colab session!
DATA_PATH = "v2_training_dataset.csv"
MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

print("Loading Data...")
if not os.path.exists(DATA_PATH):
    print(f"ERROR: '{DATA_PATH}' not found! Please upload it to your Colab session.")
    exit(1)

df = pd.read_csv(DATA_PATH)
df['text'] = df['text'].apply(preprocess_pipeline) # Fixed to use full pipeline

label_map = {"Low": 0, "Medium": 1, "High": 2}
df['label_idx'] = df['threat_level'].map(label_map)

# Fix Pandas treating the string "None" as NaN
df['bns_section'] = df['bns_section'].fillna("None")

# ==========================================
# 3. 80/20 Split (CRITICAL REQUIREMENT)
# ==========================================
print("Splitting data (80% Train, 20% Validation)...")
X_train_raw, X_val_raw, y_train, y_val, bns_train, bns_val = train_test_split(
    df['text'], 
    df['label_idx'], 
    df['bns_section'], 
    test_size=0.20, 
    random_state=42, 
    stratify=df['label_idx']
)

print(f"Training Set: {len(X_train_raw)} rows")
print(f"Validation Set: {len(X_val_raw)} rows")

# ==========================================
# 4. TF-IDF Vectorization
# ==========================================
print("Vectorizing Text...")
vectorizer = TfidfVectorizer(max_features=2000, stop_words='english')
X_train = vectorizer.fit_transform(X_train_raw).toarray()
X_val = vectorizer.transform(X_val_raw).toarray()

with open(os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

# ==========================================
# 5. Train Naive Bayes (for BNS Sections)
# ==========================================
print("Training Naive Bayes Classifier...")
nb_model = MultinomialNB()
nb_model.fit(X_train, bns_train)
nb_val_preds = nb_model.predict(X_val)
nb_acc = accuracy_score(bns_val, nb_val_preds)
print(f"Naive Bayes Validation Accuracy: {nb_acc * 100:.2f}%")

with open(os.path.join(MODELS_DIR, "bns_nb_model.pkl"), "wb") as f:
    pickle.dump(nb_model, f)

# ==========================================
# 6. Train PyTorch MLP with EARLY STOPPING
# ==========================================
print("\n--- Training PyTorch MLP with Early Stopping ---")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

X_train_tensor = torch.FloatTensor(X_train).to(device)
y_train_tensor = torch.LongTensor(y_train.values).to(device)
X_val_tensor = torch.FloatTensor(X_val).to(device)
y_val_tensor = torch.LongTensor(y_val.values).to(device)

class ThreatMLP(nn.Module):
    def __init__(self, input_dim):
        super(ThreatMLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 3)
        )
        
    def forward(self, x):
        return self.network(x)

actual_input_dim = X_train.shape[1]
print(f"Neural Network Input Dimension: {actual_input_dim}")
model = ThreatMLP(input_dim=actual_input_dim).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

EPOCHS = 100 
PATIENCE = 3
best_val_loss = float('inf')
best_val_acc = 0.0
patience_counter = 0
best_model_weights = None

for epoch in range(EPOCHS):
    model.train()
    optimizer.zero_grad()
    
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()
    
    _, predicted_train = torch.max(outputs.data, 1)
    train_acc = (predicted_train == y_train_tensor).sum().item() / len(y_train_tensor)
    
    model.eval()
    with torch.no_grad():
        val_outputs = model(X_val_tensor)
        val_loss = criterion(val_outputs, y_val_tensor).item()
        _, predicted_val = torch.max(val_outputs.data, 1)
        val_acc = (predicted_val == y_val_tensor).sum().item() / len(y_val_tensor)
        
    print(f"Epoch [{epoch+1:02d}] | Train Acc: {train_acc*100:.2f}% | Val Acc: {val_acc*100:.2f}% | Val Loss: {val_loss:.4f}")
    
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        best_val_acc = val_acc
        patience_counter = 0
        best_model_weights = copy.deepcopy(model.state_dict())
    else:
        patience_counter += 1
        print(f"  -> No improvement in validation loss. Patience: {patience_counter}/{PATIENCE}")
        if patience_counter >= PATIENCE:
            print(f"\n[!] EARLY STOPPING TRIGGERED AT EPOCH {epoch+1}")
            print(f"[!] Validation accuracy stopped improving. Reverting to best weights.")
            break

if best_model_weights is not None:
    model.load_state_dict(best_model_weights)

print(f"\nFinal Restored Validation Accuracy: {best_val_acc * 100:.2f}%")
torch.save(model.state_dict(), os.path.join(MODELS_DIR, "threat_mlp_model.pt"))
print("All Models saved successfully to models/ directory. Download the models/ folder to your local machine!")
