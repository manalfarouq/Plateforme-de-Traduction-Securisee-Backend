import requests
from app.core.config import settings

# Récupérer le token depuis Pydantic Settings
HF_TOKEN = settings.HF_TOKEN

if not HF_TOKEN:
    raise ValueError("HF_TOKEN non trouvé dans .env")

def query(text, model):
    api_url = f"https://router.huggingface.co/hf-inference/models/{model}"
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    # Vérifier si la réponse est correcte
    if response.status_code != 200:
        raise Exception(f"Erreur Hugging Face: {response.status_code} - {response.text}")
    
    result = response.json()
    
    # Gérer le format de réponse
    # HF retourne une liste de dicts avec 'translation_text'
    if isinstance(result, list) and len(result) > 0:
        return result[0].get('translation_text', result)
    
    return result

# # Test traduction FR -> EN
# text_fr = "Bonjour"
# result_en = query(text_fr, "Helsinki-NLP/opus-mt-fr-en")
# print("FR -> EN:", result_en)

# # Test traduction EN -> FR
# text_en = "Hello"
# result_fr = query(text_en, "Helsinki-NLP/opus-mt-en-fr")
# print("EN -> FR:", result_fr)