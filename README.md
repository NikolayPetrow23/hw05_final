# yatube

## Описание
Проект представляет собой платформу, которая позволяет пользователям создавать и публиковать свои посты. 
Он предоставляет удобный интерфейс и функциональность для написания, редактирования и публикации постов.

## Основной функционал
1. Регистрация и аутентификация: Пользователи могут создать учетную запись и войти на платформу с помощью своих учетных
данных. Это обеспечивает безопасность и позволяет управлять доступом к функциональности.

2. Создание и редактирование постов: Пользователи могут создавать новые посты, указывая заголовок, содержание и, при 
необходимости, добавлять изображения, видео или другие медиафайлы. Они также могут редактировать или удалять свои 
существующие посты.

3. Публикация и отображение постов: Посты, созданные пользователями, могут быть опубликованы и отображены
на платформе. Пользователи смогут просматривать посты других пользователей, а также оставлять комментарии и отмечать 
их понравившимися.

4. Категории и теги: Для удобной навигации и классификации постов, платформа может поддерживать категории и теги. 
Пользователи могут выбирать соответствующую категорию и добавлять теги к своим постам, что поможет другим 
пользователям находить интересующий контент.
5. 
## Технологии

```
Python 3.9
Django 2.2.16
HTML
CSS
Bootstrap
pytest 6.2.4
```

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:NikolayPetrow23/hw05_final.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv

python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Автор

```
Николай Петров
```

