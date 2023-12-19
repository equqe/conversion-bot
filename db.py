import sqlite3

db = sqlite3.connect('convbot.db', check_same_thread=False)
cursor = db.cursor()


async def db_start():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY, 
        language_code TEXT
    )""")
    db.commit()


async def create_profile(user_id, language_code):
    profile = cursor.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not profile:
        cursor.execute("INSERT INTO users VALUES(?, ?)", (user_id, language_code))
        db.commit()


async def edit_locale(user_id, language_code):
    cursor.execute(f'UPDATE users SET language_code = ? WHERE user_id = ?', (language_code, user_id))
    db.commit()


async def check_locale(user_id):
    current_locale = cursor.execute("SELECT language_code FROM users WHERE user_id == '{key}'".format
                                    (key=user_id)).fetchone()
    current_locale = ''.join(current_locale)
    print(current_locale)
    if current_locale != 'ru':
        cursor.execute("UPDATE users SET language_code = 'en' WHERE user_id == '{key}'".format(key=user_id))
    return current_locale
