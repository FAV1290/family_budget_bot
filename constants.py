import os
import dotenv


dotenv.load_dotenv(dotenv.find_dotenv())


API_TOKEN = os.environ.get('API_TOKEN')
DB_HOST = os.environ.get('DB_HOST')
REGIONS = [
    ('африка', 'africa'),
    ('европа', 'europe'),
    ('азия', 'asia'),
    ('северная америка', 'north_america'),
    ('южная америка', 'south_america'),
    ('австралия и океания', 'africa'),
    ('антарктида', 'antarctica'),
]
UTC_OFFSETS_DIVISION = {
    'africa' : [-1, 0, 1, 2, 3, 4],
    'europe' : [0, 1, 2, 3, 4],
    'asia' : [4, 5, 6, 7, 8, 9, 10, 11, 12],
    'north_america' : [-11, -10, -9, -8, -7, -6, -5, -4],
    'south america' : [-5, -4, -3, -2],
    'australia_oceania' : [6, 7, 8, 9, 10, 11, 12],
    'antarctica' : [-6, -3, 0, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13],
}
COMMANDS = {
    'new_category' : '• /new_category - добавить категорию расходов', 
    'categories' : '• /categories - список категорий расходов', 
    'add' : '• /add - добавить расходную операцию',
    'expenses' : '• /expenses -  список расходных операций',
    'help' : '• /help - перечень доступных команд',
    'start' : '• /start - запустить первоначальную настройку', 
}
MISCELLANEOUS_CATEGORY_NAME = 'разное'
DEFAULT_CATEGORIES_NAMES = [MISCELLANEOUS_CATEGORY_NAME]
