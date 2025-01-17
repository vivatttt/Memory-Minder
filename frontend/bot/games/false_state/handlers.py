import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.services.games.false_state.stats import get_game_stats, write_stats
from frontend.bot.base.texts import escape_markdown_v2
from frontend.bot.games.false_state import FalseStateGame
from frontend.bot.games.false_state.data import get_new_user_game
from frontend.bot.games.false_state.games import get_games, get_user_game
from frontend.bot.games.false_state.keyboards import (
    GameEndButtons,
    GameMenuButtons,
    Keyboard,
    ReturnButtons,
    StatementsButtons,
)
from frontend.bot.games.false_state.middleware import Middleware
from frontend.bot.main_menu.keyboards import game_started_prefix
from frontend.bot.games.false_state.utils import with_game_slug, get_explain_user_wrong

router = Router()
router.message.middleware(Middleware())
kb = Keyboard()

games = get_games()


@router.callback_query(lambda callback: callback.data == FalseStateGame.add_prefix(game_started_prefix))
async def game_started(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        f"Вы попали в игру *{FalseStateGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.game_menu(),
    )
    await state.clear()


@router.callback_query(lambda callback: callback.data == with_game_slug(GameEndButtons.retry.name))
async def retry_game(callback: CallbackQuery):
    await callback.message.edit_text(
        f"Вы попали в игру *{FalseStateGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.game_menu(),
    )


@router.callback_query(lambda callback: callback.data == with_game_slug(ReturnButtons.back.name))
async def return_back(callback: CallbackQuery):
    await callback.message.edit_text(
        f"Вы попали в игру *{FalseStateGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.game_menu(),
    )


@router.callback_query(lambda callback: callback.data == with_game_slug(GameMenuButtons.play.name))
async def handle_play(callback: CallbackQuery):
    await callback.message.edit_text(
        f"""_Придумываем новый текст{escape_markdown_v2("...")}_
У вас будет *3 минуты* чтобы прочитать его и запомнить ключевые моменты""",
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
    await asyncio.sleep(180)
    await callback.message.edit_text(
        f"Выберите все утверждения, которые считаете *неверными*\n{escape_markdown_v2(user_game.data.statements.text)}",
        parse_mode="MarkdownV2",
        reply_markup=kb.statements(user_game),
    )


@router.callback_query(lambda callback: callback.data == with_game_slug(GameMenuButtons.stats.name))
async def handle_view_stats(callback: CallbackQuery, session: AsyncSession):
    games_won, games_lost = await get_game_stats(
        session=session,
        user_id=callback.from_user.id
    )
    await callback.message.edit_text(
        f"_Ваша статистика игр_\n*Выиграно* {games_won}\n*Проиграно* {games_lost}",
        parse_mode="MarkdownV2",
        reply_markup=kb.return_back(),
    )


@router.callback_query(lambda callback: callback.data == with_game_slug(GameMenuButtons.rules.name))
async def handle_view_rules(callback: CallbackQuery):
    await callback.message.edit_text(
        """
*Правила игры*

Мы придумаем текст и дадим вам _3 минуты_, чтобы прочитать его и запомнить все ключевые моменты
Потом мы покажем некоторые утверждения о тексте, часть из которых будет содержать ложную информацию

Ваша задача найти и отметить все неправильные утверждения
        """,
        parse_mode="MarkdownV2",
        reply_markup=kb.return_back(),
    )


@router.callback_query(
    lambda callback:
    callback.data.startswith(
        with_game_slug(
            StatementsButtons.change_statement.name
        )
    )
)
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


@router.callback_query(lambda callback: callback.data == with_game_slug(StatementsButtons.send_statement.name))
async def handle_check_statements(callback: CallbackQuery, session: AsyncSession):
    user_game = get_user_game(callback.from_user.id)
    user_won = user_game.data.statements.wrong_inds == user_game.choosen_wrong_inds
    text = "Ура! Все верно!" if user_won else "Не совсем.."
    explain_user_wrong_text = get_explain_user_wrong(user_game.data.statements, user_game.choosen_wrong_inds) if not user_won else ""
    await write_stats(
        session=session,
        user_id=callback.from_user.id,
        won=user_won
    )
    await callback.message.edit_text(
        escape_markdown_v2(text) + explain_user_wrong_text,
        parse_mode="MarkdownV2",
        reply_markup=kb.end(),
    )
