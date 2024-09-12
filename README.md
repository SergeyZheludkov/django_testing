# Django testing  

## Описание
Тесты для двух проектов:
 - сайт с новостями и комментариями (тесты на Pytest)
 - сайт-блокнот (тесты на Unittest)

## Используемые технологии:

- Django 3.2
- Pytest
- Unittest

В проекте используется Python 3.9

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SergeyZheludkov/django_testing.git
```

```
cd django_testing
```

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv venv
```

```
source venv/bin/activate
```

Установить пакетный менеджер и зависимости из файла requirements.txt:

```
pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в папку ya_note и запустить unittest, указав уровень детализации:

```
cd ya_note
```

```
python manage.py test -v 3
```

Перейти в папку ya_news и запустить pytest:

```
cd ../ya_news
```

```
pytest
```

Можно запустить оба теста из корня проекта:

```
bash run_tests.sh
```

В корень проекта нужно поместить файл .env с содержимым SECRET_KEY= секретный ключ Django
____

**Сергей Желудков** 

Github: [@SergeyZheludkov](https://github.com/SergeyZheludkov/)