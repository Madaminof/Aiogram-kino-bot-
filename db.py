import os
import json

def get_message_id(kino_kodi):
    # Loyihaning joriy katalogini aniqlash (ya'ni, izlovchi_bot.py joylashgan katalog)
    base_dir = os.path.dirname(__file__)  # Hozirgi skript joylashgan katalog
    json_path = os.path.join(base_dir, "kino_codes.json")  # .json fayl bilan bir xil papkada joylashgan

    print(f"JSON faylning yo'li: {json_path}")  # Tekshirish uchun yo'lni chiqarish

    try:
        # Faylni ochish va o'qish
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Kino kodi bo'yicha message_id ni qaytarish
            return data.get(kino_kodi)
    except FileNotFoundError:
        print(f"Fayl topilmadi: {json_path}")
        return None
    except json.JSONDecodeError:
        print("JSON formatida xatolik mavjud.")
        return None
