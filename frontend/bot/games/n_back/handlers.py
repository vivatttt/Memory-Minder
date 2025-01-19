import asyncio
from asyncio import Event
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import json
import os

from frontend.bot.main_menu.keyboards import game_started_prefix
from frontend.bot.games.n_back.utils import with_game_slug
from frontend.bot.games.n_back.keyboards import Keyboard, GameEndButtons, GameMenuButtons, NumbersButtons
from frontend.bot.games.n_back import NBackGame
from frontend.bot.games.n_back.states import NBackForm, ChangeNState
from frontend.bot.games.n_back.middleware import Middleware
from backend.app.services.games.n_back.charts import scores_n_back, add_scores_n_back, date_n_back, answers_n_back

def output_results(user):
    res = "Ответы:  Ваш  Верный"
    for choice, right in zip(user.choice_values, user.right_values):
        if choice == right:
            res += "\n    ✅{:>12} {:>11}".format(choice, right)
        else:
            res += "\n    ❌{:>12} {:>11}".format(choice, right)
    return res

def generate_examples(user, n=1):
    import random
    examples = []
    for i in range(n):
        sign = random.choice(["+", "-"])
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        if n != 1:
            examples.append(f"{i+1}) {a} {sign} {b}")
        else:
            examples.append(f"{a} {sign} {b}")
        if sign == "+": 
            user.right_values.append(str(a+b)[-1]) 
        else:
            user.right_values.append(str(a-b)[-1]) 
    return "\n".join(examples)


class UserSession:
    def __init__(self):
        self.choice_event = asyncio.Event()
        self.choice_values = []
        self.right_values = []

user_sessions = {}  # Хранилище сессий пользователей

router = Router()
router.message.middleware(Middleware())
kb = Keyboard()
    
@router.callback_query(lambda callback : callback.data == NBackGame.add_prefix(game_started_prefix))
async def game_started(callback: CallbackQuery, state: FSMContext):
    user_id = str(callback.from_user.id)
    user_data = load_user_data()
    first_user = False
    if user_id not in user_data:
        user_data[user_id] = {"n": 1}
        first_user = True
    n = user_data[user_id].get("n", 1)
    save_user_data(user_data)

    if first_user:
        await callback.message.answer(
            f"Приветствую новенького любителя прокачать память🧐 Вы попали в игру *{NBackGame.name}*\\." +
            f"\nВаше *N \\= {n}*\\. Если вы не понимаете что это\\, то советую для начала нажать на кнопку *Правила*\\." +
            f"\n_Выберите действие_",
            parse_mode="MarkdownV2",
            reply_markup=kb.game_menu(),
        )
    else:
        await callback.message.answer(
            f"Вы попали в игру *{NBackGame.name}*\\. Ваше *N \\= {n}*\n_Выберите действие_",
            parse_mode="MarkdownV2",
            reply_markup=kb.game_menu(),
        )
    await state.clear()

@router.callback_query(lambda callback : callback.data == with_game_slug(GameEndButtons.retry.name))
async def retry_game(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    user_data = load_user_data()
    n = user_data[user_id].get("n", 1)
    await callback.message.edit_text(
        f"Вы попали в игру *{NBackGame.name}*\\. Ваше *N \\= {n}*\n_Выберите действие_",
        parse_mode="MarkdownV2",
        reply_markup=kb.game_menu(),
    )

@router.callback_query(lambda callback : callback.data == with_game_slug(GameEndButtons.results.name))
async def results_game(callback: CallbackQuery):
    await callback.message.edit_text(
        output_results(user_sessions[callback.from_user.id]),
        parse_mode="MarkdownV2",
        reply_markup=kb.game_menu(),
    )

# Указываем путь к JSON-файлу
DATA_FILE = "user_data.json"
project_root = os.path.dirname(os.path.abspath(__file__))
path_to_file = os.path.join(project_root, DATA_FILE)

def load_user_data():
    """Загружает данные пользователей из JSON-файла."""
    if not os.path.exists(path_to_file):
        return {}
    with open(path_to_file, "r", encoding="utf-8") as file:
        return json.load(file)

def save_user_data(data):
    """Сохраняет данные пользователей в JSON-файле."""
    with open(path_to_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

@router.callback_query(lambda callback: callback.data == with_game_slug(GameMenuButtons.N.name))
async def change_n(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"Введите новое значение (от 1 до 100):")
    await state.set_state(ChangeNState.waiting_for_n)  # Устанавливаем состояние

@router.message(ChangeNState.waiting_for_n)
async def input_n(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_data = load_user_data()

    try:
        new_n = int(message.text)
        if not 1 <= new_n <= 100:
            raise ValueError

        # Обновляем значение n
        if user_id not in user_data:
            user_data[user_id] = {}
        user_data[user_id]["n"] = new_n
        save_user_data(user_data)  # Сохраняем изменения

        await message.answer(
            f"Ваше значение N обновлено на {new_n}.",
            reply_markup=kb.game_menu()
            )
        await state.clear()  # Завершаем состояние

    except ValueError:
        await message.answer("Пожалуйста, введите корректное число от 1 до 100.")


@router.callback_query(lambda callback : callback.data == with_game_slug(GameMenuButtons.rules.name))
async def game_rule(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    user_data = load_user_data()
    n = user_data[user_id].get("n", 1)

    await callback.message.edit_text(
        f"В данной игре изначально вам необходимо решить N примеров за 3\\*N секунд *\\(текущее N \\= {n}\\)* " +
        f"и запомнить последние цифры в каждом ответе\\. После этого вам придет сообщение с новым примером и 10 цифрами в качестве варианта ответа\\."+
        f" Вам надо будет также решить этот пример\\, запомнить последнюю цифру и выбрать последнюю цифру ответа на *самый первый* решенный" +
        f" пример в этой игре\\. Далее ситуация будет повторяться, только ответ нужно будет дать уже на второй решенный вами пример и так далее до конца игры\\." +
        f" Всего N\\+10 вопросов\\." +
        f"\n\nЕсли в правилах что\\-то неясно\\, то скорее начинайте игру\\, так станет сразу понятнее\\!",
        parse_mode="MarkdownV2",
        reply_markup=kb.game_menu_after_rule(),
    )

@router.callback_query(lambda callback: callback.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery):
    user_id = callback.from_user.id
    session = user_sessions[user_id]
    session.choice_values.append(callback.data.split("_")[1])
    session.choice_event.set()
    session.choice_event.clear()
    # await callback.answer(f"Вы выбрали {session.choice_values[-1]}")

@router.callback_query(lambda callback: callback.data == with_game_slug(GameMenuButtons.play.name))
async def game_start(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    user_data = load_user_data()
    n = user_data[str(user_id)].get("n", 1)
    k = 10
    user_sessions[user_id] = UserSession()
    sessions = user_sessions[user_id]

    await callback.message.edit_text(f"Запомните последние цифры в ответах этих примеров\n{generate_examples(sessions, n)}")
    await asyncio.sleep(3 * n + 2)

    for i in range(k):
        msg = await callback.message.edit_text(
            f"Пример: {generate_examples(sessions)}" +
            f"\n\nВыберите последнюю цифру ответа на {i+1} пример",
            reply_markup=NumbersButtons.key
        )
        
        await sessions.choice_event.wait()
    
    for i in range(n):
        msg = await callback.message.edit_text(
            f"\n\nВыберите последнюю цифру ответа на {i+k+1} пример",
            reply_markup=NumbersButtons.key
        )
        
        await sessions.choice_event.wait()

    
    if sessions.choice_values == sessions.right_values:
        await add_scores_n_back(
            session=session,
            user_id=callback.from_user.id,
            correct_answers=len(sessions.right_values),
            wrong_answers=0,
            percentage=100,
            n_level=n
        )

        await callback.message.edit_text(
            f"Прекрасный результат🎉🎉🎉 \n100% правильных ответов",
            reply_markup=kb.end_game_menu()
        )
    else:
        count_right_answer = sum(1 for choice, right in zip(sessions.choice_values, sessions.right_values) if choice == right)

        await add_scores_n_back(
            session=session,
            user_id=callback.from_user.id,
            correct_answers=count_right_answer,
            wrong_answers=len(sessions.right_values) - count_right_answer,
            percentage=int(count_right_answer/len(sessions.choice_values)*100+0.5),
            n_level=n
        )


        await callback.message.edit_text(
            f"Неидеальный результат, есть к чему стремиться!" +
            f"\n{int(count_right_answer/len(sessions.choice_values)*100+0.5)}% правильних ответов. Не расстраивайтесь🤗",
            reply_markup=kb.end_game_menu()
        )

@router.callback_query(lambda callback: callback.data == with_game_slug(GameMenuButtons.stats.name))
async def stats_game(callback: CallbackQuery, session: AsyncSession):

    chart_buf = await scores_n_back(session=session, user_id=callback.from_user.id)
    photo = FSInputFile(chart_buf)
    await callback.message.answer_photo(photo=photo, caption="Анализ успеха")


    chart_buf = await date_n_back(session=session, user_id=callback.from_user.id)
    photo = FSInputFile(chart_buf)
    await callback.message.answer_photo(photo=photo, caption="Анализ дат")

    chart_buf = await answers_n_back(session=session, user_id=callback.from_user.id)
    photo = FSInputFile(chart_buf)
    await callback.message.answer_photo(photo=photo, caption="Анализ ответов")


    await callback.message.answer(
        f"_СТАТИСТИКА_",
        reply_markup=kb.game_menu_after_rule()
    )