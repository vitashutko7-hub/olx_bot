import telebot
import requests
from bs4 import BeautifulSoup
import time 
import os
import json

# 🔑 ВСТАВ свій токен і свій Telegram ID
BOT_TOKEN = "8521927589:AAGl-trzqEu4tdW2yGWGBLFG-sytlssMg18"
YOUR_ID = 1381602436  # твій Telegram ID

bot = telebot.TeleBot(BOT_TOKEN)
# 📦 Файл для збереження старих оголошень
ADS_FILE = "known_ads.json"

# Завантажуємо збережені оголошення (якщо файл існує)
if os.path.exists(ADS_FILE):
    with open(ADS_FILE, "r", encoding="utf-8") as f:
        known_ads = set(json.load(f))
else:
    known_ads = set()

# Зберігаємо нові оголошення
def save_known_ads():
    with open(ADS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(known_ads), f, ensure_ascii=False, indent=2)
# 🔹 Усі твої OLX-посилання
OLX_URLS = [
    "https://www.olx.pl/motoryzacja/samochody/mitsubishi/?search%5Bfilter_enum_model%5D%5B0%5D=pajero&search%5Bfilter_float_price%3Ato%5D=35000&search%5Bfilter_float_year%3Afrom%5D=2007&search%5Border%5D=created_at%3Adesc",
    "https://www.olx.pl/motoryzacja/samochody/?search%5Bfilter_enum_car_body%5D%5B0%5D=pickup&search%5Bfilter_float_price%3Ato%5D=50000&search%5Bfilter_float_year%3Afrom%5D=2007&search%5Border%5D=created_at%3Adesc",
    "https://www.olx.pl/motoryzacja/samochody/volkswagen/?search%5Bfilter_enum_model%5D%5B0%5D=amarok&search%5Bfilter_float_price%3Ato%5D=50000&search%5Border%5D=created_at%3Adesc",
    "https://www.olx.pl/motoryzacja/samochody/ford/?search%5Bfilter_enum_model%5D%5B0%5D=ranger&search%5Bfilter_float_price%3Ato%5D=50000&search%5Border%5D=created_at%3Adesc",
    "https://www.olx.pl/motoryzacja/dostawcze/furgon-blaszak/q-4-motion/?search%5Bfilter_float_price%3Ato%5D=50000&search%5Border%5D=created_at%3Adesc",
    "https://www.olx.pl/motoryzacja/samochody/mitsubishi/?search%5Bfilter_enum_model%5D%5B0%5D=l200&search%5Bfilter_float_price%3Ato%5D=50000&search%5Bfilter_float_year%3Afrom%5D=2010&search%5Border%5D=created_at%3Adesc",
    "https://www.olx.pl/motoryzacja/samochody/toyota/?my_ads=1&search%5Bfilter_enum_model%5D%5B0%5D=hilux&search%5Bfilter_float_price%3Ato%5D=50000&search%5Bfilter_float_year%3Afrom%5D=2008&search%5Border%5D=created_at%3Adesc",
    "https://www.olx.pl/motoryzacja/samochody/isuzu/?search%5Bfilter_enum_model%5D%5B0%5D=d-max&search%5Bfilter_enum_model%5D%5B1%5D=pick-up&search%5Bfilter_float_price%3Ato%5D=50000&search%5Border%5D=created_at%3Adesc",
    "https://www.olx.pl/motoryzacja/dostawcze/q-toyota-hiace/?search%5Bfilter_float_year%3Afrom%5D=2007&search%5Border%5D=relevance%3Adesc",
    "https://www.olx.pl/motoryzacja/dostawcze/q-4x4/?search%5Bfilter_float_price%3Ato%5D=50000&search%5Bfilter_float_year%3Afrom%5D=2010&search%5Border%5D=created_at%3Adesc"
]
def get_new_ads():
    new_ads = []

    for url in OLX_URLS:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            ads = soup.select("div[data-cy='l-card']")

            for ad in ads:
                link = ad.select_one("a.css-rc5s2u")["href"]
                if not link.startswith("http"):
                    link = "https://www.olx.pl" + link

                # Якщо оголошення нове — додаємо
                if link not in known_ads:
                    known_ads.add(link)
                    new_ads.append(link)

        except Exception as e:
            print(f"Помилка при обробці {url}: {e}")

    # Зберігаємо оновлений список відомих оголошень
    save_known_ads()

    return new_ads
# 📦 Словник для збереження старих оголошень
known_ads = set()

def get_new_ads():
    new_ads = []
    for url in OLX_URLS:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            ads = soup.select("div[data-cy='l-card']")
            for ad in ads:
                link = ad.select_one("a")["href"] if ad.select_one("a") else ""
                if not link.startswith("http"):
                    link = "https://www.olx.pl" + link
                if link not in known_ads:
                    known_ads.add(link)
                    title = ad.select_one("h6").text.strip() if ad.select_one("h6") else "Без назви"
                    new_ads.append(f"{title}\n{link}")
        except Exception as e:
            print(f"Помилка з {url}: {e}")
    return new_ads
    def send_new_ads():
    while True:
        new_ads = get_new_ads()

        if new_ads:
            for ad in new_ads:
                bot.send_message(YOUR_ID, ad)
                time.sleep(2)  # невелика пауза між повідомленнями
        else:
            print("Нових оголошень немає.")

        time.sleep(300)  # перевіряти кожні 5 хвилин


# 🔹 Запускаємо бота
if __name__ == "__main__":
    bot.send_message(YOUR_ID, "🤖 Бот запущено! Чекаю нових оголошень...")
    send_new_ads()

# 🕒 Перевірка OLX кожні 5 хвилин
def check_loop():
    while True:
        new_ads = get_new_ads()
        if new_ads:
            bot.send_message(YOUR_ID, f"🚗 Нові оголошення знайдено: {len(new_ads)}")
            for ad in new_ads:
                bot.send_message(YOUR_ID, ad)
        else:
            bot.send_message(YOUR_ID, "ℹ️ Нових оголошень поки немає.")
        time.sleep(300)  # 300 секунд = 5 хвилин

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "👋 Привіт! Я буду надсилати тобі нові авто-оголошення з OLX кожні 5 хвилин.")

import threading
threading.Thread(target=check_loop, daemon=True).start()

bot.infinity_polling()
