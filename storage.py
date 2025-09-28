# storage.py
import aiofiles
import json

DATA_FILE = "kino_data.json"  # Fayl nomi

async def load_data() -> dict:
    """JSON fayldan ma’lumotlarni yuklash"""
    try:
        async with aiofiles.open(DATA_FILE, "r") as f:
            return json.loads(await f.read())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

async def save_data(data: dict):
    """Ma’lumotlarni JSON faylga saqlash"""
    async with aiofiles.open(DATA_FILE, "w") as f:
        await f.write(json.dumps(data, indent=4, ensure_ascii=False))

async def get_kino(kino_code: str):
    """Kino kodiga qarab kino nomi va message_id ni olish"""
    data = await load_data()
    return data.get(kino_code)

async def add_kino(kino_code: str, kino_name: str, message_id: int):
    """Kino qo‘shish yoki yangilash"""
    data = await load_data()
    data[kino_code] = {"name": kino_name, "message_id": message_id}
    await save_data(data)
