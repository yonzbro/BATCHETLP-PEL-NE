import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv

# Proje kök dizinindeki .env dosyasını otomatik bul ve yükle
load_dotenv(find_dotenv())

def load_data_to_db(df):
    if df.empty:
        print("DataFrame boş, veritabanına yükleme atlanıyor.")
        return

    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME')
    sslmode = os.getenv('DB_SSLMODE', 'require')

    if not all([db_user, db_pass, db_host, db_name]):
        raise ValueError("Veritabanı bağlantı bilgileri .env dosyasında eksik!")

    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?sslmode={sslmode}"
    engine = create_engine(db_url)
    
    with engine.begin() as conn:
        # 1. Dim Date Güncelleme (SQLAlchemy text() nesnesi ile güvenli parametrik SQL)
        date_id = int(df['date_id'].iloc[0])
        full_date = str(df['full_date'].iloc[0])
        dt = pd.to_datetime(full_date)
        
        insert_date_sql = text("""
            INSERT INTO dim_date (date_id, full_date, year, month, day, day_of_week)
            VALUES (:date_id, :full_date, :year, :month, :day, :day_of_week)
            ON CONFLICT (date_id) DO NOTHING;
        """)
        
        conn.execute(insert_date_sql, {
            "date_id": date_id,
            "full_date": full_date,
            "year": int(dt.year),
            "month": int(dt.month),
            "day": int(dt.day),
            "day_of_week": dt.day_name()
        })
        
        # 2. Fact Tablosuna Ekleme (currency_id haritalaması ile)
        dim_curr = pd.read_sql(text("SELECT currency_id, currency_code FROM dim_currency"), conn)
        merged_df = df.merge(dim_curr, on='currency_code')
        
        fact_df = merged_df[['currency_id', 'date_id', 'rate_to_usd']]
        fact_df.to_sql('fact_exchange_rates', conn, if_exists='append', index=False)