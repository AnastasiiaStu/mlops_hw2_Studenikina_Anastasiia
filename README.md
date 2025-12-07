# Домашнее задание 2. Реализация /health и /predict эндпоинтов в gRPC-сервисе

**Выполнила**: Студеникина Анастасия Александровна

Выполняла в основном в bash строке

## 1) Создание папок:

mkdir ml_grpc_service

mkdir ml_grpc_service/protos, ml_grpc_service/server,
ml_grpc_service/client, ml_grpc_service/models,
ml_grpc_service/generated

cd ml_grpc_service

## 2) Загрузка файлов в папки

Отдельно создала файлы, за основу брала код с лекций и семинаров 3 и 4
(в папке приложены, здесь не дублирую): model.proto, requirements.txt,
train_model.py, server.py, client.py, Dockerfile, .dockerignore

## 3) Устанавливались зависимости

py -m pip install -r requirements.txt

py -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/model.proto

## 4) Обучение модели

py train_model.py

## 5) Проводим тест в том же терминале 

python -m server.server

## 6) Запустила докер, открыла второй терминал в папке с проектом:

docker ps

docker build -t grpc-ml-service .

python -m client.client

## 7) Создаем новый репозиторий на своем аккаунте Git, копируем HTTPS ключ

## 8) Добавление всех файлов, папок в Git – тут последовательность действий как на прошлом HW
