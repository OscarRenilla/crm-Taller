@echo off
REM Arranque en 1 comando (Windows): doble clic o  iniciar.bat
if not exist venv py -m venv venv
call venv\Scripts\activate
pip install -q -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py cargar_ejemplo
echo Abre http://127.0.0.1:8000/  usuario: admin  clave: admin1234
py manage.py runserver
