import os

currentPath = os.getcwd()
pythonPath = os.path.join(currentPath, 'venv/bin/python3')
os.system(f'{pythonPath} {currentPath}/src/main.py')
