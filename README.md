# API YaMDb

[![CI](https://github.com/IlyaVasilevsky47/foodgram-project-react/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/IlyaVasilevsky47/foodgram-project-react/actions/workflows/main.yml)

API YaMDb - это программный интерфейс, предназначенный для социальной сети, которая позволяет пользователям оставлять отзывы на различные произведения.

## Возможности:
– Произведения классифицируются по категориям, таким как «Книги», «Фильмы», «Музыка», и могут быть отнесены к жанрам из списка доступных. Добавлять произведения, категории и жанры имеет право только администратор.
– На сайте пользователи могут оставлять текстовые отзывы и оценивать произведения в диапазоне от 1 до 10. На основе пользовательских оценок вычисляется средняя оценка произведения. Пользователь может оставить только один отзыв на одно произведение. Добавлять отзывы, комментарии и оценивать произведения могут только аутентифицированные пользователи.

## Запуск проекта:
1. Клонируем проект.
```bash
git clone
```
2. Создаем и активируем виртуальное окружение. 
```bash
python -m venv venv
source venv/scripts/activate
```
3. Обновляем менеджер пакетов pip и устанавливаем зависимости из файла requirements.txt.
```bash
python -m pip install --upgrade pip
pip install -r api_yamdb/requirements.txt
```
4. Переходим в папку и создаем базу данных. 
```bash
cd api_yamdb
python manage.py migrate 
```
5. Загружаем тестовые данные в базу данных.
```bash
python manage.py database_import
```
6. Запускаем проект.
```bash
python manage.py runserver 
```

## Запуск через контейнеры:
1. Переходим в папку и создаем файл.
```bash
cd infra
touch .env
```
2. Заходим в файл.
```bash
nano .env
```
3. Заполняем файл.
```conf
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
4. Запускаем контейнеры.
```bash
docker-compose up -d
```
5. Создаем базу данных.
```bash
docker-compose exec web python manage.py migrate
```
6. Заполняем тестовыми данными базу данных.
```bash
docker-compose exec web python manage.py database_import
```
7. Собираем всю статику.
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

## Документация:
После запуска сервера локально, заходим в ReDoc по ссылке:
```url
http://127.0.0.1:8000/redoc/
```
Если вы запустили сервер в контейнерах, то вам нужно перейти по этой ссылке:
```url
http://localhost/redoc/
```

## Авторы:
| Имя | GitHub |
| - | :-: |
| Илья Василевсикй | <a href="https://github.com/IlyaVasilevsky47" target="_blank"> :heavy_check_mark:</a> |
| Игорь Белошицкий | <a href="https://github.com/IgorBelosh" target="_blank"> :heavy_check_mark:</a> |
| Ангелина Тингаева | <a href="https://github.com/Angelina91" target="_blank"> :heavy_check_mark:</a> |

## Технический стек
- Python 3.7.9
- Django 3.2.16
- Django REST Framework 3.12.4
  - Simple JWT 4.8.0
- PyJWT 2.1.0
