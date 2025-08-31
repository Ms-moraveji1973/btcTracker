import os
from dotenv import load_dotenv
from telethon import TelegramClient
load_dotenv()
proxy = {
    'proxy_type': 'socks5',
    'addr': '127.0.0.1',
    'port': 9052,
}
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

client = TelegramClient('sessions', API_ID, API_HASH,proxy=proxy)
async def send():
    if not client.is_connected():
        print('client connected')
        await client.connect()
    try :
        await client.send_message("+{your phone number}", "bitcoin's price increase 3%")
    except Exception as e:
        print(f"Error: {e}")


