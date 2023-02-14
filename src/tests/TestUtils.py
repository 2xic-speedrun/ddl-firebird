import os

def get_full_path(path):
    return os.path.join(
        os.path.dirname(__file__),
        path,
    )
