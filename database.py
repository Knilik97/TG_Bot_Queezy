import aiosqlite
import config

async def init_db():
    async with aiosqlite.connect(config.DB_NAME) as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                quiz_index INTEGER DEFAULT 0
            );
        ''')
        await conn.commit()

async def get_quiz_index(user_id):
    async with aiosqlite.connect(config.DB_NAME) as conn:
        cursor = await conn.execute('SELECT quiz_index FROM users WHERE telegram_id=?', (user_id,))
        result = await cursor.fetchone()
        if not result:
            await conn.execute('INSERT INTO users (telegram_id) VALUES (?)', (user_id,))
            await conn.commit()
            return 0
        return result[0]

async def update_quiz_index(user_id, new_index):
    async with aiosqlite.connect(config.DB_NAME) as conn:
        await conn.execute('UPDATE users SET quiz_index=? WHERE telegram_id=?', (new_index, user_id))
        await conn.commit()