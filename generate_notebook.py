import nbformat as nbf

nb = nbf.v4.new_notebook()

# Cell 1: Instructions
markdown_text = """# CyberNyaya - Google Colab Training (PyTorch MLP & GPU)
This notebook trains the Vernacular Cyber Harassment detection engine using a PyTorch MLP on a T4 GPU.

### Instructions:
1. Ensure you are connected to a T4 GPU (Runtime > Change runtime type > Hardware accelerator > T4 GPU).
2. Upload the `final_colab_dataset.csv` (generated locally) to the root of this Colab environment.
3. Run all cells."""
nb.cells.append(nbf.v4.new_markdown_cell(markdown_text))

# Cell 2: Setup
code_setup = """!pip install scikit-learn pandas nltk torch
import nltk
nltk.download('wordnet')"""
nb.cells.append(nbf.v4.new_code_cell(code_setup))

# Cell 3: Preprocessing Logic
code_preprocessing = """import re
import pandas as pd
from nltk.corpus import wordnet

HINGLISH_MAP = {
    "gadha": "idiot", "pagal": "stupid", "kutta": "dog", 
    "bakwas": "nonsense", "maar": "kill", "mar": "kill", 
    "dekh": "see", "tod": "break", "goli": "shoot", "jaan": "life"
}

def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    return re.sub(r'[^a-z0-9\\s]', '', text).strip()

def preprocess_pipeline(text):
    cleaned = clean_text(text)
    words = cleaned.split()
    processed_words = []
    for w in words:
        w_mapped = HINGLISH_MAP.get(w, w)
        processed_words.append(w_mapped)
    return " ".join(processed_words)

print("Loading dataset...")
df = pd.read_csv('final_colab_dataset.csv')
print(f"Dataset loaded: {len(df)} rows.")

print("Preprocessing data (this may take a minute)...")
df['processed_text'] = df['text'].apply(preprocess_pipeline)
print("Preprocessing complete!")"""
nb.cells.append(nbf.v4.new_code_cell(code_preprocessing))

# Cell 4: Train BNS Models (Naive Bayes & Decision Tree)
code_bns = """from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
import pickle

print("Training Naive Bayes with N-grams (BNS Section)...")
nb_pipeline = Pipeline([
    ('ngram', CountVectorizer(ngram_range=(1, 3))),
    ('nb', MultinomialNB(alpha=1.0))
])
nb_pipeline.fit(df['processed_text'], df['bns'])

print("Training Decision Tree (BNS Section)...")
dt_pipeline = Pipeline([
    ('ngram', CountVectorizer(ngram_range=(1, 2))),
    ('dt', DecisionTreeClassifier(random_state=42, max_depth=15))
])
dt_pipeline.fit(df['processed_text'], df['bns'])

with open("bns_nb_model.pkl", "wb") as f:
    pickle.dump(nb_pipeline, f)
print("BNS Models saved locally.")"""
nb.cells.append(nbf.v4.new_code_cell(code_bns))

# Cell 5: PyTorch MLP (Threat Level)
code_mlp = """import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Training on device: {device}")

# 1. TF-IDF Vectorization
print("Vectorizing for MLP...")
tfidf = TfidfVectorizer(max_features=2000)
X_tfidf = tfidf.fit_transform(df['processed_text']).toarray()

# Save TFIDF vectorizer for inference
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf, f)

# 2. Encode Labels
threat_map = {"Low": 0, "Medium": 1, "High": 2}
y_encoded = df['label'].map(threat_map).values

# 3. Create Tensors
X_tensor = torch.FloatTensor(X_tfidf).to(device)
y_tensor = torch.LongTensor(y_encoded).to(device)

dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=256, shuffle=True)

# 4. Define PyTorch MLP
class ThreatMLP(nn.Module):
    def __init__(self, input_size):
        super(ThreatMLP, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 3) # 3 threat classes

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = ThreatMLP(input_size=2000).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 5. Training Loop
print("Starting PyTorch Training...")
epochs = 15
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch_x, batch_y in loader:
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}/{epochs} - Loss: {total_loss/len(loader):.4f}")

# 6. Save Model
# We save the state_dict
torch.save(model.state_dict(), "threat_mlp_model.pt")
print("PyTorch Model Saved to threat_mlp_model.pt")"""
nb.cells.append(nbf.v4.new_code_cell(code_mlp))

# Cell 6: Download Files
code_download = """from google.colab import files
print("Downloading models...")
files.download("bns_nb_model.pkl")
files.download("tfidf_vectorizer.pkl")
files.download("threat_mlp_model.pt")
print("Done! Move these files to project4/models/ locally.")"""
nb.cells.append(nbf.v4.new_code_cell(code_download))

with open('colab_training.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook generated successfully!")
