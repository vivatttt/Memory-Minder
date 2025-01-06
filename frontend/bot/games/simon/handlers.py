from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from frontend.bot.games.simon.keyboards import Keyboard
from frontend.bot.games.simon import SimonGame
from frontend.bot.games.simon.states import SimonForm
from frontend.bot.games.simon.middleware import Middleware

router = Router()
router.message.middleware(Middleware())
kb = Keyboard()

@router.message(SimonForm.game_started)
async def game_started(message: Message, state: FSMContext):
    await message.answer(
        f"Вы попали в игру *{SimonGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear() # тут ваши изменения состояния