import os
import json

def get_message_id(kino_kodi):
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, "kino_codes.json")

    try:
        # Faylni o'qishdan oldin, yangilanishini majburlash
        with open(json_path, "r", encoding="utf-8") as file:
            os.fsync(file.fileno())  # Faylni tizim keshidan yangilash
            data = json.load(file)
            return data.get(kino_kodi)
    except FileNotFoundError:
        print(f"Fayl topilmadi: {json_path}")
        return None
    except json.JSONDecodeError:
        print("JSON formatida xatolik mavjud.")
        return None
