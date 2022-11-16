Описание проекта:
    В проекте представлена социальная сеть Yatube с возможностью
создавать публикациии и делиться ими с другими пользователя. Польза огромная!

-----------------------------------------------------------------------------------

Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
git clone https://github.com/Senkdar/api_final_yatube
cd api_final_yatube

Cоздать и активировать виртуальное окружение:
python -m venv venv
source venv/Scripts/activate

Установить зависимости из файла requirements.txt:
python -m pip install --upgrade pip
pip install -r requirements.txt

Выполнить миграции:
python manage.py migrate

Запустить проект:
python manage.py runserver

-----------------------------------------------------------------------------------


