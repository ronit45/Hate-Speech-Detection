from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import os
import sys
import torch

# Add parent directory to path so we can import preprocessing
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocessing import preprocess_pipeline
from predict import generate_complaint
from ml_models import ThreatMLP

app = FastAPI(title="CyberNyaya Backend API (PyTorch Enabled)")

# Configure CORS for Vite Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models
nb_model = None
tfidf_vectorizer = None
mlp_model = None
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
device = torch.device("cpu") # Backend inference can run fast enough on CPU

try:
    with open(os.path.join(MODEL_DIR, "bns_nb_model.pkl"), "rb") as f:
        nb_model = pickle.load(f)
        
    with open(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"), "rb") as f:
        tfidf_vectorizer = pickle.load(f)
        
    # Load PyTorch Model weights
    mlp_model = ThreatMLP(input_size=2000)
    mlp_model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "threat_mlp_model.pt"), map_location=device, weights_only=True))
    mlp_model.eval() # Set to evaluation mode
    
    print("Models loaded successfully (including PyTorch)!")
except Exception as e:
    print(f"Warning: Could not load models. Ensure Colab training is done and models are in the models/ folder. Error: {e}")

class AnalyzeRequest(BaseModel):
    text: str

class ComplaintRequest(BaseModel):
    original_text: str
    bns_section: str
    threat_level: str

@app.get("/")
def health_check():
    return {"status": "CyberNyaya Backend is running", "models_loaded": nb_model is not None and mlp_model is not None}

@app.post("/api/analyze")
def analyze_text(request: AnalyzeRequest):
    if not nb_model or not mlp_model or not tfidf_vectorizer:
        raise HTTPException(status_code=500, detail="Models are not loaded.")
        
    text = request.text
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
        
    processed = preprocess_pipeline(text)
    
    # Predict BNS
    bns_section = nb_model.predict([processed])[0]
    
    # Predict Threat Level (PyTorch)
    tfidf_vector = tfidf_vectorizer.transform([processed]).toarray()
    tensor_input = torch.FloatTensor(tfidf_vector)
    
    with torch.no_grad():
        outputs = mlp_model(tensor_input)
        _, predicted = torch.max(outputs, 1)
        
    threat_map = {0: "Low", 1: "Medium", 2: "High"}
    threat_level = threat_map[predicted.item()]
    
    return {
        "original_text": text,
        "processed_text": processed,
        "threat_level": threat_level,
        "bns_section": bns_section
    }

@app.post("/api/complaint/generate")
def get_complaint(request: ComplaintRequest):
    draft = generate_complaint(request.original_text, request.bns_section, request.threat_level)
    return {"draft": draft}
