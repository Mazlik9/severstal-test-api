# Severstal Test API

REST API для управления задачами и пользователями.

## Стек

- Python 3.12, Django 5.2, Django REST Framework
    
- PostgreSQL 16
    
- MinIO (S3 совместимое хранилище для файлов)
    
- drf-spectacular для автоматической генерации OpenAPI/Swagger документации
    

---

## Установка и запуск (development)

1. Скопируйте `.env.example` в `.env` и заполните переменные окружения:
    

```bash
cp .env.example .env
```

2. Запустите Docker-контейнеры:
    

```bash
docker-compose -f docker-compose-local.yml up --build
```

- Сервисы внутри одной сети Docker:
    
    - `db` — PostgreSQL
        
    - `minio` — S3-хранилище
        
    - `backend` — Django проект
        

3. При первом запуске автоматически:
    
    - Генерируются JWT ключи (`private_key.pem`, `public_key.pem`)
        
    - Создаётся bucket в MinIO (публичный)
        
    - Выполняются миграции базы данных
        

---

## Окружения

В проекте используются три основных окружения:

|Окружение| Описание                                    | Настройки базы и MinIO                        |
|---|---------------------------------------------|-----------------------------------------------|
|`local`| Локальная разработка без Docker | DB: локальный Postgres, MinIO: через Docker   |
|`development`| Локальная разработка в Docker-сети          | DB: Postgres в Docker, Django, MinIO в Docker |
|`production`| Продакшн (заложена основа)                  | DB и MinIO на сервере                         |

Выбор окружения производится через переменную `.env`:

```env
ENVIRONMENT=development
```

Файл `.env.example` можно использовать как шаблон для всех окружений. В зависимости от `ENVIRONMENT` Django подхватывает соответствующий `settings` файл (`local.py`, `development.py`, `production.py`).

---

## JWT аутентификация

- Используется для всех защищённых эндпоинтов.
    
- Генерация ключей происходит автоматически при первом запуске (файлы `private_key.pem` и `public_key.pem` в корне проекта).
    
- В `.env` настраиваются ключи:
    

```env
JWT_PRIVATE_KEY=private_key.pem
JWT_PUBLIC_KEY=public_key.pem
```

- Для авторизации в API используйте Bearer Token в заголовке:
    

```
Authorization: Bearer <access_token>
```

---

## Документация API (Swagger / Redoc)

- Swagger UI доступен по URL:
    

```
http://localhost:8000/api/docs/
```

- Redoc UI доступен по URL:
    

```
http://localhost:8000/api/redoc/
```

- Для каждого эндпоинта автоматически сгенерирована документация с примерами запроса и ответов.
    

---

## Админка Django

- Доступна по URL:
    

```
http://localhost:8000/admin/
```

- Для создания суперпользователя:
    

```bash
docker-compose -f docker-compose-local.yml exec backend python manage.py createsuperuser
```

- После этого можно логиниться в админку и управлять пользователями и задачами.
    

---

## Тесты

- Для запуска тестов используйте:
    

```bash
docker-compose -f docker-compose-local.yml exec backend pytest --cov
```

- Покрытие тестами: **84%**.
    
- Тесты проверяют:
    
    - CRUD операции для задач
        
    - Модели User и Task
        
    - Проверку прав доступа
        

---

## Загрузка аватаров пользователей

- Эндпоинт: `PATCH /api/v1/user-self/avatar/`
    
- Формат запроса: `multipart/form-data` с полем `avatar` (файл до 5MB, форматы: jpeg, png, webp)
    
- Пример запроса через Swagger UI:
    

```json
{
  "avatar": "файл изображения"
}
```

- Старые аватары автоматически удаляются из S3 при обновлении.
    
Интерфес MinIO доступен по адресу
```
http://localhost:9001
```

---
