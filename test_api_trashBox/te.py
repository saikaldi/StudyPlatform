import requests

url = 'http://127.0.0.1:8000/api/v1/confirm-user/'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1MTYxNzE4LCJpYXQiOjE3MzUxNjE0MTgsImp0aSI6ImE2MTQ0ODgyMzI3YjQ1YWE5NzU3YWYxYjEzMTE0M2ZjIiwidXNlcl9pZCI6NX0.X4bxzFHb-9W0isHFnOWfwbdZj-JJb2udxiKyWSkXXPY',  # Если используется аутентификация через токен
}

data = {
    'email': 'aktanarynov567@gmail.com',
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print('Пользователь успешно подтвержден')
else:
    print(f'Ошибка: {response.status_code}, ')
