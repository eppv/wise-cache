import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_URL = os.getenv('YOUTRACK_SERVICE_URL')
TOKEN = os.getenv('TOKEN')
