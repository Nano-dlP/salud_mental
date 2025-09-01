@echo off
REM Activar entorno virtual y correr servidor Django

cd ..
cd entornos\salud_mental\Scripts
call activate

cd ..\..\..\salud_mental
python manage.py runserver

pause
