from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


class BaseKeyboard:
    def create_reply_keyboard(
        self,
        buttons,
        row_width=3,
        resize_keyboard=True,
        one_time_keyboard=False
    ):
        if not buttons:
            raise ValueError("Список кнопок не может быть пустым")

        keyboard = [
            [KeyboardButton(text=button) for button in buttons[i:i + row_width]]
            for i in range(0, len(buttons), row_width)
        ]

        markup = ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard
        )
        return markup

    def create_inline_keyboard(
        self,
        buttons,
        row_width=3
    ):
        if not buttons:
            raise ValueError("Список кнопок не может быть пустым")

        keyboard = [
            [InlineKeyboardButton(text=text, callback_data=data) for text, data in buttons[i:i + row_width]]
            for i in range(0, len(buttons), row_width)
        ]

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup

    def statistic_keyboard(
        self,
        buttons,
    ):
        if not buttons:
            raise ValueError("Список кнопок не может быть пустым")

        keyboard = []

        for button in buttons:
            if isinstance(button, list):
                keyboard.append([InlineKeyboardButton(text=btn, callback_data=btn) for btn in button])
            else:
                keyboard.append([InlineKeyboardButton(text=button, callback_data=button)])

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup

