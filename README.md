# Благотворительный фонд поддержки котиков QRKot

## Описание проекта

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

### Запуск проекта 

1. Создание виртуального окружения и его запуск
   ```
   python3 -m venv venv
   ```
   ```
   source /venv/bin/activate
   ```
2. Установка зависимостей
   ```
   pip install -r requirements.txt
   ```
3. Создать .env файл в корне проекта по примеру:
   ```
    DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
    SECRET=your_secret
    FIRST_SUPERUSER_EMAIL=user@example.com
    FIRST_SUPERUSER_PASSWORD=your_password
   ```
4. Выполнить миграции  
    ```
    alembic revision -m 'Final project'
    ```
5. Применить миграции
    ```
    alembic upgrade head
    ```
6. Запустить сервер
    ```
    uvicorn app.main:app --reload
    ```

### Список доступных эндпоинтов и документация
    http://127.0.0.1:8000/docs

### Использованный стек
1. Alembic
2. FastAPI
3. FastAPI Users
4. SQLAlchemy

### Автор @slavdosya