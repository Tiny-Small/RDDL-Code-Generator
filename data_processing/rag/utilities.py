import os

def check_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
