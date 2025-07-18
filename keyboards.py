from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer"
        ))
    builder.adjust(1)
    return builder.as_markup()

def create_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Начать игру"))
    return builder.as_markup(resize_keyboard=True)