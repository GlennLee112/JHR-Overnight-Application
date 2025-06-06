import os
import sys


def get_base_path():
    # Ref:
    # https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
    # https://stackoverflow.com/questions/66734987/absolute-path-of-exe-file-not-working-properly-in-python
    """Base path function condition gate to determine if file is running as script of as executable"""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    elif __file__:
        base_path = os.path.dirname(__file__)

    return base_path

