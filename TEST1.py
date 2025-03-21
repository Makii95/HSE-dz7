import json
import requests
from flask import Flask, render_template, redirect, url_for
import os

app = Flask(__name__, template_folder='templates')

CONFIG_FILE = "config.json"

if not os.path.exists(CONFIG_FILE):
    print(f"Ошибка: Файл {CONFIG_FILE} отсутствует. Создайте его вручную и добавьте ваш GitHub токен.")
    exit(1)

try:
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
        if not config.get("github_token"):
            print("Ошибка: Токен GitHub отсутствует в config.json!")
            exit(1)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Ошибка загрузки {CONFIG_FILE}: {e}")
    exit(1)

cached_user_data = None

def fetch_github_user_data():
    global cached_user_data
    try:
        api_url = "https://api.github.com/user"
        headers = {'Authorization': f'token {config["github_token"]}'}

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
            "profile_url": user_data.get("html_url", "#"),
            "public_repos": user_data.get("public_repos", "Не указано"),
            "followers": user_data.get("followers", "Не указано"),
            "created_at": user_data.get("created_at", "Не указано")
        }

        cached_user_data = filtered_data
        return filtered_data

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {}

@app.route('/')
def resume():
    global cached_user_data
    if cached_user_data is None:
        cached_user_data = fetch_github_user_data()
    return render_template('resume_template.html', user=cached_user_data)


@app.route('/update')
def update():
    global cached_user_data
    cached_user_data = fetch_github_user_data()
    return redirect(url_for('resume'))


if __name__ == '__main__':
    app.run(debug=True)
