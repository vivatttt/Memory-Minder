from aiogram import F, Router
from aiogram.filters import Command
from aiogram.methods import answer_callback_query
from aiogram.types import FSInputFile, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from frontend.bot.games.simon import SimonGame
from frontend.bot.games.simon.states import SimonForm
from frontend.bot.games.simon.keyboards import Keyboard
from frontend.bot.main_menu.keyboards import Keyboard as MainMenuKeyboard
from frontend.bot.games.simon.middleware import Middleware
from frontend.bot.main_menu.states import MainMenuForm
from frontend.bot.main_menu.keyboards import game_started_prefix
from backend.app.services.games.simon.charts import add_scores_simon, scores_length, date_simon

from random import choice
import asyncio

router = Router()
router.message.middleware(Middleware())
kb = Keyboard()
main_menu_kb = MainMenuKeyboard()

@router.callback_query(lambda callback: callback.data == SimonGame.add_prefix(game_started_prefix))
async def game_started(callback: CallbackQuery, state: FSMContext):
    keyboard = [
        [KeyboardButton(text="Начать игру")],
        [KeyboardButton(text="Описание игры")],
        [KeyboardButton(text="Статистика")],
        [KeyboardButton(text="Выйти из игры")]
    ]
    start_text = f"Добро пожаловать в игру *{SimonGame.name}*\\.\n" \
                 f"Пожалуйста, выберите действие во всплывающем меню\\."
    await callback.message.answer(
        text=start_text,
        parse_mode="MarkdownV2",
        reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(SimonForm.get_command)


@router.message(SimonForm.get_command)
async def get_command(message: Message, state: FSMContext, session: AsyncSession):
    if message.text == "Начать игру":
        await message.answer(text="Приготовься! Игра начинается.\n\nЗапоминай последовательность цветов.")
        await asyncio.sleep(1)
        await state.set_state(SimonForm.simon_game)
        await start_game(message, state)
    elif message.text == "Описание игры":
        description_text = f"*Саймон* \\- это игра, направленная на развитие и тренировку памяти\\." \
                           f"\n\n*Задача игры:* запомнить продемонстрированную игроку последовательность цветов\\. " \
                           f"Каждый ход на экран будет выводится картинка, цвет которой нужно будет запомнить " \
                           f"и воспроизвести, сохраняя предыдущую последовательность\\." \
                           f"\n\nНапример, на первом ходу появился *Красный*, нужно выбрать *Красный*\\. " \
                           f"На втором ходу появился *Синий*, тогда необходимо последовательно нажать: " \
                           f"*Красный* \\- *Синий* И так далее, пока не ошибёшься\\!" \
                           f"\n\nХочешь попробовать свои силы\\? Давай сыграем\\!"
        keyboard = [
            [KeyboardButton(text="Начать игру")],
            [KeyboardButton(text="Описание игры")],
            [KeyboardButton(text="Статистика")],
            [KeyboardButton(text="Выйти из игры")]
        ]
        await message.answer(
            text=description_text,
            parse_mode="MarkdownV2",
            reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
    elif message.text == "Выйти из игры":
        await message.answer(
            "Добро пожаловать в *MemoryMinder*\n_Выберите действие_",
            parse_mode="MarkdownV2",
            reply_markup=main_menu_kb.main_menu()
        )
        await state.set_state(MainMenuForm.started)
    elif message.text == "Статистика":

        chart_buf = await scores_length(session=session, user_id=message.from_user.id)
        photo = FSInputFile(chart_buf)
        await message.answer_photo(photo=photo, caption="Анализ успеха")

        chart_buf = await date_simon(session=session, user_id=message.from_user.id)
        photo = FSInputFile(chart_buf)
        await message.answer_photo(photo=photo, caption="Анализ дат")

        keyboard = [
            [KeyboardButton(text="Начать игру")],
            [KeyboardButton(text="Описание игры")],
            [KeyboardButton(text="Статистика")],
            [KeyboardButton(text="Выйти из игры")]
        ]

        await message.answer(
            "_Статистика_",
            parse_mode="MarkdownV2",
            reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
    elif message.text != "Продолжить игру":
        await message.answer("Неизвестная команда. Повтори ввод, пожалуйста.")


@router.message(SimonForm.simon_game, F.text)
async def prevent_text_input(message: Message):
    await message.answer("Пожалуйста, не пишите текст, а нажимайте на кнопки.")


@router.message(SimonForm.simon_game)
async def start_game(message, state: FSMContext):
    colours = ["🟥", "🟦", "🟩", "🟨"]
    keyboard = [
        [InlineKeyboardButton(text="Красный", callback_data="colour_red")],
        [InlineKeyboardButton(text="Синий", callback_data="colour_blue")],
        [InlineKeyboardButton(text="Зелёный", callback_data="colour_green")],
        [InlineKeyboardButton(text="Жёлтый", callback_data="colour_yellow")]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    data = await state.get_data()
    answer = data.get("answer", [])
    colour = choice(colours)
    answer.append(colour)
    await state.update_data({"result": []})

    sent_message = await message.answer(" ".join(answer))
    await state.update_data({"colour": colour, "answer": answer})
    await asyncio.sleep(1)
    await sent_message.edit_text("Повторите последовательность, нажимая на кнопки ниже:",
                                 reply_markup=reply_markup, one_time_keyboard=True)


def translate_colour(english):
    if english == "red":
        return "🟥"
    elif english == "blue":
        return "🟦"
    elif english == "green":
        return "🟩"
    elif english == "yellow":
        return "🟨"
    else:
        return ""


@router.callback_query(lambda call: call.data.startswith('colour_'))
async def handle_colour_choice(call, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    colour = data.get('colour', "")
    answer = data.get('answer', [])
    selected_colour = translate_colour(call.data.split('_')[1])
    result = data.get('result', [])
    result.append(selected_colour)
    await state.update_data({"result": result})

    mistake = False
    if len(answer) == len(result):
        for i in range(len(answer)):
            if answer[i] != result[i]:
                mistake = True
                break
        if not mistake:
            await call.answer(f"Верно!")
            await call.message.delete()
            await start_game(call.message, state=state)
        else:
            await call.answer(f"Неправильный выбор: {", ".join(result)}.\nНужно было: {", ".join(answer)}.")
            await asyncio.sleep(1)
            await call.message.delete()
            await state.clear()
            await state.set_state(SimonForm.get_command)
            keyboard = [
                [KeyboardButton(text="Начать игру")],
                [KeyboardButton(text="Описание игры")],
                [KeyboardButton(text="Статистика")],
                [KeyboardButton(text="Выйти из игры")]
            ]

            await add_scores_simon(session=session, user_id=call.from_user.id, all_length=len(answer))

            await call.message.answer(
                text=f"Не унывай\\! Ты продержался {len(answer)} раз\\(а\\)\\.\n\nХочешь попробовать ещё раз\\?",
                parse_mode="MarkdownV2",
                reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
            )
            await get_command(message=call.message.edit_text("Продолжить игру"), state=state, session=session)
    else:
        await call.answer()