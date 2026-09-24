## Описание pet-проекта:
Данный pet-проект создавался для закрепления навыков работы с микрофрейморком Flask, PostgreSQL (psycopg), абстракцией работы с БД.

## Минимальные требования:
- Python 3.13+
- uv 0.11.7+
- Flask 3.1.3+
- psycopg 3.3.6+ 

## Инструкция по установке и запуску:
**Установка проекта**
```bash
git clone git@github.com:Ainur2006/my-project-flask.git
cd my-project-flask
uv tool install .
```
## Настройка окружения

Сгенерируйте SECRET_KEY:
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

Создайте .env и укажите параметры подключения к БД и SECRET_KEY:

```bash
DATABASE_URL=postgresql://[user]:[password]@localhost:5432/my_project
SECRET_KEY=...
```

## Подготовка БД

1. Создайте базу данных через psql
```bash
psql -U postgres -c "CREATE DATABASE my_project;"
```
2. Применить схему (schema.sql)
```bash
psql -d my_project -f schema.sql
```
3. Загрузите данные 


## Запуск
```bash
make start
```