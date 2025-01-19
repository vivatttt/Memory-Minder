from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.schemas.internal_objects import UserObject
from backend.app.utils.authorization import authorize_user
from frontend.bot.base.texts import escape_markdown_v2

from frontend.bot.games import GamesFactory
from frontend.bot.main_menu.keyboards import Keyboard, MainMenuButtons, ReturnHomeButtons, MainMenuButtonsAdmin
from frontend.bot.main_menu.states import AuthorizationForm, MainMenuForm
from frontend.bot.main_menu.utils import is_valid_user_name
from backend.app.services.users.admin import check_info, get_id
from shared.config import get_settings

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
        settings = get_settings()

        admin = False
        if message.from_user.id == settings.ADMIN:
            admin = True
        await authorize_user(
            session=session,
            user=UserObject(
                id=message.from_user.id,
                name=name,
                username=message.from_user.username,
                is_admin=admin
            )
        )
        if admin:
            reply_markup = kb.main_menu_admin()
        else:
            reply_markup = kb.main_menu()

        await message.answer(
            f"{escape_markdown_v2(name)}, добро пожаловать в *MemoryMinder*\n_Выберите действие_",
            parse_mode="MarkdownV2",
            reply_markup=reply_markup
        )
        await state.set_state(MainMenuForm.started)
    else:
        await message.answer(
            "Имя может содержать только буквы или тире и должно быть длиной от 2 до 20 символов",
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(Command("start"))
async def command_start(message: Message, state: FSMContext, session: AsyncSession):
    if await check_info(session=session, id=message.from_user.id):
        reply_markup = kb.main_menu_admin()
    else:
        reply_markup = kb.main_menu()

    await message.answer(
        "Добро пожаловать в *MemoryMinder*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=reply_markup
    )
    await state.set_state(MainMenuForm.started)


@router.callback_query(lambda callback : callback.data == ReturnHomeButtons.return_home.name)
async def handle_home(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if await check_info(session=session, id=callback.from_user.id):
        reply_markup = kb.main_menu_admin()
    else:
        reply_markup = kb.main_menu()

    await callback.message.answer(
        "Добро пожаловать в *MemoryMinder*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=reply_markup
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
        f"Привет! Это **Memory Minder** — бот, который поможет вам развить свою память!\n"
        f"В настоящий момент я умею играть в пять логических игр:\n\n"
        f"1. Ложные высказывания\n2. N-back математический\n3. Названия из памяти\n4. Саймон\n5. Слова\n\n"
        f"Вы сможете найти подробные правила и описание каждой игры, зайдя в нужное меню!",
        reply_markup=kb.back_home()
    )
    await state.set_state(MainMenuForm.about)

@router.callback_query(lambda callback : callback.data == MainMenuButtonsAdmin.send.name)
async def send_about(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Введите сообщение для рассылки!",
    )
    await state.set_state(MainMenuForm.send)


@router.message(MainMenuForm.send)
async def send_about(message: Message, state: FSMContext, session: AsyncSession):
    ids = await get_id(session)
    bot = message.bot

    id_break = ""

    if ids != "":
        for id in ids:
            try:
                await bot.send_message(chat_id=id, text=message.text)
            except:
                id_break = id_break + " " + str(id)

    await message.answer(
        f"_Все отправлено\\. {id_break}_",
        parse_mode="MarkdownV2",
        reply_markup=kb.main_menu_admin()
    )
    await state.set_state(MainMenuForm.started)


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
