from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.schemas.internal_objects import UserObject
from backend.app.utils.authorization import authorize_user
from frontend.bot.base.texts import escape_markdown_v2

from frontend.bot.games import GamesFactory
from frontend.bot.main_menu.keyboards import Keyboard, MainMenuButtons, ReturnHomeButtons
from frontend.bot.main_menu.states import AuthorizationForm, MainMenuForm
from frontend.bot.main_menu.utils import is_valid_user_name

router = Router()
kb = Keyboard()
games_config = GamesFactory()

@router.message(AuthorizationForm.waiting_for_name)
async def show_unauthorized(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, введите ваше имя",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AuthorizationForm.name_filled)

@router.message(AuthorizationForm.name_filled)
async def handle_authorization(message: Message, state: FSMContext, session: AsyncSession):
    name = message.text
    name_is_valid = is_valid_user_name(name)
    if name_is_valid:
        await authorize_user(
            session=session,
            user=UserObject(
                id=message.from_user.id,
                name=name,
                username=message.from_user.username,
                is_admin=False
            )
        )
        await message.answer(
            f"{escape_markdown_v2(name)}, добро пожаловать в *MemoryMinder*\n_Выберите действие_",
            parse_mode="MarkdownV2",
            reply_markup=kb.main_menu()
        )
        await state.set_state(MainMenuForm.started)
    else:
        await message.answer(
            "Имя может содержать только буквы или тире и должно быть длиной от 2 до 20 символов",
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(Command("start"))
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать в *MemoryMinder*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.main_menu()
    )
    await state.set_state(MainMenuForm.started)


@router.callback_query(lambda callback : callback.data == ReturnHomeButtons.return_home.name)
async def handle_home(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Добро пожаловать в *MemoryMinder*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.main_menu()
    )
    await state.set_state(MainMenuForm.started)



@router.callback_query(lambda callback : callback.data == MainMenuButtons.select_game.name)
async def handle_select_game(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() != MainMenuForm.started:
        return
    await callback.message.edit_text(
        "Выберите игру",
        reply_markup=kb.game_selection()
    )
    await state.set_state(MainMenuForm.select_game)


@router.callback_query(lambda callback : callback.data == MainMenuButtons.about.name)
async def handle_about(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() != MainMenuForm.started:
        return
    await callback.message.edit_text(
        "Тут скоро будет подробная информация о возможностях бота",
        reply_markup=kb.back_home()
    )
    await state.set_state(MainMenuForm.about)


# @router.callback_query(lambda callback: callback.data in games_config.slugs)
# async def handle_game_selection(callback: CallbackQuery, state: FSMContext):
#     """Классы для каждой из игр имеют общее состояние входа - game_started"""
#     game = games_config.get(callback.data)
#     await state.set_state(game.form.game_started)
#     await state.update_data(id=callback.from_user.id)
#     await callback.message.answer(
#         f"Выбрана игра {game.name}\n_Нажмите чтобы начать_",
#         parse_mode="MarkdownV2",
#         reply_markup=kb.play(),
#     )
