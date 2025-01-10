from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from frontend.bot.games.n_back import NBackGame
from frontend.bot.games.n_back.keyboards import Keyboard
from frontend.bot.games.n_back.middleware import Middleware
from frontend.bot.games.n_back.states import NBackForm

router = Router()
router.message.middleware(Middleware())
kb = Keyboard()

@router.message(NBackForm.game_started)
async def game_started(message: Message, state: FSMContext):
    await message.answer(
        f"Вы попали в игру *{NBackGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear() # тут ваши изменения состояния
