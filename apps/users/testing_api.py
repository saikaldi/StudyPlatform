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

# 1. Регистрация пользователя
def register_user():
    url = 'http://localhost:8000/api/v1/sign-up/'
    data = {
        'email': 'test_user@example.com',
        'password': 'securepassword123',
        'password_confirm': 'securepassword123',
        'user_status': 'Студент',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'paid': 'Не оплачено'
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Регистрация успешна:", response.json())
    else:
        print("Ошибка регистрации:", response.status_code, response.text)

# 2. Подтверждение регистрации
def confirm_registration():
    url = 'http://localhost:8000/api/v1/sign-up-confirmation/'
    data = {
        'email': 'test_user@example.com',
        'code': '123456'  # Это должен быть реальный код, который был отправлен на почту
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Регистрация подтверждена:", response.json())
    else:
        print("Ошибка подтверждения регистрации:", response.status_code, response.text)

# 3. Вход в систему
def login_user():
    url = 'http://localhost:8000/api/v1/sign-in/'
    data = {
        'email': 'test_user@example.com',
        'password': 'securepassword123'
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Вход успешен:", response.json())
    else:
        print("Ошибка входа:", response.status_code, response.text)

# 4. Запрос на сброс пароля
def request_password_reset():
    url = 'http://localhost:8000/api/v1/request-password-reset/'
    data = {
        'email': 'test_user@example.com'
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Запрос на сброс пароля отправлен:", response.json())
    else:
        print("Ошибка при запросе сброса пароля:", response.status_code, response.text)

# 5. Сброс пароля
def reset_password():
    uidb64 = 'encoded_user_id'  # Замените на реальный uidb64
    token = 'secure_token'  # Замените на реальный токен
    url = f'http://localhost:8000/api/v1/reset-password/{uidb64}/{token}/'
    data = {
        'new_password': 'newpassword123',
        'new_password_confirm': 'newpassword123'
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Пароль успешно сброшен:", response.json())
    else:
        print("Ошибка при сбросе пароля:", response.status_code, response.text)

# 6. Получение профиля пользователя
def get_user_profile():
    url = 'http://localhost:8000/api/v1/account/profile/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Профиль пользователя:", response.json())
    else:
        print("Ошибка получения профиля:", response.status_code, response.text)

# 7. Подтверждение пользователя администратором (требуется токен администратора)
def confirm_user_by_admin():
    url = 'http://localhost:8000/api/v1/confirm-user-status-priveligion/'
    data = {
        'email': 'test_user@example.com'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Пользователь подтвержден:", response.json())
    else:
        print("Ошибка подтверждения пользователя:", response.status_code, response.text)

# Выполнение запросов
register_user()
confirm_registration()
login_user()
request_password_reset()
# reset_password() - требуется реальный uidb64 и token
get_user_profile()
confirm_user_by_admin()
