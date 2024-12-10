import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from config import BOT_TOKEN, CHANNEL_ID
from db import get_message_id  # Yangi funksiyani import qilamiz

# Botni sozlash
bot = Bot(
    token=BOT_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode="HTML"),
)
router = Router()
dp = Dispatcher()

# Ma'lumotlar bazasi uchun havza saqlash
db_pool = None


@router.message(Command("start"))
async def start_handler(message: types.Message):
    """
    Start komandasi foydalanuvchiga bot haqida ma'lumot beradi.
    """
    await message.answer("Assalomu alaykum! \n🎬Kino kodini kiriting va bot sizga \ntegishli kinoni topib beradi.")


@router.message()
async def get_kino(message: types.Message):
    """
    Foydalanuvchi kino kodini kiritganda tegishli videoni botga yuboradi.
    """
    kino_kodi = message.text.strip()
    try:
        # Kino kodi asosida message_id ni olish
        message_id = get_message_id(kino_kodi)  # Endi JSON fayldan olamiz
        if message_id:
            # Kino kodi va message_id topilganda, video yuboriladi
            sent_message = await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=message_id,
            )
        else:
            await message.answer("Bunday kino kodi topilmadi.")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")


async def main():
    """
    Asosiy botni ishga tushirish funksiyasi.
    """
    global db_pool

    # Routerni dispatcherga ulash
    dp.include_router(router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
