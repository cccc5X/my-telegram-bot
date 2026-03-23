from telethon import TelegramClient, events, Button
import asyncio
import random

‎# بياناتك
API_ID = 23880529 
API_HASH = '1fe31c66b4423429dea10934870155e1' 
BOT_TOKEN = '8722917878:AAFEPYoqVrVBEFo6HdZZ2beQ-CqZQWk5RH8' 
OWNER_ID = 1867845900

‎# تشغيل البوت والارتباط بملف الجلسة
bot = TelegramClient('bot_control', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user = TelegramClient('user_session', API_ID, API_HASH)

db = {"groups": [], "messages": [], "is_running": False}

@bot.on(events.NewMessage(pattern='/start', from_users=OWNER_ID))
async def start(event):
    buttons = [
        [Button.inline("➕ إضافة مجموعة", b"add_g"), Button.inline("📝 إضافة رسالة", b"add_m")],
        [Button.inline("🚀 بدء النشر", b"run"), Button.inline("🛑 إيقاف", b"stop")]
    ]
    await event.respond("✅ النظام جاهز على Koyeb!\nتم العثور على ملف الجلسة.", buttons=buttons)

@bot.on(events.CallbackQuery(from_users=OWNER_ID))
async def handler(event):
    if event.data == b"add_g":
        async with bot.conversation(event.chat_id) as conv:
            await conv.send_message("ارسل يوزر المجموعة مع الـ @:")
            res = await conv.get_response()
            db["groups"].append(res.text)
            await conv.send_message("✅ تم")
    elif event.data == b"add_m":
        async with bot.conversation(event.chat_id) as conv:
            await conv.send_message("ارسل نص الإعلان:")
            res = await conv.get_response()
            db["messages"].append(res.text)
            await conv.send_message("✅ تم")
    elif event.data == b"run":
        db["is_running"] = True
        asyncio.create_task(run_poster())
        await event.answer("🚀 بدأ النشر!")

async def run_poster():
    if not user.is_connected(): await user.start()
    while db["is_running"]:
        for g in db["groups"]:
            try:
                await user.send_message(g, random.choice(db["messages"]))
                await asyncio.sleep(30)
            except: pass
        await asyncio.sleep(600)

print("🚀 البوت يعمل...")
bot.run_until_disconnected()
