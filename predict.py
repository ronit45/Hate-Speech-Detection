import pickle
import os
from preprocessing import preprocess_pipeline

def load_models():
    if not os.path.exists("models"):
        print("Models not found. Please run train_models.py first.")
        return None, None
        
    with open("models/bns_nb_model.pkl", "rb") as f:
        nb_model = pickle.load(f)
    with open("models/threat_mlp_model.pkl", "rb") as f:
        mlp_model = pickle.load(f)
        
    return nb_model, mlp_model

def generate_complaint(original_text, bns_section, threat_level):
    if threat_level == "Low":
        return "No formal complaint required as the threat level is low."
        
    draft = f"""---
FORMAL CYBER CRIME COMPLAINT DRAFT
---
To the Cyber Crime Cell,

This is to officially report a case of online cyber harassment and/or hate speech. 
On the date of this report, the following text was directed at me:

"{original_text}"

Based on the automated assessment by the Vernacular Cyber Harassment Detection Engine:
- Assessed Threat Level: {threat_level}
- Primary Offense Category: {bns_section}

I request immediate investigation into this matter under the relevant sections of the Bharatiya Nyaya Sanhita (BNS).

Sincerely,
[Your Name]
"""
    return draft

def analyze(text):
    nb_model, mlp_model = load_models()
    if not nb_model or not mlp_model:
        return
        
    processed = preprocess_pipeline(text)
    
    bns_section = nb_model.predict([processed])[0]
    threat_level = mlp_model.predict([processed])[0]
    
    print("=" * 50)
    print(f"INPUT TEXT: {text}")
    print(f"PROCESSED : {processed}")
    print("-" * 50)
    print(f"PREDICTED THREAT LEVEL : {threat_level}")
    print(f"PREDICTED BNS SECTION  : {bns_section}")
    print("=" * 50)
    print(generate_complaint(text, bns_section, threat_level))
    print("=" * 50)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyze(" ".join(sys.argv[1:]))
    else:
        # Default test case
        analyze("tu ek number ka gadha hai, I will kill you")
