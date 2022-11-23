# Yatube API
В проекте представлен API к социальной сети Yatube.

## Как запустить проект (для Windows):
Клонировать репозиторий и перейти в него в командной строке:

```bash
  git clone https://github.com/Senkdar/API_YaTube
  
  cd API_YaTube
```
 
Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv

source Venv/Scripts/activate

```
Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python manage.py migrate
```
Запустить проект:
```bash
python manage.py runserver   
```

