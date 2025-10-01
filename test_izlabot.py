import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from config import BOT_TOKEN, CHANNEL_ID, SUBSCRIPTION_CHANNEL
from storage import get_kino

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(
    token=BOT_TOKEN,
    session=AiohttpSession(),
    parse_mode="HTML"  # shu yerda beriladi
)
dp = Dispatcher()
router = Router()
dp.include_router(router)


SUBSCRIPTION_CHANNEL = "@android_notes_developer"

@router.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        # Foydalanuvchini kanal a'zoligini tekshiramiz
        user = await bot.get_chat_member(SUBSCRIPTION_CHANNEL, message.from_user.id)

        if user.status in ["member", "creator", "administrator"]:
            await message.answer("✅ Obuna tasdiqlandi!\n\n🎬 Kino kodini yuboring.")
        else:
            # Agar status boshqa bo‘lsa, obuna bo‘lmagan hisoblanadi
            await message.answer(
                f"❗ Botdan foydalanish uchun kanalga obuna bo‘ling:\n"
                f"👉 <a href='https://t.me/{SUBSCRIPTION_CHANNEL.lstrip('@')}'>Obuna bo‘lish</a>\n\n"
                f"Obuna bo‘lgach, /start ni qayta yuboring.",
                disable_web_page_preview=True
            )

    except Exception as e:
        # Har qanday xato bo‘lsa ham obuna bo‘lish linkini yuboramiz
        logger.error(f"Obuna tekshirishda xatolik: {e}")
        await message.answer(
            f"❗ Botdan foydalanish uchun kanalga obuna bo‘ling:\n"
            f"👉 <a href='https://t.me/{SUBSCRIPTION_CHANNEL.lstrip('@')}'>Obuna bo‘lish</a>\n\n"
            f"Obuna bo‘lgach, /start ni qayta yuboring.",
            disable_web_page_preview=True
        )


@router.message()
async def get_kino_handler(message: types.Message):
    kino_kodi = message.text.strip()
    kino_info = await get_kino(kino_kodi)

    if not kino_info:
        await message.answer("❌ Bunday kino kodi topilmadi.")
        return

    try:
        await bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=kino_info["message_id"],
        )
    except Exception as e:
        logger.error(f"copy_message ishlamadi: {e}")
        if kino_info.get("file_id"):
            try:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=kino_info["file_id"],
                    caption=f"🎬 Kino: {kino_info['name']}\n🔑 Kod: {kino_info['code']}"
                )
            except Exception as e2:
                logger.error(f"file_id orqali ham yuborilmadi: {e2}")
                await message.answer("❌ Video yuborishda xatolik yuz berdi.")
        else:
            await message.answer("❌ Video ma’lumotlari yo‘q.")

async def main():
    logger.info("📌 Izlabot ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
