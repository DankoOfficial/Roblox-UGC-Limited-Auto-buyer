@echo off
echo Proceed with installation if you don't have Python and Pip installed.
winget install pip
pip install requests
echo Running main.py
python3 main.py
