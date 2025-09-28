import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties

from config import UPLOAD_BOT_TOKEN, CHANNEL_ID
from storage import add_kino

# Logging sozlash
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

# Foydalanuvchi sessionlari
user_sessions = {}


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("👋 Xush kelibsiz!\nAvval video yuboring.\nSo‘ng formatda yuboring:\n\nKino: kino_nomi\nKod: kino_kodi")


@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id

    # Video yuborilgan bo‘lsa
    if message.video:
        user_sessions[user_id] = {"video_id": message.video.file_id}
        await message.answer("✅ Video qabul qilindi.\nEndi formatda yuboring:\n\nKino: kino_nomi\nKod: kino_kodi")

    # Agar foydalanuvchi video yuborgandan keyin Kino/Kod yuborsa
    elif user_id in user_sessions and "Kino:" in message.text and "Kod:" in message.text:
        lines = message.text.split("\n")
        kino_name = lines[0].replace("Kino:", "").strip()
        kino_code = lines[1].replace("Kod:", "").strip()

        video_id = user_sessions[user_id]["video_id"]

        # Kanalga yuborish
        sent_message = await message.bot.send_video(
            chat_id=CHANNEL_ID,
            video=video_id,
            caption=f"🎬 Kino: {kino_name}\n🔑 Kod: {kino_code}",
        )

        # JSON faylga yozish
        await add_kino(
            kod=kino_code,
            name=kino_name,
            message_id=sent_message.message_id,
            file_id=video_id
        )

        await message.answer(f"✅ Kino kanalga yuborildi!\nKod: {kino_code}")

        # Session tozalash
        del user_sessions[user_id]

    else:
        await message.answer("❗ Avval video yuboring, keyin formatda yozing:\n\nKino: kino_nomi\nKod: kino_kodi")


async def main():
    bot = Bot(
        token=UPLOAD_BOT_TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
