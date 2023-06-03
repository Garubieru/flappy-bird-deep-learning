import os

os.system('python -m venv venv')
dirName = os.path.join(os.getcwd(), 'venv/bin/pip')
os.system(f'{dirName} install -r requirements.txt')
