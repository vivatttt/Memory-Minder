import asyncio
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from frontend.bot.base.texts import escape_markdown_v2
from frontend.bot.games.false_state.utils import with_game_slug
from frontend.bot.games.false_state.keyboards import Keyboard, GameMenuButtons, StatementsButtons, GameEndButtons
from frontend.bot.games.false_state import FalseStateGame
from frontend.bot.games.false_state.states import FalseStateForm
from frontend.bot.games.false_state.middleware import Middleware
from frontend.bot.games.false_state.data import get_new_user_game
from frontend.bot.games.false_state.games import get_games, get_user_game
router = Router()
router.message.middleware(Middleware())
kb = Keyboard()

games = get_games()

@router.message(FalseStateForm.game_started)
async def game_started(message: Message, state: FSMContext):
    await message.answer(
        f"Вы попали в игру *{FalseStateGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.game_menu(),
    )
    await state.clear()

@router.callback_query(lambda callback : callback.data == with_game_slug(GameEndButtons.retry.name))
async def retry_game(callback: CallbackQuery):
    await callback.message.edit_text(
        f"Вы попали в игру *{FalseStateGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.game_menu(),
    )

@router.callback_query(lambda callback : callback.data == with_game_slug(GameMenuButtons.play.name))
async def handle_play(callback: CallbackQuery):
    await callback.message.edit_text(
        f"_Придумываем новый текст{escape_markdown_v2("...")}_\nУ вас будет *3 минуты* чтобы прочитать его и запомнить ключевые моменты",
        parse_mode="MarkdownV2",
        reply_markup=None,
    )
    user_game = get_new_user_game(difficulty=3)
    games[callback.from_user.id] = user_game
    await callback.message.edit_text(
        user_game.data.text,
        # parse_mode="MarkdownV2",
        reply_markup=None,
    )
    await asyncio.sleep(5)
    await callback.message.edit_text(
        f"Выберите все утверждения, которые считаете *неверными*\n{escape_markdown_v2(user_game.data.statements.text)}",
        parse_mode="MarkdownV2",
        reply_markup=kb.statements(user_game),
    )


@router.callback_query(lambda callback : callback.data.startswith(with_game_slug(StatementsButtons.change_statement.name)))
async def handle_select_statement(callback: CallbackQuery):
    user_game = get_user_game(callback.from_user.id)
    changed_statement = int(callback.data.split(":")[1])
    
    if changed_statement not in user_game.choosen_wrong_inds:
        user_game.choosen_wrong_inds.add(changed_statement)
    else:
        user_game.choosen_wrong_inds.remove(changed_statement)

    await callback.message.edit_text(
        f"Выберите все утверждения, которые считаете *неверными*\n{escape_markdown_v2(user_game.data.statements.text)}",
        parse_mode="MarkdownV2",
        reply_markup=kb.statements(user_game),
    )
    

@router.callback_query(lambda callback : callback.data == with_game_slug(StatementsButtons.send_statement.name))
async def handle_check_statements(callback: CallbackQuery):
    user_game = get_user_game(callback.from_user.id)
    user_won = user_game.data.statements.wrong_inds == user_game.choosen_wrong_inds
    text = "Ура! Все верно!" if user_won else "Не совсем.."
    await callback.message.edit_text(
        escape_markdown_v2(text),
        parse_mode="MarkdownV2",
        reply_markup=kb.end(),
    )