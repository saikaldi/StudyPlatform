import requests
import json
from pprint import pprint

# Конфигурация
BASE_URL = "http://127.0.0.1:8000/api/v1/"
AUTH_URL = f"{BASE_URL}sign-in/"
AUTH_DATA = {
    "email": "aktanarynov566@gmail.com",
    "password": "stringst",
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

# Заголовки авторизации
auth_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
}

# Функция для выполнения запросов
def make_request(url, method='GET', data=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=auth_headers)
        elif method == 'POST':
            response = requests.post(url, headers=auth_headers, data=json.dumps(data))
        else:
            raise ValueError(f"Метод {method} не поддерживается.")
        
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка запроса {method} к {url}:")
        if e.response:
            pprint(e.response.json())
        else:
            print(e)
        return None

# Тестирование API
print("Тестирование CategoryVideo ViewSet:")
category_videos = make_request(f"{BASE_URL}category-video/")
pprint(category_videos)

print("\nТестирование Video ViewSet:")
videos = make_request(f"{BASE_URL}video/")
pprint(videos)

video_id = 2

print("\nПроверка доступа к видео:")
access_check = make_request(f"{BASE_URL}video/{video_id}/check_access/")
pprint(access_check)

print("\nТестирование TestContent ViewSet:")
test_contents = make_request(f"{BASE_URL}test-content/")
pprint(test_contents)

test_content_id = 3

print("\nОтправка ответа на тест:")
submit_answer = make_request(
    f"{BASE_URL}test-content/{test_content_id}/submit_answer/",
    method='POST',
    data={'answer': 'd'},  # Пример ответа
)
pprint(submit_answer)

# Сброс теста
# print("\nСброс теста:")
# reset_test = make_request(
#     f"{BASE_URL}test-content/{test_content_id}/reset_test/",
#     method='POST',
# )
# pprint(reset_test)

print("\nТестирование UserStatistic ViewSet:")
user_statistics = make_request(f"{BASE_URL}user-statistic/")
pprint(user_statistics)

print("\nТестирование UserAnswer ViewSet:")
user_answers = make_request(f"{BASE_URL}user-answer/")
pprint(user_answers)

print("\nТестирование ошибок:")
try:
    invalid_test = make_request(
        f"{BASE_URL}test-content/999/submit_answer/",
        method='POST',
        data={'answer': 'a'},  # Неверный формат ответа
    )
    pprint(invalid_test)
except Exception as e:
    print("Обработана ошибка:", e)

# # Сброс всех тестов для одного видео
# print("\nСброс всех тестов для видео:")
# video_id = 1  # или другой ID видео, которое вы хотите сбросить
# reset_all_tests = make_request(
#     f"{BASE_URL}video/{video_id}/reset_all_tests/",
#     method='POST',
# )
# pprint(reset_all_tests)
