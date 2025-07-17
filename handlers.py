from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from config import API_TOKEN
from database import get_quiz_index, update_quiz_index
from keyboards import generate_options_keyboard, create_main_menu
from quiz_data import quiz_data

router = Router()

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer("Верно!")
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Квиз завершён.")

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Квиз завершён.")

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в квиз!", reply_markup=create_main_menu())

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    options = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(options, options[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)