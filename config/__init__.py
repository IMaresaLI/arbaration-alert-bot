import configparser
import os



def read_config(config_path="config/config.ini"):
    """
    Reads the config.ini file at the specified file path.
    """
    config = configparser.ConfigParser()
    # config.read(config_path) #if the config is in the config folder.
    config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)),config_path)) #if the config is in the Auto_Arbitration folder.
    return config