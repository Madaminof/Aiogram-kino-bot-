import asyncio
import aiofiles
import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from config import BOT_TOKEN, CHANNEL_ID

# Botni sozlash
bot = Bot(
    token=BOT_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode="HTML"),
)
router = Router()
dp = Dispatcher()

# JSON fayl nomi
kino_codes_file = "kino_codes.json"


async def get_kino_from_file(kino_code: str):
    """
    JSON fayldan kino kodi bo'yicha kino nomi va message_id ni qaytaradi.
    """
    try:
        async with aiofiles.open(kino_codes_file, mode="r") as file:
            try:
                data = json.loads(await file.read())
                kino_info = data.get(kino_code)
                if kino_info:
                    return kino_info["name"], kino_info["message_id"]
                return None, None
            except json.JSONDecodeError:
                return None, None
    except FileNotFoundError:
        return None, None


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
        kino_nomi, message_id = await get_kino_from_file(kino_kodi)
        if kino_nomi and message_id:
            # Kino kodi, nomi va message_id topilganda, kino nomi va video yuboriladi
            await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=message_id,
            )
        else:
            await message.answer("Bunday kino kodi topilmadi. Iltimos, kino kodini tekshiring.")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")


async def main():
    """
    Asosiy botni ishga tushirish funksiyasi.
    """
    # Routerni dispatcherga ulash
    dp.include_router(router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
