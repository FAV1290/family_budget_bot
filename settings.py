
import os
import dotenv


dotenv.load_dotenv(dotenv.find_dotenv())
API_TOKEN = os.environ.get('API_TOKEN')
