SHOOTER GAME

Простая игра написанная на Python.


## Требования
Python 3.12+
pyGame 2.6.1
pyInstaller 6.21.0 (опционально для пересборки проекта)


## Сборка
1. python -m venv .venv
2. pip install pygame pyinstaller
3. выполнить `pyinstaller -i ufo.ico -F -w .\shooter_game.py`
4. переместить бинарный файл `shooter_game.exe` или `shooter_game` из папки `dist` в корень проекта
5. запустить его

