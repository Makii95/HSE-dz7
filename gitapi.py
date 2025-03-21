import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("Ошибка: Токен GitHub отсутствует! Укажите его в .env файле.")

cached_user_data = None  # Кэш для хранения данных пользователя

def fetch_github_user_data():
    """Функция для получения данных пользователя из GitHub API."""
    global cached_user_data
    try:
        api_url = "https://api.github.com/user"
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}

        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}, ответ: {response.text}")
            return {}

        if 'application/json' not in response.headers.get('Content-Type', ''):
            print("Ошибка: Сервер вернул HTML вместо JSON.")
            return {}

        user_data = response.json()

        filtered_data = {
            "name": user_data.get("name", "Не указано"),
            "login": user_data.get("login", "Не указано"),
            "email": user_data.get("email", "Не указано"),
            "public_repos": user_data.get("public_repos", "Не указано"),
            "followers": user_data.get("followers", "Не указано"),
            "created_at": user_data.get("created_at", "Не указано"),
            "bio": user_data.get("bio", "Не указано"),
            "blog": user_data.get("blog", "Не указано")
        }

        cached_user_data = filtered_data
        return filtered_data

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {}
