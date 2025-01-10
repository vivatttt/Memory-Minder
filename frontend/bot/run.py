import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from frontend.bot.games.false_state.handlers import router as false_state_router
from frontend.bot.games.n_back.handlers import router as n_back_router
from frontend.bot.games.names_memory.handlers import router as names_memory_router
from frontend.bot.games.simon.handlers import router as simon_router
from frontend.bot.games.words.handlers import router as words_router
from frontend.bot.main_menu.handlers import router as main_menu_router
from frontend.bot.main_menu.middleware import AuthorizationMiddleware, DBSessionMiddleware
from shared.config import get_settings
from shared.logs import setup_logging

bot = Bot(token=get_settings().BOT_API_TOKEN)
dp = Dispatcher()

async def set_base_commands():
    commands = [
        BotCommand(command='start', description='В начало'),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def main():

    dp.startup.register(set_base_commands)

    dp.update.outer_middleware(DBSessionMiddleware())
    dp.update.middleware(AuthorizationMiddleware())

    dp.include_routers(
        false_state_router,
        n_back_router,
        names_memory_router,
        simon_router,
        words_router,
        main_menu_router
    )

    setup_logging()

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    except Exception:
        logging.exception("An error occurred while running the bot")


if __name__ == "__main__":
    asyncio.run(main())
