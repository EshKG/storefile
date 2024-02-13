from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse
import psycopg2
import psycopg2.extras
from datetime import datetime, date
from pathlib import Path
import pathlib
import uuid

app = FastAPI()

def check_db(uuid='',filename='',date=''):
    """
    Функция check_db возвращает список словарей,которые содержат параметры файлов, которые имеются на диске

    """

#Создаем первоначальный словарь с названиями ключей идентичных названием колонок в таблице,в качестве значений будут переменные полученные из аргументов функции
#Это нужно для того, чтобы создать корректное условие для запроса данных в бд
    dict_1 = {"UUID": uuid, "FILENAME": filename, "UPLOAD_DATE": date} 
#Создаем второй словарь, в котором исключаем ключи с пустыми значениями, смысла от них для поиска в бд нет
    dict_2 = {}
    for k,v in dict_1.items():
       if(v!= ''):
          dict_2[k] = v

#подключение к бд
    conn = psycopg2.connect(database="storefile_db", user="postgresql", password="postgresql", host="172.17.0.1", port=5432)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#query переменная содержащая запрос в бд  для получение списка файлов
    query = """
                  SELECT * FROM public.file_storage WHERE 1=1 
             """

#Выделяем дополнительные условия для добавления к query из словаря dict_2 
    for k,v in dict_2.items():
        query = query + ' AND "{}" like '.format(k) + "'" + v + "'"


    cur.execute(query)

#data хранит данные,полученные из бд
    data = cur.fetchall()

#list_rows -это список,который после преобразования переменной data будет хранить словари с параметрами файлов
    list_rows = []

#заполнение list_rows
    for d in range(len(data)):
#        print(dict(data[d]))
        list_rows.append(dict(data[d]))

    return  list_rows


@app.get("/")
def read_root():
    return {"API FOR TEST"}


@app.get("/v1/find")
def file(UUID='', filename='', date=''):
    """
    Возвращает список файлов, по заданным параметрам, использует функцию  check_db для получения данных
    """
    result = check_db(UUID, filename, date)
#    print("result = ",result)
    return result

@app.get("/v1/download")
def download(UUID: str):
#Присвоение переменной result стандартного ответа, в случае, если не будет данных для скачивания
    result='{"response": "ERROR 404"}'
#Инициализация подключение к бд
    conn = psycopg2.connect(database="storefile_db", user="postgresql", password="postgresql", host="172.17.0.1", port=5432)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    query = """
                  SELECT "FILENAME" FROM public.file_storage WHERE "UUID"='{}'
             """.format(str(UUID))
    cur.execute(query)
    data = cur.fetchone()

#В случае если в базе данных есть файл с заданным UUID из параметра запроса, то скачивается файл из директории тома
    return FileResponse(path='/files/' + data[0], filename=data[0], media_type="multipart/form-data")

@app.post("/v2/upload")
async def upload(file: UploadFile = File(...)):
#Генерация уникального uuid по названию файла и сохранение в переменную UUID
    UUID =  uuid.uuid5(uuid.NAMESPACE_DNS,file.filename)
#location - переменная, содержащая путь к файлу на диске, который будет после записи
    location = "/files/" + file.filename

#Запись или перезапись файла на диск
    with open(location, "wb") as file_record:
        file_record.write(file.file.read())

#Переменная UPLOAD_DATE включает сегодняшнюю дату в формате Y-m-d
    UPLOAD_DATE = date.today().strftime('%Y-%m-%d')

#FILENAME хранит имя файла
    FILENAME = file.filename

#Если нет записи в бд о таком файле, то добавляем запись,в противном случае не записываем 
    if(len(check_db(str(UUID)))==0):
        conn = psycopg2.connect(database="storefile_db", user="postgresql", password="postgresql", host="172.17.0.1", port=5432)

        cur = conn.cursor()

        query = 'INSERT INTO public.file_storage ("UUID", "FILENAME", "UPLOAD_DATE") VALUES ({}, {}, {})'.format("'" + str(UUID) + "'", "'" + FILENAME + "'", "'" + UPLOAD_DATE + "'")

        cur.execute(query)

        conn.commit()


    return {"UUID": UUID}

