import  os, json, datetime
from config import read_config

class DataHandler:
    def __init__(self):
        """
        Initializes the DataHandler class.

        The class reads the configuration from the config.ini file, gets the path to the database folder from the configuration, and creates the folder if it doesn't exist.

        :param config: The configuration read from the config.ini file
        """
        self.config_data = read_config()
        DB_Name = self.config_data.get('Database', 'MAIN_FOLDER')
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), DB_Name)
    
    def create_files(self):
        """
        Creates the database folder and the JSON files for storing arbitrage data and prices if they don't already exist.

        The method reads the database folder path from the configuration file and creates the folder if it doesn't exist.
        It also creates three JSON files for storing arbitrage data, successful arbitrage data, and prices if they don't already exist.

        :return: None
        """
        os.makedirs(self.db_path, exist_ok=True)
        self.arbitrage_json = os.path.join(self.db_path, self.config_data.get('Database', 'ARBITRAGE_JSON'))
        self.arbitrage_success = os.path.join(self.db_path, self.config_data.get('Database', 'ARBITRAGE_SUCCESS'))
        self.prices_json = os.path.join(self.db_path, self.config_data.get('Database', 'PRICES'))
        
        if os.path.exists(self.arbitrage_json) != True:
            with open(self.arbitrage_json, 'w') as f:
                json.dump({}, f)
        if os.path.exists(self.arbitrage_success) != True:
            with open(self.arbitrage_success, 'w') as f:
                json.dump({}, f)
        if os.path.exists(self.prices_json) != True:
            with open(self.prices_json, 'w') as f:
                json.dump({}, f)
             
    def insert_data(self, data):
        """
        Inserts arbitrage data into the database.
        Args:
            data (dict): Dictionary containing arbitrage data.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.arbitrage_json, 'r') as f:
            arbitrage_data = json.load(f)
        with open(self.arbitrage_json, 'w') as f:
            arbitrage_data[timestamp] = {
                'symbol': data['symbol'],
                'min_price': data['min_price'],
                'min_exchange': data['min_exchange'],
                'max_price': data['max_price'],
                'max_exchange': data['max_exchange'],
                'arbitrage_percentage': data['arbitrage_percentage'],
                'datetime': timestamp
            }
            json.dump(arbitrage_data, f)
    
    def insert_prices(self, prices, symbol):
        """
        Inserts prices into the database.
        Args:
            prices (dict): Dictionary containing prices from different exchanges.
            symbol (str): The symbol for which the prices are being inserted.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.prices_json, 'r') as f:
            prices_data = json.load(f)
        with open(self.prices_json, 'w') as f:
            prices_data[timestamp] = {
                'symbol': symbol,
                'prices': prices,
                'datetime': timestamp
            }
            json.dump(prices_data, f)
            
    def insert_success_data(self, data):
        """
        Inserts successful arbitrage data into the database.
        Args:
            data (dict): Dictionary containing arbitrage data.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.arbitrage_success, 'r') as f:
            success_data = json.load(f)
        with open(self.arbitrage_success, 'w') as f:
            success_data[timestamp] = {
                'symbol': data['symbol'],
                'min_price': data['min_price'],
                'min_exchange': data['min_exchange'],
                'max_price': data['max_price'],
                'max_exchange': data['max_exchange'],
                'arbitrage_percentage': data['arbitrage_percentage'],
                'datetime': timestamp
            }            
            json.dump(success_data, f)
        
    def fetch_all_data(self, json_file):
        """
        Fetches arbitrage data from the database. 
        Args:
            json_file (str): The JSON file to fetch data from.
        Returns:
            dict: Dictionary containing arbitrage data.  
        """
        if json_file == "arbitrage":
            self.arbitrage_json = os.path.join(self.db_path, self.config_data.get('Database', 'ARBITRAGE_JSON'))
        elif json_file == "success":
            self.arbitrage_json = os.path.join(self.db_path, self.config_data.get('Database', 'ARBITRAGE_SUCCESS'))
        elif json_file == "prices":
            self.arbitrage_json = os.path.join(self.db_path, self.config_data.get('Database', 'PRICES'))
            
        with open(self.arbitrage_json, 'r') as f:
            data = json.load(f)
        return data
