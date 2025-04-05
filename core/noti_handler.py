import requests
from config import read_config

class NotiHandler:
    """
    A class to handle notifications via Telegram.
    """
    def __init__(self):
        """
        Initializes the NotiHandler class.

        Reads the bot token and chat ID from the config.ini file and stores them as instance variables.

        :param config: The configuration read from the config.ini file
        """
        self.config_data = read_config()
        self.bot_token = self.config_data.get('Telegram', 'TELEGRAM_BOT_TOKEN')
        self.chat_id = self.config_data.get('Telegram', 'TELEGRAM_CHAT_ID')
        self.webhook_url = self.config_data.get('Discord', 'DISCORD_WEBHOOK_URL')
        
    def telegram_send_message(self, bot_message):
        """
        Sends a message to the configured Telegram chat.

        Args:
            bot_message (str): The message to be sent to the Telegram chat.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """

        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage'
        PARAMS = {
            'chat_id': self.chat_id,
            'text': bot_message
        }

        response = requests.post(send_text, params=PARAMS)

        if response.status_code != 200:
            return False
        else :
            return True

    def telegram_chat_id(self):
        """
        Returns a list of tuples (chat_id, name) where name is either the username, first name or title of the chat.
        If there are no updates, returns None.
        """
        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
        response = requests.get(url)
        data = response.json()
        if 'result' not in data or len(data['result']) == 0:
            return None
        # Get the chat ID from the first result
        chat_list = []
        for result in data['result']:
            chat_id = result['message']['chat']['id']
            try :
                name = result['message']['chat']['username']
            except KeyError:
                try :
                    name = result['message']['chat']['first_name']
                except KeyError:
                    name = result['message']['chat']['title']
            chat_list.append((chat_id, name))
        return chat_list

    def discord_send_message(self, bot_message):
        """
        Sends a message to a Discord channel using a webhook.

        Args:
            bot_message (str): The message content to be sent to the Discord channel.

        Returns:
            bool: True if the message is successfully sent, False otherwise.
        """
        data = {
            "content": bot_message,
            "username": "Arbitrage Bot"
        }
        response = requests.post(self.webhook_url, json=data)
        if response.status_code != 204:
            return False
        else :
            return True

