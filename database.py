import aiosqlite
from datetime import datetime

DB_NAME = "bookings.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                service TEXT,
                date TEXT,
                time TEXT,
                name TEXT,
                phone TEXT,
                lang TEXT DEFAULT 'ru',
                status TEXT DEFAULT 'new',
                created_at TEXT
            )
        """)
        await db.commit()


async def add_booking(user_id: int, username: str, service: str, date: str, time: str, name: str, phone: str, lang: str = "ru"):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO bookings (user_id, username, service, date, time, name, phone, lang, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, username, service, date, time, name, phone, lang, datetime.now().isoformat())
        )
        await db.commit()


async def get_all_bookings():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM bookings ORDER BY id DESC")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
