import os

def load_modules():
    for item in os.listdir(os.path.dirname(__file__)):
        filename, ext = os.path.splitext(item)
        if ext != '.py':
            continue
        if filename == '__init__':
            continue
        __import__('snakepit.lib.modules.' + filename)