import asyncio
import aiosqlite


async def async_fetch_users():
    """ fetch all users """
    cur = await cursor.execute("SELECT * FROM users")
    result = await cur.fetchall()
    return result


async def async_fetch_older_users():
    """ fetch all users older than 40 """
    cur = await cursor.execute("SELECT * FROM users WHERE age > 40")
    result = await cur.fetchall()
    return result

async def fetch_concurrently():
    global cursor
    async with aiosqlite.connect("users.db") as db:
        cursor = db
        await asyncio.gather(async_fetch_users(), async_fetch_older_users())

asyncio.run(fetch_concurrently())