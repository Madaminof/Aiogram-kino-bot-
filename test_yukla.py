import asyncio
import logging
import json
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties

# Bot tokeningizni kiriting
TOKEN = "7907590797:AAH6yrkSbxeay0KfRuxdwFTpzqY23J9qzKM"

# Dispatcher yaratamiz
dp = Dispatcher()

# Video yuborish uchun o'zgaruvchilar
video_id = None
waiting_for_code = False

# Kino kodi, nomi va message_id'larni saqlash uchun fayl nomi
kino_codes_file = "kino_codes.json"


# Kino kodi, nomi va message_id ni JSON faylga saqlash yoki yangilash
def save_kino_code(kino_code, kino_name, message_id):
    try:
        # Fayldan mavjud ma'lumotni yuklab olish
        with open(kino_codes_file, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    except FileNotFoundError:
        data = {}

    # Ma'lumotlarni yangilash
    data[kino_code] = {"name": kino_name, "message_id": message_id}

    # Yangilangan ma'lumotni faylga qayta yozish
    with open(kino_codes_file, "w") as file:
        json.dump(data, file, indent=4)


# JSON fayldan kino kodi bo'yicha kino nomi va message_id ni olish
def get_message_id_from_file(kino_code):
    try:
        with open(kino_codes_file, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return None
            return data.get(kino_code)
    except FileNotFoundError:
        return None


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """Botga start buyrug‘ini jo‘natganda ishlaydi."""
    await message.answer(
        "Botga xush kelibsiz! Avval video yuboring, keyin esa kino kodi va nomini yuborishingizni so'rayman. Format: kod: name."
    )


@dp.message()
async def handle_video(message: Message) -> None:
    """Video yuborish uchun handler."""
    global video_id, waiting_for_code

    if message.video:
        # Foydalanuvchi video yuborgan bo'lsa
        video_id = message.video.file_id
        waiting_for_code = True
        await message.answer("Kino kodi va nomini yuboring. Format: kod: name")
    elif waiting_for_code:
        # Kino kodi va nomi yuborilsa, video va kodi kanalga yuboriladi
        code_name = message.text.strip()
        if ":" not in code_name:
            await message.answer("Iltimos, kino kodi va nomini to'g'ri formatda yuboring: kod: name")
            return

        kino_code, kino_name = code_name.split(":", 1)
        if video_id:
            sent_message = await message.bot.send_video(
                chat_id='@kinotopbot01',
                video=video_id,
                caption=f"Kino kodi: {kino_code} \nKino nomi:{kino_name}"
            )
            # Kino kodi, nomi va message_id ni JSON faylga saqlash
            save_kino_code(kino_code.strip(), kino_name.strip(), sent_message.message_id)

            await message.answer(f"Video va kino kodi kanalga yuborildi. Message ID: {sent_message.message_id}")
            # Video va kod yuborilganidan so'ng, navbatni tozalash
            video_id = None
            waiting_for_code = False
        else:
            await message.answer("Iltimos, avval video yuboring.")
    else:
        await message.answer("Avval video yuboring, so'ngra kino kodi va nomini yuborishingizni kutyapman.")


async def main():
    logging.basicConfig(level=logging.INFO)

    # Bot obyektini to'g'ri konfiguratsiya qilamiz
    bot = Bot(
        token=TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML")  # Yangi usulda parse_mode
    )

    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
