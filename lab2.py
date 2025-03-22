

import re
import random
import datetime
import webbrowser
import urllib.parse
import http.client  
import json  
import os

API_KEY = "083e1d1fe7c88dcf28e4d76c493fa34b"  

responses = {
    r"привет": ["Добрый день!", "Привет!", "Здравствуйте!"],
    r"как дела\??": ["Отлично!", "Хорошо", "Всё в порядке", "Неплохо, а у вас?"],
    r"как тебя зовут\??|кто ты такой\??": ["Меня зовут Бот!", "Я просто чат-бот."],
    r"сколько сейчас времени": lambda: datetime.datetime.now().strftime("%H:%M:%S"),
    r"какое сегодня число": lambda: datetime.datetime.now().strftime("%d.%m.%Y"),
    r"какая сейчас погода в городе\s+(.+)\??": "weather",
    r"поиск\s+(.+)": "search",
    r"(\d+)\s*([+\-\/*])\s*(\d+)": "calculate",
    r"выход": "exit",
    r"что ты умеешь\??|какие у тебя функции\??|что ты можешь\??": [
        "Я могу отвечать на приветствия, сообщать текущее время и дату.",
        "Я могу говорить о погоде, выполнять поиск в интернете, вычислять простые арифметические выражения и прощаться.",
        "Мои возможности пока ограничены, но я постоянно развиваюсь!"
    ],
    r"спасибо": ["Пожалуйста!", "Всегда рад помочь!", "Не за что."],
    r"хорошо|нормально": ["Отлично!"] 
}



def calculate(match):
    try:
        num1 = int(match.group(1))
        operator = match.group(2)
        num2 = int(match.group(3))

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "На ноль делить нельзя :("
            result = num1 / num2
        else:
            return "Неизвестная операция."

        return str(result)
    except ValueError:
        return "Некорректный ввод чисел."

def get_weather(city):
    global API_KEY
    conn = http.client.HTTPSConnection("api.openweathermap.org")
    encoded_city = urllib.parse.quote(city) 
    url = f"/data/2.5/weather?q={encoded_city}&appid={API_KEY}&units=metric&lang=ru"
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    conn.close()

    try:
        data = json.loads(data)
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"В городе {city} сейчас {weather_desc}, температура {temp}°C."
    except (KeyError, json.JSONDecodeError):
        print("Ошибка при обработке данных о погоде.")
        return "Не удалось получить информацию о погоде. Пожалуйста, убедитесь, что название города введено правильно и API-ключ указан верно."


def search_web(query):
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)
    return f"Открываю поиск для: {query}"

def chatbot_response(text):
    text = text.lower()
    for pattern, response_type in responses.items():
        match = re.search(pattern, text)
        if match:
            if isinstance(response_type, list):
                return random.choice(response_type) 
            elif callable(response_type):
                return response_type()
            elif response_type == "calculate":
                return calculate(match)
            elif response_type == "weather":
                city = match.group(1)
                return get_weather(city)
            elif response_type == "search":
                query = match.group(1)
                return search_web(query)
            elif response_type == "exit":
                return "До свидания!"
            else:
                return response_type
    return random.choice(["Я не понял вопрос.", "Попробуйте перефразировать."])


def log_message(user_message, bot_response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] User: {user_message}\n[{timestamp}] Bot: {response}\n"
    with open("chat_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)


if __name__ == "__main__":
    print("Привет! Я чат-бот. Введите 'выход' для завершения диалога.")

 
    if not os.path.exists("chat_log.txt"):
        with open("chat_log.txt", "w", encoding="utf-8") as f:
            f.write("Начало лога\n")

    while True:
        user_input = input("Вы: ")
        response = chatbot_response(user_input)
        print("Бот:", response)

        log_message(user_input, response) 

        if user_input.lower() == "выход":
            print("Завершение работы...")
            break
