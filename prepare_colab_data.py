import pandas as pd
import os

def prepare_data():
    print("Loading datasets...")
    
    # Paths to the old project data
    hinglish_path = "../project3/backend/data/hinglish_hate_speech.csv"
    english_path = "../project3/backend/data/english_test_data.csv"
    
    df_hinglish = pd.read_csv(hinglish_path)
    df_english = pd.read_csv(english_path)
    
    print(f"Hinglish rows: {len(df_hinglish)}")
    print(f"English rows: {len(df_english)}")
    
    # Standardize Hinglish (already has text, label, bns)
    df_hinglish = df_hinglish[['text', 'label', 'bns']]
    
    # Standardize English
    # Map label 0 -> Low (No Offense)
    # Map label 1 -> High (BNS 351)
    df_english['bns'] = df_english['label'].apply(lambda x: "No Offense" if x == 0 else "BNS 351 (Criminal Intimidation)")
    df_english['label'] = df_english['label'].apply(lambda x: "Low" if x == 0 else "High")
    df_english = df_english[['text', 'label', 'bns']]
    
    # Combine
    combined = pd.concat([df_hinglish, df_english], ignore_index=True)
    
    # Drop NaNs
    combined = combined.dropna()
    
    # Shuffle
    combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"Total Combined Rows: {len(combined)}")
    
    # Save to project4 data dir
    os.makedirs("data", exist_ok=True)
    out_path = "data/final_colab_dataset.csv"
    combined.to_csv(out_path, index=False)
    print(f"Dataset successfully prepared and saved to {out_path}!")

if __name__ == "__main__":
    prepare_data()
