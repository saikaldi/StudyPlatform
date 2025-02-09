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

import requests
import json

# Предполагается, что `headers` уже определены и содержат токен аутентификации

# 1. TestCategory
def create_test_category():
    url = 'http://localhost:8000/api/v1/testcategories/'
    data = {'test_category_name': 'Новая категория теста'}
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Категория теста")

# 2. SubjectCategory
def create_subject_category():
    url = 'http://localhost:8000/api/v1/subjectcategories/'
    data = {'subject_category_name': 'Новая категория предмета'}
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Категория предмета")

# 3. Test
def create_test():
    url = 'http://localhost:8000/api/v1/tests/'
    data = {
        'test_category_id': 1,
        'subject_category_id': 1,
        'title': 'Новый тест',
        'description': 'Описание нового теста'
    }
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Тест")

# 4. TestContent
def create_test_content():
    url = 'http://localhost:8000/api/v1/TestContent/'
    data = {
        'test_id': 1,
        'question_text': 'Новый вопрос',
        'true_answer': 'а'
    }
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Контент теста")

# 5. TestFullDescription
def create_test_full_description():
    url = 'http://localhost:8000/api/v1/testfulldescriptions/'
    data = {
        'test_id': 1,
        'description_title': 'Описание теста',
        'description_image': 'path/to/image.jpg'
    }
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Полное описание теста")

# 6. TestInstruction
def create_test_instruction():
    url = 'http://localhost:8000/api/v1/test-instruction/'
    data = {
        'test_id': 1,
        'instruction_title': 'Инструкция теста',
        'instruction_image': 'path/to/instruction.jpg'
    }
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Инструкция теста")

# 7. UserAnswer
def create_user_answer():
    url = 'http://localhost:8000/api/v1/useranswers/'
    data = {
        'test_content_id': 1,
        'answer_vars': 'а'
    }
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Ответ пользователя")

# 8. UserStatistic
def create_user_statistic():
    url = 'http://localhost:8000/api/v1/userstatistics/'
    data = {
        'test_id': 1,
        'true_answer_count': 1,
        'false_answer_count': 0
    }
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Статистика пользователя")

# 9. OkupTushunuu
def create_okup_tushunuu():
    url = 'http://localhost:8000/api/v1/okup-tushunuu/'
    data = {
        'name': 'Новый тест Окуп тушунуу',
        'description': 'Описание нового теста'
    }
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Окуп тушунуу")

# 10. OkupTushunuuText
def create_okup_tushunuu_text():
    url = 'http://localhost:8000/api/v1/okup-tushunuu-text/'
    data = {
        'test_id': 1,
        'title': 'Новый текст',
        'text1': 'path/to/text1.jpg'
    }
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Текст Окуп тушунуу")

# 11. OkupTushunuuQuestion
def create_okup_tushunuu_question():
    url = 'http://localhost:8000/api/v1/okup-tushunuu-questions/'
    data = {
        'okup_tushunuu_id': 1,
        'question': 1,
        'question_text': 'Новый вопрос',
        'var_A_text': 'Ответ А',
        'true_answer': 'а'
    }
    response = requests.post(url, json=data, headers=headers)
    handle_response(response, "Вопрос Окуп тушунуу")

def handle_response(response, entity):
    if response.status_code == 201:
        print(f"{entity} создан успешно:", response.json())
    else:
        print(f"Создание {entity} не удалось:", response.status_code, response.text)

# Выполнение запросов
create_test_category()
create_subject_category()
create_test()
create_test_content()
create_test_full_description()
create_test_instruction()
create_user_answer()
create_user_statistic()
create_okup_tushunuu()
create_okup_tushunuu_text()
create_okup_tushunuu_question()
