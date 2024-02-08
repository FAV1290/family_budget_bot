from typing import Any

from telegram.ext import ApplicationBuilder, BaseHandler


class FamilyFundsBot():
    def __init__(self, api_token: str) -> None:
        self.app = ApplicationBuilder().token(api_token).build()

    def add_handlers(self, handlers: list[BaseHandler[Any, Any]]) -> None:
        for handler in handlers:
            self.app.add_handler(handler)

    def run_polling(self) -> None:
        self.app.run_polling()
