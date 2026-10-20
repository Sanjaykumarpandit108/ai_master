


import os


def log(text):
    if os.getenv("DEBUG") == "True":
        print(f" \033[91m{text}\033[0m")
