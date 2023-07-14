import os
import dotenv


dotenv.load_dotenv(dotenv.find_dotenv())


API_TOKEN = os.environ.get('API_TOKEN')
DB_LOGIN = os.environ.get('DB_LOGIN')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
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
    'add_category' : '• /add_category [Имена категорий через запятую] :\nДобавить категории расходов', 
    'categories' : '• /categories : Список категорий расходов', 
    'add' : '• /add [Сумма] [Комментарий - необязательно] :\nДобавить расход на заданную сумму',
    'expenses' : '• /expenses : Список расходных операций',
    'help' : '• /help : Перечень доступных команд',
}
MISCELLANEOUS_CATEGORY = 'разное'
DEFAULT_CATEGORIES = [MISCELLANEOUS_CATEGORY]
