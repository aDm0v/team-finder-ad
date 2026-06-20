# TeamFinder

Платформа для поиска участников в IT-проекты.

## Автор

kanef1 — [github.com/kanef1](https://github.com/kanef1)

## Технологический стек

- Python 3 / Django 5.2
- PostgreSQL 16
- Docker / Docker Compose
- Pillow

---

## Быстрый старт

**1. Склонируйте репозиторий и перейдите в папку проекта:**

```bash
git clone https://github.com/kanef1/team-finder-ad.git
cd team-finder-ad
```

**2. Создайте виртуальное окружение и установите зависимости:**

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**3. Создайте `.env` на основе примера:**

```bash
cp .env_example .env
```

Файл `.env` уже содержит настройки для запуска. При необходимости отредактируйте параметры БД.

**4. Запустите базу данных через Docker Compose:**

```bash
docker compose up -d
```

Postgres запустится на порту 5436 (задано в `.env`).

**5. Примените миграции:**

```bash
python3 manage.py migrate
```

**6. Загрузите тестовые данные:**

```bash
python3 create_test_data.py
```

Создаются 5 пользователей и 8 проектов.

**7. Запустите сервер разработки:**

```bash
python3 manage.py runserver
```

Сайт доступен по адресу: [http://localhost:8000](http://localhost:8000)

Панель администратора: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Тестовые аккаунты

| Роль            | Email                  | Пароль      |
|-----------------|------------------------|-------------|
| Администратор   | admin@example.com      | admin123    |
| Пользователь 1  | alice@example.com      | password123 |
| Пользователь 2  | bob@example.com        | password123 |
| Пользователь 3  | carol@example.com      | password123 |
| Пользователь 4  | dave@example.com       | password123 |

---

## Вариант задания

Реализован **Вариант 1**: «Избранное» и фильтрация пользователей.

---

## Структура проекта

- `users/` — приложение для управления пользователями (регистрация, вход, профиль)
- `projects/` — приложение для управления проектами (создание, избранное, участие)
- `templates_var1/` — HTML-шаблоны
- `static/` — CSS, JS, изображения
- `docker-compose.yml` — конфигурация PostgreSQL

---

## Зависимости

Все зависимости перечислены в `requirements.txt`. Для работы необходим Docker.
