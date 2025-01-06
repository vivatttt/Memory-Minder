from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from frontend.bot.main_menu.keyboards import Keyboard, MainMenuButtons
from frontend.bot.main_menu.states import MainMenuForm
from frontend.bot.games import GamesFactory

router = Router()
kb = Keyboard()
games_config = GamesFactory()

@router.message(Command("start"))
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать в *MemoryMinder*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.main_menu()
    )
    await state.set_state(MainMenuForm.started)

    
@router.message(F.text == MainMenuButtons.view_statistics.value)
async def view_statistics(message: Message, state: FSMContext):
    if await state.get_state() != MainMenuForm.started:
        return
    await message.answer(
        "Тут скоро будет статистика ваших игр",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MainMenuForm.view_statistics)

@router.message(F.text == MainMenuButtons.select_game.value)
async def select_game(message: Message, state: FSMContext):
    if await state.get_state() != MainMenuForm.started:
        return
    await message.answer(
        "Выберите игру",
        reply_markup=kb.game_selection()
    )
    await state.set_state(MainMenuForm.select_game)

@router.message(F.text == MainMenuButtons.about.value)
async def about(message: Message, state: FSMContext):
    if await state.get_state() != MainMenuForm.started:
        return
    await message.answer(
        "Тут скоро будет подробная информация о возможностях бота",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MainMenuForm.about)


@router.callback_query(lambda callback: callback.data in games_config.slugs)
async def handle_game_selection(callback: CallbackQuery, state: FSMContext):
    """Классы для каждой из игр имеют общее состояние входа - game_started"""
    game = games_config.get(callback.data)
    await state.set_state(game.form.game_started)
    await callback.message.answer(
        f"Выбрана игра {game.name}\n_Нажмите чтобы начать_",
        parse_mode="MarkdownV2",
        reply_markup=kb.play(),
    )