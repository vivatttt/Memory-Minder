import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from frontend.bot.games.words import WordsGame
from frontend.bot.games.words.keyboards import Keyboard, StartGameButtons, ReturnGameButtons
from frontend.bot.games.words.middleware import Middleware
from frontend.bot.games.words.states import WordsForm
from frontend.bot.games.words.utils import with_game_slug
from frontend.bot.games.words.gameplay import GameLogic

router = Router()
router.message.middleware(Middleware())
kb = Keyboard()
game_logic = GameLogic()


@router.message(WordsForm.game_started)
async def game_started(message: Message, state: FSMContext):
    await message.answer(
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
async def take_guess(message: Message, state: FSMContext):
    await state.update_data(user_words=message.text)
    data = await state.get_data()

    right_answers, words_amount = game_logic.calculate_results(data["response_words"], data["user_words"])
    result_text = (
        f"Правильно: {right_answers} из {words_amount} слов\n"
        f"{'Вы Выиграли!' if right_answers > words_amount / 2 else 'Вы Проиграли'}"
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


@router.callback_query(lambda callback: callback.data == with_game_slug(StartGameButtons.statistics.name))
async def view_statistics(callback: CallbackQuery):
    await callback.message.edit_text(
        "Здесь будет *статистика*",
        parse_mode="MarkdownV2",
        reply_markup=kb.return_back(),
    )
