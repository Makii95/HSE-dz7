import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

MONTHS_RU = {
    "January": "января", "February": "февраля", "March": "марта", "April": "апреля",
    "May": "мая", "June": "июня", "July": "июля", "August": "августа",
    "September": "сентября", "October": "октября", "November": "ноября", "December": "декабря"
}

def format_github_date(date_str):
    if not date_str:
        return "Не указано"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        month_en = dt.strftime("%B")
        month_ru = MONTHS_RU.get(month_en, month_en)
        day = dt.strftime("%d").lstrip("0")
        return f"{day} {month_ru} {dt.year} в {dt.strftime('%H:%M')}"
    except ValueError:
        return "Не указано"


def fetch_github_user_data():
    if not GITHUB_TOKEN:
        print("Токен отсутствует! Укажите его в .env файле.")
        return {}

    try:
        api_url = "https://api.github.com/user"
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}, ответ: {response.text}")
            return {}

        user_data = response.json()

        return {
            "name": user_data.get("name", "Не указано"),
            "login": user_data.get("login", "Не указано"),
            "email": user_data.get("email", "Не указано"),
            "public_repos": user_data.get("public_repos", "Не указано"),
            "followers": user_data.get("followers", "Не указано"),
            "created_at": format_github_date(user_data.get("created_at")),
            "bio": user_data.get("bio", "Не указано"),
            "blog": user_data.get("blog", "Не указано"),
        }
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {}
