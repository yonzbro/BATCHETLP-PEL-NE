import sys
import logging
from dotenv import load_dotenv

# Modülleri içe aktarma
from extract import fetch_exchange_rates
from transform import transform_exchange_data
from load import load_data_to_db

# Logging Yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_pipeline():
    logging.info("ETL Boru Hattı Başlatıldı.")
    
    # Lokal çalıştırmada .env dosyasını oku
    load_dotenv()
    
    try:
        # Adım 1: Extract
        raw_data = fetch_exchange_rates()
        
        # Adım 2: Transform
        transformed_df = transform_exchange_data(raw_data)
        
        # Adım 3: Load
        load_data_to_db(transformed_df)
        
        logging.info("ETL Boru Hattı Başarıyla Tamamlandı!")
        
    except Exception as e:
        logging.error(f"ETL Boru Hattı Başarısız Oldu! Hata: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()