# test_izlabot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

from config import BOT_TOKEN, CHANNEL_ID, SUBSCRIPTION_CHANNEL
from storage import get_kino

# Logging sozlash
logging.basicConfig(level=logging.INFO)

# Bot obyektlari
bot = Bot(
    token=BOT_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode="HTML"),
)
router = Router()
dp = Dispatcher()
dp.include_router(router)


@router.message(Command("start"))
async def start_handler(message: types.Message):
    """Start komandasi: obunani tekshiradi"""
    try:
        user = await bot.get_chat_member(chat_id=SUBSCRIPTION_CHANNEL, user_id=message.from_user.id)
        if user.status in ["member", "creator", "administrator"]:
            await message.answer("✅ Obuna tasdiqlandi!\n\n🎬 Kino kodini yuboring.")
        else:
            raise Exception("Not subscribed")
    except Exception:
        link = f"https://t.me/{SUBSCRIPTION_CHANNEL.lstrip('@')}"
        await message.answer(
            f"❗ Botdan foydalanish uchun kanalga obuna bo‘ling:\n👉 <a href='{link}'>Obuna bo‘lish</a>\n\nObuna bo‘lgach, /start ni qayta yuboring.",
            disable_web_page_preview=True
        )


@router.message()
async def get_kino_handler(message: types.Message):
    """Kino kodini yuborganda video chiqarish"""
    kino_kodi = message.text.strip()
    kino_info = await get_kino(kino_kodi)

    if kino_info:
        try:
            await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=kino_info["message_id"],
            )
        except Exception as e:
            logging.error(f"Video yuborishda xatolik: {e}")
            await message.answer("❌ Video yuborishda xatolik yuz berdi.")
    else:
        await message.answer("❌ Bunday kino kodi topilmadi. Iltimos, kodni tekshiring.")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
