# test_izlabot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from config import BOT_TOKEN, CHANNEL_ID, SUBSCRIPTION_CHANNEL
from storage import get_kino

# 🔹 Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 🔹 Bot va Dispatcher
bot = Bot(
    token=BOT_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode="HTML"),
)
dp = Dispatcher()
router = Router()
dp.include_router(router)


# 🔹 Start komandasi
@router.message(Command("start"))
async def start_handler(message: types.Message):
    """Foydalanuvchi start bosganda obunani tekshiradi"""
    try:
        user = await bot.get_chat_member(
            chat_id=SUBSCRIPTION_CHANNEL,
            user_id=message.from_user.id
        )

        if user.status in ["member", "creator", "administrator"]:
            await message.answer(
                "✅ Obuna tasdiqlandi!\n\n🎬 Kino kodini yuboring."
            )
        else:
            raise TelegramBadRequest("Not subscribed")

    except TelegramBadRequest:
        link = f"https://t.me/{SUBSCRIPTION_CHANNEL.lstrip('@')}"
        await message.answer(
            f"❗ Botdan foydalanish uchun kanalga obuna bo‘ling:\n"
            f"👉 <a href='{link}'>Obuna bo‘lish</a>\n\n"
            f"Obuna bo‘lgach, /start ni qayta yuboring.",
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Obuna tekshirishda xatolik: {e}")
        await message.answer("❌ Obuna tekshirishda xatolik yuz berdi. Keyinroq urinib ko‘ring.")


# 🔹 Kino kodini ishlovchi handler
@router.message()
async def get_kino_handler(message: types.Message):
    """Kino kodini yuborganda video chiqarish"""
    kino_kodi = message.text.strip()
    kino_info = await get_kino(kino_kodi)

    if not kino_info:
        await message.answer("❌ Bunday kino kodi topilmadi. Iltimos, kodni tekshiring.")
        return

    try:
        # Kino nomi va kodini format bilan yuborish
        caption = f"🎬 Kino: {kino_info['name']}\n🔑 Kod: {kino_info['code']}"

        await bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=kino_info["message_id"],
            caption=caption
        )
    except Exception as e:
        logger.error(f"Video yuborishda xatolik: {e}")
        await message.answer("❌ Video yuborishda xatolik yuz berdi.")


# 🔹 Asosiy ishga tushirish
async def main():
    logger.info("📌 Izlabot ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
