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
    await message.answer(
        "👋 Xush kelibsiz!\n"
        "Avval video yuboring 🎥\n"
        "Keyin esa shu tartibda yuboring:\n\n"
        "Kino: kino_nomi\n"
        "Kod: kino_kodi"
    )


@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id

    # 1️⃣ Video yuborilgan bo‘lsa
    if message.video:
        user_sessions[user_id] = {"video_id": message.video.file_id}
        await message.answer("✅ Video qabul qilindi.\nEndi yuboring:\nKino: kino_nomi")

    # 2️⃣ Agar foydalanuvchi Kino: yuborsa
    elif user_id in user_sessions and message.text.startswith("Kino:"):
        kino_name = message.text.replace("Kino:", "").strip()
        user_sessions[user_id]["kino_name"] = kino_name
        await message.answer("✅ Kino nomi qabul qilindi.\nEndi yuboring:\nKod: kino_kodi")

    # 3️⃣ Agar foydalanuvchi Kod: yuborsa
    elif user_id in user_sessions and message.text.startswith("Kod:"):
        kino_code = message.text.replace("Kod:", "").strip()
        session = user_sessions[user_id]

        # Barcha ma’lumotlar tayyor bo‘lsa kanalga yuborish
        if "video_id" in session and "kino_name" in session:
            sent_message = await message.bot.send_video(
                chat_id=CHANNEL_ID,
                video=session["video_id"],
                caption=f"🎬 Kino: {session['kino_name']}\n🔑 Kod: {kino_code}",
            )

            # JSON ga saqlash
            await add_kino(kino_code, session["kino_name"], sent_message.message_id)

            await message.answer(
                f"✅ Video kanalga yuborildi!\n"
                f"📌 Kino: {session['kino_name']}\n"
                f"🔑 Kod: {kino_code}"
            )

            # Session tozalash
            del user_sessions[user_id]
        else:
            await message.answer("❗ Avval Kino: nomini yuboring.")

    else:
        await message.answer(
            "❗ Avval video yuboring 🎥, keyin esa quyidagi tartibda yozing:\n\n"
            "Kino: kino_nomi\n"
            "Kod: kino_kodi"
        )


async def main():
    bot = Bot(
        token=UPLOAD_BOT_TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML")
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
