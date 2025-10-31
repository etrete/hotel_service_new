import os
import time
import psycopg2
from django.db import connections
from django.db.utils import OperationalError

def wait_for_db():
    """Ожидание готовности базы данных"""
    print("Ожидаем базу данных...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB', 'hotel_db'),
                user=os.getenv('POSTGRES_USER', 'postgres'),
                password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
                host=os.getenv('POSTGRES_HOST', 'db'),
                port=os.getenv('POSTGRES_PORT', '5432')
            )
            conn.close()
            print("База данных готова!")
            return True
        except psycopg2.OperationalError:
            retry_count += 1
            print(f"База данных не готова, повторяем попытку... ({retry_count}/{max_retries})")
            time.sleep(2)
    
    print("Не удалось подключиться к базе данных после повторных попыток")
    return False

if __name__ == "__main__":
    wait_for_db()