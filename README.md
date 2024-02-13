### Тестовое задание.Разработать сервис хранения файлов с использование:
### 
### Python3.9 и выше (uwsgi или FastAPI)
### PosgreSQL
### Docker


## Порядок действий для быстрого старта с тем что есть :
#### Клонируем репозиторий на свой компьютер:
 ```https://github.com/EshKG/storefile.git```
#### В репозитории содержится папка "app", папка "container" с готовым контейнером,Dockerfile,requirements.txt. В файле main.py в комментариях выведены подробные команды для работы API. 
#### В файле Dockerfile содержиться информация для сборки образа FastAPI
#### В файле requirements.txt содержаться необходимые библиотеки для сборки образа


#### Создаем образ image_1 из Dockerfile для сервера FastAPI
```docker build -t image_1 .```
 
#### Выполняем команды для создания контейнера сервера FastAPI(название контейнера server) и базы данных(название контейнера postgresql). Подключаем для обоих контейнеров один том с названием volume_1: 
##### 1) Для сервера fastapi:

```docker run --name server -p 80:80 -v volume_1:/files -it image_1``` 


##### 2) Для базы данных:

```docker run --name postgresql -p 5432:5432 -e POSTGRES_PASSWORD=postgresql -e POSTGRES_USER=postgresql -e POSTGRES_DB=storefile_db  -e PGDATA=/var/lib/postgresql/data/pgdata -v volume_1:/var/lib/postgresql/data -d postgres``` 

##### Теперь API доступен по адресу http://localhost/docs, а контейнеры можно запускать и отключать командами:
```docker start server ```

```docker start postgresql```


```docker stop server```

```docker stop postgresql```
##### БД ip: localhost port: 5432
