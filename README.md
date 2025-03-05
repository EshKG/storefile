# Сервис хранения файлов

## Используемые технологии:
- **Python 3.9 и выше** (uWSGI или FastAPI)
- **PostgreSQL**
- **Docker**

---

## Быстрый старт

### 1. Клонирование репозитория
Склонируйте репозиторий на свой компьютер:
```sh
git clone https://github.com/EshKG/storefile.git
```

Все дальнейшие команды выполняются из директории **storefile**.

---

### 2. Структура репозитория
В репозитории находятся:
- **app/** — исходный код приложения  
- **container/** — готовый контейнер  
- **Dockerfile** — инструкции для сборки образа FastAPI  
- **requirements.txt** — зависимости Python  

Файл `main.py` содержит комментарии с примерами API-запросов.

---

### 3. Сборка и запуск контейнеров

#### 3.1 Создание Docker-образа для сервера FastAPI
```sh
docker build -t image_1 .
```

#### 3.2 Запуск контейнеров  

##### 1) Сервер FastAPI:
```sh
docker run --name server -p 80:80 -v volume_1:/files -it image_1
```

##### 2) База данных PostgreSQL:
```sh
docker run --name postgresql -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgresql \
  -e POSTGRES_USER=postgresql \
  -e POSTGRES_DB=storefile_db \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v volume_1:/var/lib/postgresql/data \
  -d postgres
```

---

### 4. Создание таблицы в базе данных
После запуска контейнера базы данных необходимо создать таблицу хранения параметров файлов.  

Можно выполнить SQL-запрос через DBeaver или psql:
```sql
CREATE TABLE storefile_db.public.file_storage (
  id SERIAL PRIMARY KEY,
  "UUID" VARCHAR,
  "FILENAME" VARCHAR,
  "UPLOAD_DATE" VARCHAR
);
```

---

### 5. Доступ к API
После запуска сервер доступен по адресу:  
📌 **http://localhost/docs** (Swagger UI)

---

### 6. Управление контейнерами

#### Запуск контейнеров:
```sh
docker start server
docker start postgresql
```

#### Остановка контейнеров:
```sh
docker stop server
docker stop postgresql
```

---

## Подключение к базе данных
- **IP:** `localhost`  
- **Порт:** `5432`  
