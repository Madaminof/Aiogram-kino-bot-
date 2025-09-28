import json
import os

KINO_CODES_FILE = "kino_codes.json"

# Fayl mavjud bo'lmasa yaratamiz
if not os.path.exists(KINO_CODES_FILE):
    with open(KINO_CODES_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)


async def add_kino(kod: str, name: str, message_id: int, file_id: str):
    """Yangi kino qo‘shish"""
    with open(KINO_CODES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data[kod] = {
        "name": name,
        "message_id": message_id,
        "file_id": file_id
    }

    with open(KINO_CODES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def get_kino(kod: str):
    """Kod orqali kino olish"""
    with open(KINO_CODES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get(kod)
