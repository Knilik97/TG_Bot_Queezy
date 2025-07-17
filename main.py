import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from handlers import router
from database import init_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание экземпляра бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Зарегистрируем роутеры
dp.include_router(router)

# Основная точка входа
async def main():
    await init_db()  # Создаем базу данных
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Запустим основную программу
    except KeyboardInterrupt:
        print("\nПриложение остановлено.")