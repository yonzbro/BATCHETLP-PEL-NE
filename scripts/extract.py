import os
from pathlib import Path
import requests
from dotenv import load_dotenv

# Proje kök dizinindeki .env dosyasının mutlak yolunu bul ve yükle
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def fetch_exchange_rates(base_currency="USD"):
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise ValueError(f".env dosyası arandı ({env_path}), ancak EXCHANGE_RATE_API_KEY bulunamadı. Lütfen .env dosyanızı kontrol edin.")
    
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}&base={base_currency}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
