from pyrogram import Client, filters
import datetime
import time
import asyncio
from database.users_chats_db import db  # Ensure this module provides `get_all_users` and `total_users_count`
from info import ADMINS  # Ensure this module provides the list of admin IDs
from utils import broadcast_messages  # Ensure this module provides the `broadcast_messages` function

app = Client("Hsjsbwbot")

@app.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your message to this bot\'s users...'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed = 0
    success = 0

    async for user in users:
    user_id = int(user['id'])
    try:
        pti, sh = await broadcast_messages(user_id, b_msg)
        if pti:
            success += 1
        else:
            if sh == "Blocked":
                blocked += 1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
    except Exception as e:
        failed += 1
        print(f"Error broadcasting to {user_id}: {e}")
    done += 1
    await asyncio.sleep(2)
    if not done % 20:
        await sts.edit(
            f"Broadcast in progress:\n\nTotal users: {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}\nFailed: {failed}"
           )
    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.edit(
        f"Broadcast successfully completed:\nBroadcast completed in {time_taken}.\n\nTotal users: {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}\nFailed: {failed}"
    )

if __name__ == "__main__":
    app.run()
