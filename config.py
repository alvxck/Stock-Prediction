import os
from dotenv import load_dotenv

load_dotenv()
FLASK_APP = os.getenv("FLASK_APP")