from aiogram import F, Router
from aiogram import types
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputFile
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import random

from frontend.bot.games.names_memory.keyboards import Keyboard, Continue, OptionsPlay, OptionsButtons, Agree
from frontend.bot.games.names_memory.utils import with_game_slug
from frontend.bot.games.names_memory import NamesMemoryGame
from frontend.bot.games.names_memory.keyboards import Keyboard
from frontend.bot.games.names_memory.middleware import Middleware
from frontend.bot.games.names_memory.states import NamesMemoryForm
from backend.app.services.games.names_memory.get_data import get_images, change_images
from backend.app.services.games.names_memory.const import images_in_round, asking_in_round
from backend.app.services.games.names_memory.stats_scores import rounds, get_results_round
from frontend.bot.base.texts import markdown

router = Router()
router.message.middleware(Middleware())
kb = Keyboard()

@router.message(NamesMemoryForm.game_started)
async def game_started(message: Message, state: FSMContext, session: AsyncSession):

    data = await state.get_data()
    id = data.get('id')
    result = await rounds(session, id)

    if result != 0:
        welcome_text = (
            f"Мы снова увидились в игре *{NamesMemoryGame.name}*\\!\n\n⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️\n\n_Посмотрим\\, что у нас тут есть для вас_"
        )
        reply_markup = kb.options_buttons()
    else:
        welcome_text = (
            f"➿➿🔺➿➿➿➿➿➿➿➿➿➿➿\n\n‼️Приветствуем вас в игре‼️\n      *{NamesMemoryGame.name}*\\!"
            f"\n\n➿➿➿➿➿➿➿➿➿➿➿🔻➿➿\n\n🔹Вы еще не играли в нее🔹\\, "
            f"но мы уверены\\, что вам понравится\\!\n\n"
            f"Правила очень просты\\.\nСейчас вы получите 8 картинок с их названиями с интервалом в 3 секунды\\.\n"
            f"Вам необходимо запомнить как можно больше картинок и их названий за отведенное время\\."
            f" Затем вам будут предложены картинки\\, и вы должны вспомнить и написать их названия\\."
            f" Однако  вам могут попасться картинки\\, которые не были упомянуты в раунде\\, тогда напишите"
            f" НЕ БЫЛО\\.☑️\n\n➿➿➿➿➿➿♦️♦️➿➿➿➿➿➿\n\nДумаю\\, ты со всем справишься\\!🥳\n🔸Давай начинать🔸\\!"
        )
        reply_markup = kb.options_buttons_first()

    await message.answer(
        welcome_text,
        parse_mode="MarkdownV2",
        reply_markup=reply_markup
    )
    await state.clear()


@router.callback_query(lambda callback: callback.data == with_game_slug(Continue.conti.name))
async def continue_game(callback: CallbackQuery):

    ''' Думаю добаавить тут удаление сообщений раунда '''

    await callback.message.answer(
        f"_🧐А что будем делать дальше\\?🧐_",
        parse_mode="MarkdownV2",
        reply_markup=kb.options_buttons()
    )

@router.callback_query(lambda callback: callback.data == with_game_slug(OptionsButtons.stats.name))
async def stats_game(callback: CallbackQuery, session: AsyncSession):

    ''' добаавить тут stats '''

    await callback.message.answer(
        f"_СТАТИСТИКА\\!_",
        parse_mode="MarkdownV2",
        reply_markup=kb.options_buttons()
    )

@router.callback_query(lambda callback: callback.data == with_game_slug(OptionsButtons.rules.name))
async def rules_game(callback: CallbackQuery):

    ''' Расписать правила '''

    await callback.message.answer(
        f"_А что будем делать дальше\\? Правила\\!_",
        parse_mode="MarkdownV2",
        reply_markup=kb.options_buttons()
    )

@router.callback_query(lambda callback: callback.data == with_game_slug(OptionsPlay.play.name))
async def playing(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    message_ids = []

    images = await get_images(session, user_id=callback.from_user.id)
    await state.update_data(images=images)

    message = await callback.message.edit_text(
        f"_Приготовились запоминать\\!\n🤫🤫🤫🤯🤯🤯🤫🤫🤫\nСейчас все начнётся\\!_",
        parse_mode="MarkdownV2",
        reply_markup=None,
    )
    await asyncio.sleep(2)

    for i in range(images_in_round() - 2):
        id, photo_url, image_title = images[i]

        message = await callback.message.edit_text(
            f"_Картинка_ {i + 1}\n",
            parse_mode="MarkdownV2",
            reply_markup=None,
        )
        message_ids.append(message.message_id)

        try:
            message = await callback.message.answer_photo(
                photo=photo_url,
                caption=f"{image_title}\n",
            )
            message_ids.append(message.message_id)
            await asyncio.sleep(2)
            await callback.message.chat.delete_message(message.message_id)
        except:
            await callback.message.edit_text(
                f"_Извините\\, картинка не смогла загрузиться_😭\n",
                parse_mode="MarkdownV2",
                reply_markup=None,
            )
            await asyncio.sleep(2)

    message = await callback.message.edit_text(
        f"Ну что\\, теперь проверим\\?",
        parse_mode="MarkdownV2",
        reply_markup=kb.agree_button()
    )
    message_ids.append(message.message_id)

    for message_id in message_ids:
        try:
            await callback.message.delete_message(message_id)
        except Exception as e:
            pass

@router.callback_query(lambda callback: callback.data == with_game_slug(Agree.agree.name))
async def rules_game(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.set_state(NamesMemoryForm.waiting_for_answer.state)
    await state.update_data(question_index=0, answers=[])

    data = await state.get_data()
    images = data.get('images', [])

    images = await change_images(images)

    await state.update_data(images=images, id=callback.from_user.id, session=session)
    id, photo_url, image_title = images[0]

    await callback.message.edit_text(
        f"_Картинка_ {1}",
        parse_mode="MarkdownV2",
        reply_markup=None,
    )
    try:
        await callback.message.answer_photo(
            photo=photo_url,
        )
    except:
        await callback.message.edit_text(
            f"_Извините\\, картинка не смогла загрузиться_😭\n",
            parse_mode="MarkdownV2",
            reply_markup=None,
        )

    await callback.message.answer("Введите ваш ответ:")

@router.message(NamesMemoryForm.waiting_for_answer)
async def handle_user_answer(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    answers = data.get('answers', [])
    question_index = data.get('question_index', 0)
    images = data.get('images')
    id = data.get('id')

    answers.append(message.text)
    question_index += 1

    if question_index < asking_in_round():
        await state.update_data(answers=answers, question_index=question_index)
        await message.answer(f"Ваш ответ: {message.text}\n")

        id, photo_url, image_title = images[question_index]

        await message.answer(
            f"_Картинка_ {question_index + 1}\n\nВведите ваш ответ\\:",
            parse_mode="MarkdownV2")
        try:
            message = await message.answer_photo(
                photo=photo_url,
            )
        except:
            await message.edit_text(
                f"_Извините\\, картинка не смогла загрузиться_😭\n",
                parse_mode="MarkdownV2",
                reply_markup=None,
            )
    else:
        results, arr = await get_results_round(session, id, images, answers)
        await message.answer(
            f"🔥Раунд завершен\\!🔥\nВы ответили правильно {results} из {asking_in_round()}\\.\n\n"
            f"Правильные ответы \\:\n{markdown(arr)}",
            parse_mode="MarkdownV2",
            reply_markup=kb.continue_button()
        )
        await state.clear()
