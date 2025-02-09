import requests

base_url = "http://localhost:8000/api/v1"
video_id = 1  # Замените на нужный ID видео
endpoint = f"{base_url}/videos/{video_id}/reset_test/"

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2NTM4MDU1LCJpYXQiOjE3MzY0NTE2NTUsImp0aSI6IjE1YjU2YjI2OTQwYTQ3NzJhYjJhYWU5MzgwZjE4MTNlIiwidXNlcl9pZCI6MX0.-gcu01bG4ZIbS8-d_C_1pJ8djhpKxWy2fiaHhW-0Kt4'

headers = {
    "Authorization": f"Bearer {token}"  # Замените на токен пользователя
}

response = requests.post(endpoint, headers=headers)

if response.status_code == 200:
    print("Тест сброшен. Вы можете пройти его снова.")
else:
    print(f"Ошибка: {response.status_code} - {response.json()}")
