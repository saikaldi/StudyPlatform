import requests
import json

# URL для аутентификации
auth_url = 'https://api.recordonline.kg/api/v1/sign-in/'
auth_data = {
    'email': 'admin@gmail.com',
    'password': 'adminadmin'
}

# Функция для получения токена аутентификации
def get_auth_token():
    response = requests.post(auth_url, json=auth_data)
    if response.status_code == 200:
        return response.json().get('token', None)
    else:
        print("Аутентификация не удалась:", response.status_code, response.text)
        return None

# Получение токена аутентификации
token = get_auth_token()
if not token:
    exit()

# Общие заголовки с токеном
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# 1. Categories - GET
def get_categories():
    url = 'http://localhost:8000/api/v1/categories/'
    response = requests.get(url, headers=headers)
    handle_response(response, "Категории")

# 2. Categories - POST
def create_category():
    url = 'http://localhost:8000/api/v1/categories/'
    data = {'category_name': 'Новая категория предмета'}
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Категория предмета")

# 3. Subject Categories - GET
def get_subject_categories():
    url = 'http://localhost:8000/api/v1/subject-categories/'
    response = requests.get(url, headers=headers)
    handle_response(response, "Подкатегории видео")

# 4. Subject Categories - POST
def create_subject_category():
    url = 'http://localhost:8000/api/v1/subject-categories/'
    data = {'subject_category_name': 'Новая подкатегория'}
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Подкатегория видео")

# 5. Category Videos - GET
def get_category_videos():
    url = 'http://localhost:8000/api/v1/category-video/'
    response = requests.get(url, headers=headers)
    handle_response(response, "Категории видео")

# 6. Category Videos - POST
def create_category_video():
    url = 'http://localhost:8000/api/v1/category-video/'
    data = {'category_name': 'Новая категория видео'}
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Категория видео")

# 7. Videos - GET
def get_videos():
    url = 'http://localhost:8000/api/v1/video/'
    response = requests.get(url, headers=headers)
    handle_response(response, "Видео")

# 8. Videos - POST
def create_video():
    url = 'http://localhost:8000/api/v1/video/'
    data = {
        'subject_name': 'Новая тема урока',
        'description': 'Описание новой темы',
        'video_url': 'URL к видео',
        'video_order': 1,
        'is_paid': True,
        'category_id': 1,  # ID категории предмета
        'video_category_id': 1,  # ID категории видео
        'subject_category_id': 1,  # ID подкатегории видео
    }
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Видео")

# 9. Videos - Check Access
def check_video_access(video_id):
    url = f'http://localhost:8000/api/v1/video/{video_id}/check_access/'
    response = requests.get(url, headers=headers)
    handle_response(response, f"Проверка доступа к видео {video_id}")

# 10. Videos - Reset Tests
def reset_video_tests(video_id):
    url = f'http://localhost:8000/api/v1/video/{video_id}/reset_all_tests/'
    response = requests.post(url, headers=headers)
    handle_response(response, f"Сброс тестов для видео {video_id}")

# 11. Test Content - GET
def get_test_content():
    url = 'http://localhost:8000/api/v1/test-content/'
    response = requests.get(url, headers=headers)
    handle_response(response, "Тестовый контент")

# 12. Test Content - POST (Submit Answer)
def submit_answer(test_content_id, answer):
    url = f'http://localhost:8000/api/v1/test-content/{test_content_id}/submit_answer/'
    data = {'answer': answer}
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, f"Отправка ответа для теста {test_content_id}")

# 13. Test Content - Reset Test
def reset_test(test_content_id):
    url = f'http://localhost:8000/api/v1/test-content/{test_content_id}/reset_test/'
    response = requests.post(url, headers=headers)
    handle_response(response, f"Сброс теста {test_content_id}")

# 14. User Statistics - GET
def get_user_statistics():
    url = 'http://localhost:8000/api/v1/user-statistic/'
    response = requests.get(url, headers=headers)
    handle_response(response, "Статистика пользователя")

# 15. User Answers - GET
def get_user_answers():
    url = 'http://localhost:8000/api/v1/user-answer/'
    response = requests.get(url, headers=headers)
    handle_response(response, "Ответы пользователя")

def handle_response(response, entity):
    if response.status_code in [200, 201]:
        print(f"{entity} успешно получены/созданы:", response.json())
    else:
        print(f"Ошибка при получении/создании {entity}:", response.status_code, response.text)

# Выполнение запросов
get_categories()
create_category()
get_subject_categories()
create_subject_category()
get_category_videos()
create_category_video()
get_videos()
create_video()
check_video_access(1)  # Замените 1 на реальный ID видео
# reset_video_tests(1)  # Замените 1 на реальный ID видео
get_test_content()
submit_answer(1, 'а')  # Замените 1 на реальный ID тестового контента и 'а' на ваш ответ
# reset_test(1)  # Замените 1 на реальный ID тестового контента
get_user_statistics()
get_user_answers()
