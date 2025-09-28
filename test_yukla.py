import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties

from config import UPLOAD_BOT_TOKEN, CHANNEL_ID
from storage import add_kino

# Logging
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
user_sessions = {}  # foydalanuvchi sessionlari

@dp.message(Command("start"))
async def command_start_handler(message: Message):
    await message.answer("👋 Xush kelibsiz!\nAvval video yuboring, keyin `Kino: nomi` va `Kod: kodi` formatida yuboring.")

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id

    # 🔹 Video yuborilgan bo‘lsa
    if message.video:
        user_sessions[user_id] = {"video_id": message.video.file_id}
        await message.answer("✅ Video qabul qilindi.\nEndi `Kino: nomi` va `Kod: kodi` yuboring.")
        return

    # 🔹 Foydalanuvchi video yuborgandan keyin matn yuborsa
    if user_id in user_sessions and "Kino:" in message.text and "Kod:" in message.text:
        try:
            lines = message.text.split("\n")
            kino_name = lines[0].split("Kino:")[1].strip()
            kino_code = lines[1].split("Kod:")[1].strip()

            video_id = user_sessions[user_id]["video_id"]

            sent_message = await message.bot.send_video(
                chat_id=CHANNEL_ID,
                video=video_id,
                caption=f"🎬 Kino: {kino_name}\n🔑 Kod: {kino_code}"
            )

            # 🔹 PostgreSQL ga yozish
            await add_kino(kino_code, kino_name, sent_message.message_id, video_id)

            await message.answer(f"✅ Kino kanalga yuborildi.\nMessage ID: {sent_message.message_id}")
            del user_sessions[user_id]

        except Exception as e:
            await message.answer(f"❌ Xatolik: {e}")

    else:
        await message.answer("❗ Avval video yuboring, so‘ng `Kino: nomi` va `Kod: kodi` yuboring.")

async def main():
    bot = Bot(
        token=UPLOAD_BOT_TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML")
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
