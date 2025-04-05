# -*- coding: UTF-8 -*-
import concurrent.futures
from threading import Thread
import time, logging, datetime
from config import read_config
from core import get_price_from_api, check_arbitrage, DataHandler, NotiHandler

class arbitrage_main:
    def __init__(self):
        """
        Initializes the arbitrage_main class.

        This constructor reads the configuration from the config.ini file, initializes the database and notification handlers, sets up logging, and prepares the class for operation.

        Attributes:
            config (ConfigParser): The configuration object with settings from the config.ini file.
            db_handler (DataHandler): An instance of the DataHandler class to manage data operations.
            noti_handler (NotiHandler): An instance of the NotiHandler class to handle notifications.
            thread_start (bool): A flag to indicate the start status of the threading operations.
        """

        self.config = read_config()
        self.db_handler = DataHandler()
        self.db_handler.create_files()
        self.noti_handler = NotiHandler()
        logging.basicConfig(filename='.\\logs\\arbitrage.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        self.config_setup()
        self.thread_start = False

   
    def config_setup(self):
        """
        Reads the configuration from the config.ini file and sets up the class variables.

        :param self: The instance of the class
        """
        self.SYMBOLS = self.config.get('Arbitrage Settings', 'SYMBOLS').replace(' ', '').split(',')
        self.SAVE_SMI = self.config.getboolean('Arbitrage Settings', 'PRICES_SAVE')
        self.ARBITRAGE_THRESHOLD = self.config.get('Arbitrage Settings', 'ARBITRAGE_THRESHOLD').replace(' ', '').split(',')
        self.TIMER_INTERVAL = self.config.getint('Arbitrage Settings', 'TIMER_INTERVAL')
        self.ARBITRAGE_SAVE = self.config.getboolean('Arbitrage Settings', 'ARBITRAGE_SAVE')
        self.ARBITRAGE_SUCCESS = self.config.getboolean('Arbitrage Settings', 'ARBITRAGE_SUCCESS_SAVE')
        self.TELEGRAM_STATUS = self.config.getboolean('Telegram', 'NOTIFICATION_STATUS')
        self.DISCORD_STATUS = self.config.getboolean('Discord', 'NOTIFICATION_STATUS')
              
    def get_api_urls(self, SYMBOL):
        """
        Builds a dictionary of API URLs for the given SYMBOL.

        :param SYMBOL: The symbol to fetch API URLs for
        :return: A dictionary of API URLs, keyed by exchange name
        """
        API_URLS = {}
        for section in self.config.sections():
            if not section.startswith("Exchange Details"):
                continue
            for exchange in self.config.options(section):
                if exchange.find("_") != -1 :
                    continue
                
                exchange = exchange.capitalize()
                
                SELECT_EXCHANGES = self.config.getboolean(section, exchange.upper() + "_STATUS")
                if SELECT_EXCHANGES:
                    API_URL = self.config.get(section, exchange)
                    if exchange == "Binance" or exchange == "Mexc" or exchange == "Bitget":
                        API_URL = API_URL.replace("SYMBOL", SYMBOL.replace("-", ""))
                    elif exchange == "Gate.io":
                        API_URL = API_URL.replace("SYMBOL", SYMBOL.replace("-", "_"))
                    else :
                        API_URL = API_URL.replace("SYMBOL", SYMBOL)
                        
                    if API_URL:
                        API_URLS[exchange] = API_URL
        return API_URLS

    def fetch_all_prices(self, api_urls):
        """
        Fetches price data from all exchanges concurrently.
        """
        prices = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(api_urls)) as executor:
            future_to_exchange = {executor.submit(get_price_from_api, exchange, url): exchange for exchange, url in api_urls.items()}
            for future in concurrent.futures.as_completed(future_to_exchange):
                exchange = future_to_exchange[future]
                price = future.result()
                if price is not None:
                    prices[exchange] = price
        return prices

    def arbitrage_check(self):
        """
        Fetches price data and checks for arbitrage at specified intervals.
        """
        api_urls = {symbol: self.get_api_urls(symbol) for symbol in self.SYMBOLS}
        print("SYMBOLS : ", self.SYMBOLS)
        while self.thread_start:
            try :
                symbol_list = list(api_urls.keys())
                n = 0
                for symbol in symbol_list:
                    try :
                        prices = self.fetch_all_prices(api_urls[symbol])
                        data = check_arbitrage(prices,float(self.ARBITRAGE_THRESHOLD[n]))
                        data["real_data"]["symbol"] = symbol
                        if data["valid_price"] :
                            if self.ARBITRAGE_SAVE:
                                self.db_handler.insert_data(data["real_data"])
                            if self.SAVE_SMI:
                                self.db_handler.insert_prices(data["real_data"]["prices"], symbol)
                            if data["success"] and self.ARBITRAGE_SUCCESS:
                                self.db_handler.insert_success_data(data["real_data"])

                                message = f"Arbitrage Opportunity Found!\nSymbol: {symbol}\nMin Price: {data['real_data']['min_price']}\nMax Price: {data['real_data']['max_price']}\nMin Exchange: {data['real_data']['min_exchange']}\nMax Exchange: {data['real_data']['max_exchange']}\nArbitrage Percentage: {round(data['real_data']['arbitrage_percentage'],3)}%\nDatetime: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                if self.DISCORD_STATUS:
                                    res = self.noti_handler.discord_send_message(str(message))
                                    if res != True:
                                        logging.error(f"Discord message failed for {symbol}")
                                if self.TELEGRAM_STATUS:
                                    res = self.noti_handler.telegram_send_message(str(message))
                                    if res != True:
                                        logging.error(f"Telegram message failed for {symbol}")
                        n+=1
                    except Exception as e:
                        logging.error(f"{e} - {symbol}")
                time.sleep(self.TIMER_INTERVAL)
            except Exception as e:
                logging.error(f"{e} - {symbol}")
      
    def get_arbitrage_data(self,json_file):
        """
        Fetches arbitrage data from the database.
        Args:
            json_file (str): The JSON file to fetch data from.
        """
        try:
            data = self.db_handler.fetch_all_data(json_file)
            return data
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            return None


if __name__ == "__main__":
    main = arbitrage_main()
    menu = """
====== Crypto Arbitrage Alert Bot Menu ======
1 - Start Arbitrage Check
2 - Check Status / Stop Bot
3 - View Arbitrage Data
4 - Config Overview
5 - Exit the Program
====================================
"""

    try:
        while True:
            print(menu)
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                if main.thread_start:
                    print("Arbitrage check is already running.")
                else:
                    main.thread_start = True
                    th = Thread(target=main.arbitrage_check)
                    th.start()
                    print("Arbitrage check started...")

            elif choice == "2":
                print(f"Thread Status: {'Running' if main.thread_start else 'Stopped'}")
                if main.thread_start:
                    choice_THREAD = input("Do you want to stop the arbitrage check? (y/n): ").strip().lower()
                    if choice_THREAD == "y":
                        main.thread_start = False
                        print("Stopping arbitrage check...")
                        if th.is_alive():
                            th.join()
                        print("Arbitrage check stopped.")

            elif choice == "3":
                print("\n----- Data Menu -----\n1 - Arbitrage Opportunities\n2 - Successful Arbitrage Logs\n3 - Price Logs")
                choice_DATA = input("Enter your choice: ").strip()

                json_map = {"1": "arbitrage", "2": "success", "3": "prices"}
                json_file = json_map.get(choice_DATA)
                try :
                    count_input = int(input("Enter the number of records to fetch (default is 10): ").strip())
                except ValueError:
                    count_input = 10
                
                if json_file:
                    data = main.get_arbitrage_data(json_file)
                    if data:
                        if count_input > len(data.items()) :
                            count_input = len(data.items())
                        print(f"\n--- {json_file.capitalize()} Data ---")
                        
                        for key, value in list(data.items())[-count_input:]:
                            print(value)
                            
                        print("--- End of data. ---")                       
                        print(f"\nTotal records: {len(data.items())}")
                        print(f"Showing last {count_input} records.")
                    else:
                        print("\nNo data found.")
                else:
                    print("Invalid data choice.")

            elif choice == "4":
                print("\n----- Config Settings Overview -----")
                print("Symbols:", main.SYMBOLS)
                print("Arbitrage Thresholds:", main.ARBITRAGE_THRESHOLD)
                print("Timer Interval:", main.TIMER_INTERVAL, "seconds")
                print("Multiprocessing:", main.MULTI_PROCESSING)
                print("Save Prices:", main.SAVE_SMI)
                print("Exchanges Enabled:")
                for symbol in main.SYMBOLS:
                    api_urls = main.get_api_urls(symbol)
                    print(f"  {symbol}: {list(api_urls.keys())}")

            elif choice == "5":
                print("Exiting program...")
                break

            else:
                print("Invalid choice. Please select a valid option.")

    except KeyboardInterrupt:
        logging.info("Program terminated by user.")