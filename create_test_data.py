"""
Скрипт для создания тестовых данных.
Запуск: python3 create_test_data.py
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_finder.settings')
django.setup()

from users.models import User  # noqa: E402
from projects.models import Project  # noqa: E402

users_data = [
    {
        'email': 'admin@example.com',
        'name': 'Иван',
        'surname': 'Петров',
        'password': 'admin123',
        'is_staff': True,
        'is_superuser': True,
        'about': 'Администратор платформы TeamFinder',
    },
    {
        'email': 'alice@example.com',
        'name': 'Алиса',
        'surname': 'Иванова',
        'password': 'password123',
        'about': 'Frontend-разработчик, люблю React и TypeScript',
        'github_url': 'https://github.com/alice',
        'phone': '+7 900 000 0001',
    },
    {
        'email': 'bob@example.com',
        'name': 'Борис',
        'surname': 'Сидоров',
        'password': 'password123',
        'about': 'Backend-разработчик на Python/Django',
        'github_url': 'https://github.com/bob',
    },
    {
        'email': 'carol@example.com',
        'name': 'Карина',
        'surname': 'Смирнова',
        'password': 'password123',
        'about': 'UX/UI дизайнер с опытом в Figma',
        'phone': '+7 900 000 0003',
    },
    {
        'email': 'dave@example.com',
        'name': 'Дмитрий',
        'surname': 'Козлов',
        'password': 'password123',
        'about': 'Fullstack-разработчик, интересуюсь ML',
    },
]

created_users = []
for data in users_data:
    is_staff = data.pop('is_staff', False)
    is_superuser = data.pop('is_superuser', False)
    password = data.pop('password')
    email = data['email']

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        print(f'Пользователь {email} уже существует')
    else:
        user = User.objects.create_user(password=password, **data)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        print(f'Создан пользователь: {email}')
    created_users.append(user)

projects_data = [
    {
        'owner': created_users[0],
        'name': 'Платформа для обучения программированию',
        'description': (
            'Образовательная платформа с интерактивными заданиями '
            'и проверкой кода в браузере.'
        ),
        'status': 'open',
    },
    {
        'owner': created_users[1],
        'name': 'Онлайн-магазин книг',
        'description': (
            'Разработка интернет-магазина с каталогом книг, корзиной и оплатой.'
        ),
        'status': 'open',
    },
    {
        'owner': created_users[1],
        'name': 'Трекер задач',
        'description': (
            'Простой и удобный Kanban-трекер задач для небольших команд.'
        ),
        'status': 'open',
    },
    {
        'owner': created_users[2],
        'name': 'Бот для Telegram',
        'description': (
            'Бот для напоминаний и планирования дел. Используем aiogram и PostgreSQL.'
        ),
        'status': 'open',
    },
    {
        'owner': created_users[2],
        'name': 'API для мобильного приложения',
        'description': (
            'REST API на Django REST Framework с авторизацией и push-уведомлениями.'
        ),
        'status': 'closed',
    },
    {
        'owner': created_users[3],
        'name': 'Дизайн-система',
        'description': (
            'Создание унифицированной дизайн-системы для веб-приложений.'
        ),
        'status': 'open',
    },
    {
        'owner': created_users[4],
        'name': 'ML-платформа для рекомендаций',
        'description': (
            'Платформа для построения рекомендательных систем с открытым кодом.'
        ),
        'status': 'open',
    },
    {
        'owner': created_users[4],
        'name': 'Агрегатор вакансий',
        'description': (
            'Парсер и агрегатор IT-вакансий с фильтрацией по стеку и зарплате.'
        ),
        'status': 'open',
    },
]

for data in projects_data:
    name = data['name']
    if Project.objects.filter(name=name).exists():
        print(f'Проект "{name}" уже существует')
        continue
    project = Project.objects.create(**data)
    print(f'Создан проект: {name}')

print('\nТестовые данные созданы!')
print('Логин администратора: admin@example.com / admin123')
print('Логин пользователей: alice@example.com, bob@example.com и др. / password123')
