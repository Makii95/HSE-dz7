import httpx
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

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
        month_ru = MONTHS_RU.get(dt.strftime("%B"), dt.strftime("%B"))
        return f"{dt.day} {month_ru} {dt.year} в {dt.strftime('%H:%M')}"
    except (ValueError, TypeError):
        return "Не указано"

async def fetch_github_user_data_async():
    if not GITHUB_TOKEN:
        print("Токен отсутствует! Укажите его в .env файле.")
        return {}

    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    api_url = "https://api.github.com/user"

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()

            user_data = response.json() or {}
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
        except httpx.HTTPStatusError as e:
            print(f"Ошибка HTTP {e.response.status_code}: {e.response.text}")
        except httpx.TimeoutException:
            print("Ошибка: Таймаут запроса к GitHub API.")
        except httpx.RequestError as e:
            print(f"Ошибка сети: {e}")

    return {}

def fetch_github_user_data():
    return asyncio.run(fetch_github_user_data_async())
