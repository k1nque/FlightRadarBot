import os

if os.path.isfile('secret.py'):
    from secret import token as TOKEN
else:
    TOKEN = os.getenv('TOKEN')

eps = 0.5  # deg
distance = 300  # m
