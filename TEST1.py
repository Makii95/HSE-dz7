import json
import requests
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, template_folder="templates")

# Функция для загрузки конфигурации
def load_config():
    try:
        with open("config.json") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"github_token": ""}

config = load_config()

def get_github_user():
    url = "https://api.github.com/user"
    headers = {"Authorization": f'token {config.get("github_token", "")}'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and "application/json" in response.headers.get("Content-Type", ""):
            return response.json()
    except requests.RequestException as error:
        print(f"Ошибка при запросе к GitHub: {error}")

    return {}

@app.route("/")
def home():
    return render_template("resume_template.html", user=get_github_user())

@app.route("/update")
def refresh():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
