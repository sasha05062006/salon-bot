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
                master TEXT,
                date TEXT,
                time TEXT,
                duration INTEGER DEFAULT 30,
                name TEXT,
                phone TEXT,
                lang TEXT DEFAULT 'ru',
                status TEXT DEFAULT 'new',
                created_at TEXT
            )
        """)
        await db.commit()


async def add_booking(user_id: int, username: str, service: str, master: str, date: str, time: str, name: str, phone: str, lang: str = "ru", duration: int = 30):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO bookings (user_id, username, service, master, date, time, duration, name, phone, lang, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, username, service, master, date, time, duration, name, phone, lang, datetime.now().isoformat())
        )
        await db.commit()


async def update_booking_status(booking_id: int, status: str) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
        await db.commit()
        return cursor.rowcount > 0


async def get_booking(booking_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def get_all_bookings():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM bookings ORDER BY id DESC")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def is_slot_available(date: str, start_time: str, duration_minutes: int, master: str) -> bool:
    start = datetime.strptime(start_time, "%H:%M")
    end = start + __import__("datetime").timedelta(minutes=duration_minutes)
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT time, COALESCE(duration, 30) FROM bookings WHERE date = ? AND master = ? AND status != 'cancelled'",
            (date, master)
        )
        rows = await cursor.fetchall()
        for existing_time, existing_duration in rows:
            existing_start = datetime.strptime(existing_time, "%H:%M")
            existing_end = existing_start + __import__("datetime").timedelta(minutes=existing_duration or 30)
            if start < existing_end and existing_start < end:
                return False
    return True


async def is_slot_booked(date: str, time: str, master: str) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT 1 FROM bookings WHERE date = ? AND time = ? AND master = ? AND status != 'cancelled' LIMIT 1",
            (date, time, master)
        )
        return await cursor.fetchone() is not None
