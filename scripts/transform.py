import pandas as pd
from datetime import datetime

def transform_exchange_data(raw_data):
    timestamp = raw_data.get("timestamp")
    rates = raw_data.get("rates", {})
    
    if not timestamp or not rates:
        raise ValueError("API'den gelen ham veri formatı geçersiz.")
    
    # DataFrame oluşturma
    df = pd.DataFrame(list(rates.items()), columns=['currency_code', 'rate_to_usd'])
    
    # Timestamp ve Tarih Düzenlemeleri
    date_obj = datetime.fromtimestamp(timestamp)
    df['full_date'] = date_obj.strftime('%Y-%m-%d')
    df['date_id'] = int(date_obj.strftime('%Y%m%d'))
    
    # Null & Tip Kontrolleri
    df.dropna(inplace=True)
    df['rate_to_usd'] = df['rate_to_usd'].astype(float)
    
    # Seçili kurları filtreleme (Örn: EUR, TRY, GBP, JPY, CAD)
    target_currencies = ['TRY', 'EUR', 'GBP', 'JPY', 'CAD']
    df = df[df['currency_code'].isin(target_currencies)].copy()
    
    return df
