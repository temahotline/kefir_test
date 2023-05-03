# Тестовое задание на вакансию Python разрабочика для компании "KEFIR"

[Cсылка на задание](https://drive.google.com/file/d/1JuEN0uybRdX1ynBuOI3scBdPMfiikot2/view)

Технологии: FastAPI, Python3.11, PostgreSQL, SQLAlchemy, Uvicorn, Pydantic, Pytest, Docker

## Инструкция по запуску

1. Клонируем репозиторий к сбе на компьютер
```
git clone git@github.com:temahotline/kefir_test.git
```
2. Переходим в директорию с проектом
```
cd <путь кпроекту>/kefir_test
```
3. Поднимаем Docker Compose
```
docker compose -f docker-compose-local.yaml up -d
```
4. Накатываем миграции 
```
docker-compose -f docker-compose-local.yaml exec app alembic upgrade heads
```
5. Создаем админа(по желанию)
```
docker-compose -f docker-compose-local.yaml exec app python scripts/create_admin.py
```
6. Переходим на документацию
```
http://0.0.0.0:8000/docs
```
