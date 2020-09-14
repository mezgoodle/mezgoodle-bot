import os

from dotenv import load_dotenv
load_dotenv()

PRIVATE_KEY = os.environ.get('GH_PRIVATE_KEY')
APP_ID = os.environ.get('GH_APP_ID')
SECRET = os.environ.get('GH_SECRET')
