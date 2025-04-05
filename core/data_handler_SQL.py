import sqlite3, os, datetime
from config import read_config

class DataHandler:
    def __init__(self):
        self.config_data = read_config()
        DB_Name = self.config_data.get('Database', 'DB_Name')
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), DB_Name)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        """
        Creates a table to store arbitrage data if it doesn't already exist.
        """
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.config_data.get('Database', 'DB_TABLE')} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                min_price TEXT NOT NULL,
                min_exchange TEXT NOT NULL,
                max_price TEXT NOT NULL,
                max_exchange TEXT NOT NULL,
                arbitrage_percentage TEXT NOT NULL,
                datetime TEXT NOT NULL
            )
        """)
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.config_data.get('Database', 'DB_TABLE_SUCCESS')} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                min_price TEXT NOT NULL,
                min_exchange TEXT NOT NULL,
                max_price TEXT NOT NULL,
                max_exchange TEXT NOT NULL,
                arbitrage_percentage TEXT NOT NULL,
                datetime TEXT NOT NULL
            )
        """)
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.config_data.get('Database', 'DB_TABLE_PRICES')} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price TEXT NOT NULL,
                exchange TEXT NOT NULL,
                symbol TEXT NOT NULL,
                datetime TEXT NOT NULL
            )
        """)             
        self.conn.commit()
        
    def insert_data(self, data):
        """
        Inserts arbitrage data into the database.
        Args:
            data (dict): Dictionary containing arbitrage data.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(f"INSERT INTO {self.config_data.get('Database', 'DB_TABLE')} (symbol, min_price, min_exchange, max_price, max_exchange, arbitrage_percentage, datetime) VALUES (?, ?, ?, ?, ?, ?, ?)", (data['symbol'], data['min_price'], data['min_exchange'], data['max_price'], data['max_exchange'], data['arbitrage_percentage'], timestamp))
        self.conn.commit()
    
    def insert_prices(self, prices, symbol):
        """
        Inserts prices into the database.
        Args:
            prices (dict): Dictionary containing prices from different exchanges.
            symbol (str): The symbol for which the prices are being inserted.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for exchange, price in prices.items():
            self.cursor.execute(f"INSERT INTO {self.config_data.get('Database', 'DB_TABLE_PRICES')} (price, exchange, symbol, datetime) VALUES (?, ?, ?, ?)", (price, exchange, symbol, timestamp))
            
    def insert_success_data(self, data):
        """
        Inserts successful arbitrage data into the database.
        Args:
            data (dict): Dictionary containing arbitrage data.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(f"INSERT INTO {self.config_data.get('Database', 'DB_TABLE_SUCCESS')} (symbol, min_price, min_exchange, max_price, max_exchange, arbitrage_percentage, datetime) VALUES (?, ?, ?, ?, ?, ?, ?)", (data["symbol"], data['min_price'], data['min_exchange'], data['max_price'], data['max_exchange'], data['arbitrage_percentage'], timestamp))
        self.conn.commit()