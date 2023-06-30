import os
import dotenv


dotenv.load_dotenv(dotenv.find_dotenv())


API_TOKEN = os.environ.get('API_TOKEN')
FILEPATH = 'app_data.json'
COMMANDS = {
    '/add_category' : '• /add_category [Имена категорий через запятую] :\nДобавить категории расходов', 
    '/categories' : '• /categories : Список категорий расходов', 
    '/add' : '• /add [Сумма] [Комментарий - необязательно] :\nДобавить расход на заданную сумму',
    '/expenses' : '• /expenses : Список расходных операций',
    '/help' : '• /help : Перечень доступных команд',
}
DEFAULT_DATA_DICT = {
    'expenses' : [],
    'categories' : [],
    'settings' : [],
}
MISCELLANEOUS_CATEGORY = 'разное'
DEFAULT_CATEGORIES = [MISCELLANEOUS_CATEGORY]
