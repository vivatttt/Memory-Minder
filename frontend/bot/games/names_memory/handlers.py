from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from frontend.bot.games.names_memory import NamesMemoryGame
from frontend.bot.games.names_memory.keyboards import Keyboard
from frontend.bot.games.names_memory.middleware import Middleware
from frontend.bot.games.names_memory.states import NamesMemoryForm

router = Router()
router.message.middleware(Middleware())
kb = Keyboard()

@router.message(NamesMemoryForm.game_started)
async def game_started(message: Message, state: FSMContext):
    await message.answer(
        f"Вы попали в игру *{NamesMemoryGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear() # тут ваши изменения состояния
