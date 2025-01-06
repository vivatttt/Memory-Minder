from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from frontend.bot.games.false_state.keyboards import Keyboard
from frontend.bot.games.false_state import FalseStateGame
from frontend.bot.games.false_state.states import FalseStateForm
from frontend.bot.games.false_state.middleware import Middleware

router = Router()
router.message.middleware(Middleware())
kb = Keyboard()

@router.message(FalseStateForm.game_started)
async def game_started(message: Message, state: FSMContext):
    await message.answer(
        f"Вы попали в игру *{FalseStateGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear() # тут ваши изменения состояния