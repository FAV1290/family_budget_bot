import os
import dotenv


dotenv.load_dotenv(dotenv.find_dotenv())


API_TOKEN = os.environ.get("FFBOT_API_TOKEN", "")
DB_HOST = os.environ.get("FFBOT_DB_HOST", "")
LOGGING_FORMAT = "%(name)s - %(levelname)s - %(message)s"
BOT_LOG_FILEPATH = "bot.log"
START_MESSAGE = "".join(
    [
        "Привет!",
        "\nЯ помогаю вести семейный бюджет.",
        "\nПредлагаю начать с настроек:",
        "\n\n• /utc_offset — задай часовой пояс",
        "\n• /new_category — добавь категории расходов",
        "\n• /add — добавляй расходы",
        "\n• /categories — список категорий",
        "\n• /expenses — список расходов",
        "\n\nЧтобы использовать меня совместно с кем-то, ",
        "добавь в чат и дай права админа.",
        "\n\nПриятного использования! ",
    ]
)
COMMANDS = {
    "categories": "список категорий расходов",
    "incomes": "список приходов",
    "expenses": "посмотреть список расходов",

    "new_category": "добавить категорию расходов",
    "limit_category": "изменить лимит категории",

    "add": "добавить расход",
    "rm_last_expense": "удалить последний расход",

    "boost_income": "добавить приход",

    "help": "список доступных команд",
    "utc_offset": "установить часовой пояс",
    "start": "руководство по первоначальной настройке",
}
