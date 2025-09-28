# test_yukla.py
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

# Har bir foydalanuvchi uchun session
user_sessions = {}


@dp.message(Command("start"))
async def command_start_handler(message: Message):
    await message.answer("👋 Xush kelibsiz!\nAvval video yuboring, so‘ngra kod va nom yuboring. Format: kod: nom")


@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id

    # Video yuborilgan bo‘lsa
    if message.video:
        user_sessions[user_id] = {"video_id": message.video.file_id}
        await message.answer("✅ Video qabul qilindi.\nEndi formatda yuboring: kod: nom")

    # Agar foydalanuvchi video yuborgandan keyin kod yuborsa
    elif user_id in user_sessions and ":" in message.text:
        kino_code, kino_name = message.text.split(":", 1)
        video_id = user_sessions[user_id]["video_id"]

        sent_message = await message.bot.send_video(
            chat_id=CHANNEL_ID,
            video=video_id,
            caption=f"🎬 Kino kodi: {kino_code.strip()}\n📌 Nomi: {kino_name.strip()}",
        )

        # JSON faylga saqlash
        await add_kino(kino_code.strip(), kino_name.strip(), sent_message.message_id)

        await message.answer(f"✅ Video kanalga yuborildi.\nMessage ID: {sent_message.message_id}")

        # Session tozalash
        del user_sessions[user_id]

    else:
        await message.answer("❗ Avval video yuboring, keyin formatda yozing: kod: nom")


async def main():
    bot = Bot(
        token=UPLOAD_BOT_TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML")
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
