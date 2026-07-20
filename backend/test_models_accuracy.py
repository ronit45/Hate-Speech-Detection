import sys
import os
import pickle
import torch
import pandas as pd
from sklearn.metrics import classification_report

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml_models import ThreatMLP
from preprocessing import preprocess_pipeline

def evaluate():
    MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
    DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "final_colab_dataset.csv")
    
    print("Loading datasets for evaluation...")
    if not os.path.exists(DATA_PATH):
        print(f"Dataset not found at {DATA_PATH}")
        return
        
    df = pd.read_csv(DATA_PATH).sample(n=1000, random_state=42) # Evaluate on a subset of 1000 rows
    
    print("Loading Models...")
    try:
        with open(os.path.join(MODEL_DIR, "bns_nb_model.pkl"), "rb") as f:
            nb_model = pickle.load(f)
        with open(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"), "rb") as f:
            tfidf_vectorizer = pickle.load(f)
            
        mlp_model = ThreatMLP(input_size=2000)
        mlp_model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "threat_mlp_model.pt"), map_location=torch.device('cpu'), weights_only=True))
        mlp_model.eval()
    except Exception as e:
        print(f"Error loading models: {e}")
        return

    print("Preprocessing evaluation data...")
    df['processed'] = df['text'].apply(preprocess_pipeline)
    
    print("Evaluating Naive Bayes (BNS Section)...")
    bns_preds = nb_model.predict(df['processed'])
    print("\n--- BNS Section Classification Report ---")
    print(classification_report(df['bns'], bns_preds, zero_division=0))
    
    print("Evaluating PyTorch MLP (Threat Level)...")
    tfidf_matrix = tfidf_vectorizer.transform(df['processed']).toarray()
    tensor_inputs = torch.FloatTensor(tfidf_matrix)
    
    with torch.no_grad():
        outputs = mlp_model(tensor_inputs)
        _, preds = torch.max(outputs, 1)
        
    threat_map = {0: "Low", 1: "Medium", 2: "High"}
    pred_labels = [threat_map[p.item()] for p in preds]
    
    print("\n--- Threat Level Classification Report ---")
    print(classification_report(df['label'], pred_labels, zero_division=0))

if __name__ == "__main__":
    evaluate()
