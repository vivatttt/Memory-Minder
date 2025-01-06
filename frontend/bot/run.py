import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from shared.config import get_settings
from shared.logs import setup_logging

from frontend.bot.games.false_state.handlers import router as FalseStateRouter
from frontend.bot.games.n_back.handlers import router as NBackRouter
from frontend.bot.games.simon.handlers import router as SimonRouter
from frontend.bot.games.words.handlers import router as WordsRouter
from frontend.bot.games.names_memory.handlers import router as NamesMemoryRouter
from frontend.bot.main_menu.handlers import router as MainMenuRouter

bot = Bot(token=get_settings().BOT_API_TOKEN)
dp = Dispatcher()

async def set_base_commands():
    commands = [
        BotCommand(command='start', description='В начало'),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def main():

    dp.startup.register(set_base_commands)

    dp.include_routers(
        FalseStateRouter,
        NBackRouter,
        SimonRouter,
        WordsRouter,
        NamesMemoryRouter,
        MainMenuRouter
    )
    
    setup_logging()
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await dp.start_polling(bot)
    except Exception:
        logging.exception("An error occurred while running the bot")


if __name__ == "__main__":
    asyncio.run(main())
