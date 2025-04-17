import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.conn = None
        
    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=os.getenv('DB_HOST'),
                    database=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    port=os.getenv('DB_PORT')
                )
            except psycopg2.Error as e:
                print(f"Error connecting to database: {e}")
                raise
        return self.conn

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
