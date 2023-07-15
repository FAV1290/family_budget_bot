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
    'add' : '• /add - добавить расход',
    'new_category' : '• /new_category - добавить категорию расходов',
    'categories' : '• /categories - посмотреть список категорий',
    'expenses' : '• /expenses - посмотреть список расходов',
    'help' : '• /help - посмотреть список доступных команд',
    'start' : '• /start - руководство по первоначальной настройке',
    'utc_offset' : '• /utc_offset - установить часовой пояс',
}
MISCELLANEOUS_CATEGORY_NAME = 'разное'
DEFAULT_CATEGORIES_NAMES = [MISCELLANEOUS_CATEGORY_NAME]
QUICK_START = True
START_SPEECH = ''.join(
        [
        'Привет! Я помогаю вести семейный бюджет. Чтобы использовать мой функционал было удобнее, ',
        'предлагаю провести первоначальную настройку:\n',
        '\n•Для начала установите свой часовой пояс командой /utc_offset',
        '\n•Затем с помощью команды /new_category добавьте категории расходов',
        '\n•Теперь вы можете добавлять расходы командой /add',
        '\n•Чтобы посмотреть список категорий расходов, введите /categories',
        '\n•Чтобы ознакомиться со списком расходов, напишите /expenses',
        '\n\nЖелаю приятного использования! ',
        'Если вдруг вы хотите использовать меня совместно с кем-то, '
        'то добавьте в соответствующий чат и дайте права администратора'
    ]
)
