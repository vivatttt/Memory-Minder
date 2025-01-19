import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from frontend.bot.games.words import WordsGame
from frontend.bot.games.words.keyboards import Keyboard, StartGameButtons, ReturnGameButtons
from frontend.bot.games.words.middleware import Middleware
from frontend.bot.games.words.states import WordsForm
from frontend.bot.games.words.utils import with_game_slug
from frontend.bot.games.words.gameplay import GameLogic
from frontend.bot.main_menu.keyboards import game_started_prefix
from backend.app.services.games.words.charts import add_scores_words, scores_words, date_words

router = Router()
router.message.middleware(Middleware())
kb = Keyboard()
game_logic = GameLogic()


@router.callback_query(lambda callback: callback.data == WordsGame.add_prefix(game_started_prefix))
async def game_started(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        f"Вы попали в игру *{WordsGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.start_menu(),
    )
    await state.clear()


@router.callback_query(lambda callback: callback.data == with_game_slug(ReturnGameButtons.exit.name))
async def return_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Вы попали в игру *{WordsGame.name}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.start_menu(),
    )
    await state.clear()


@router.callback_query(lambda callback: callback.data == with_game_slug(StartGameButtons.play.name))
async def play_game(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WordsForm.theme)
    await callback.message.answer("Введите тематику слов",
                                  parse_mode="MarkdownV2",
                                  reply_markup=None,
                                  input_field_placeholder="Введите тему игры")


@router.message(WordsForm.theme)
async def choose_theme(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    seconds_to_remember = 10

    await message.answer("Сейчас перед вами появятся 20 слов. У вас будет 10 секунд чтобы запомнить их")

    data = await state.get_data()
    response_words = game_logic.return_words(data['theme'])
    await state.update_data(response_words=response_words)

    word_message = await message.answer(response_words)
    await asyncio.sleep(seconds_to_remember)

    await word_message.edit_text(
        "Введите через пробел все слова, которые успели запомнить",
    )

    await state.set_state(WordsForm.words)


@router.message(WordsForm.words)
async def take_guess(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(user_words=message.text)
    data = await state.get_data()

    right_answers, words_amount = game_logic.calculate_results(data["response_words"], data["user_words"])
    result_text = (
        f"Правильно: {right_answers} из {words_amount} слов\n"
        f"{'Вы Выиграли!' if right_answers > words_amount / 2 else 'Вы Проиграли'}"
    )

    await add_scores_words(
        session=session,
        user_id=message.from_user.id,
        correct_answers=right_answers,
        all_answers=words_amount
    )

    await message.answer(result_text, reply_markup=kb.end())
    await state.clear()


@router.callback_query(lambda callback: callback.data == with_game_slug(StartGameButtons.description.name))
async def game_description(callback: CallbackQuery):
    await callback.message.edit_text(
        "*Правила игры*\n"
        "Вы получите список случайно сгенерированных слов, который вы должны запомнить\\."
        "Через 10 секунд он исчезнет, а вы введете все запомнившиеся слова\\.\n"
        "_Победа_ \\- 10 слов\\. Иначе \\- _Поражение_",
        parse_mode="MarkdownV2",
        reply_markup=kb.return_back(),
    )


@router.callback_query(lambda callback: callback.data == with_game_slug(StartGameButtons.stats.name))
async def stats_game(callback: CallbackQuery, session: AsyncSession):

    chart_buf = await scores_words(session=session, user_id=callback.from_user.id)
    photo = FSInputFile(chart_buf)
    await callback.message.answer_photo(photo=photo, caption="Анализ успеха")


    chart_buf = await date_words(session=session, user_id=callback.from_user.id)
    photo = FSInputFile(chart_buf)
    await callback.message.answer_photo(photo=photo, caption="Анализ дат")

    await callback.message.answer(
        "_СТАТИСТИКА_",
        parse_mode="MarkdownV2",
        reply_markup=kb.return_back(),
    )
