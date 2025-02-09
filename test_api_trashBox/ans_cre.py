import requests

BASE_URL = "https://api.recordonline.kg/api/v1/"
AUTH_URL = f"{BASE_URL}sign-in/"
AUTH_DATA = {
    "email": "admin@gmail.com",
    "password": "adminadmin",
}

# Авторизация и получение токена
try:
    auth_response = requests.post(AUTH_URL, data=AUTH_DATA)
    auth_response.raise_for_status()
    token = auth_response.json().get('token')
    if not token:
        raise ValueError("Не удалось получить токен. Проверьте данные авторизации.")
except requests.RequestException as e:
    print("Ошибка при авторизации:", e)
    exit(1)
video_id = 1  # Замените на нужный ID видео
question_id = 2  # Замените на ID вопроса
answer = "B"

endpoint = f"{BASE_URL}/videos/{video_id}/submit_answer/"

headers = {
    "Authorization": f"Bearer {token}"  # Замените на токен пользователя
}

data = {
    # "question_id": question_id,
    "answer": answer
}

response = requests.post(endpoint, json=data, headers=headers)

if response.status_code in [200, 201]:
    print("Ответ успешно отправлен.")
    print(response.json())
# else:
#     print(f"Ошибка: {response.status_code} - {response.json()}")
