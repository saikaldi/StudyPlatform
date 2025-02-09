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

# Примеры запросов:

# 1. Получить список всех платежных сервисов
def get_payment_services():
    url = 'http://localhost:8000/api/v1/payment-services/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Платежные сервисы:", response.json())
    else:
        print("Не удалось получить платежные сервисы:", response.status_code)

# 2. Создать новый платежный сервис
def create_payment_service():
    url = 'http://localhost:8000/api/v1/payment-services/'
    data = {
        'payment_service_name': 'Новый сервис оплаты',
        'prop_number': '1234567890',
        'full_name': 'Имя Владельца',
        'whatsapp_url': 'https://wa.me/1234567890'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("Платежный сервис создан:", response.json())
    else:
        print("Создание платежного сервиса не удалось:", response.status_code, response.text)

# 3. Получить список всех платежей
def get_payments():
    url = 'http://localhost:8000/api/v1/payments/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Платежи:", response.json())
    else:
        print("Не удалось получить платежи:", response.status_code)

# 4. Создать новый платеж
def create_payment():
    url = 'http://localhost:8000/api/v1/payments/'
    data = {
        'bank': 1,  # ID платежного сервиса
        'amount': '100.00',
        'phone_number': '+996700123456',
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("Платеж создан:", response.json())
    else:
        print("Создание платежа не удалось:", response.status_code, response.text)

# 5. Обновить статус платежа (для администраторов)
def update_payment_status():
    payment_id = 1  # ID платежа, статус которого нужно обновить
    url = f'http://localhost:8000/api/v1/payments/{payment_id}/update_status/'
    data = {
        'status': 'COMPLETED'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Статус платежа обновлен:", response.json())
    else:
        print("Обновление статуса платежа не удалось:", response.status_code, response.text)

# Выполнение запросов
get_payment_services()
create_payment_service()
get_payments()
create_payment()
update_payment_status()
