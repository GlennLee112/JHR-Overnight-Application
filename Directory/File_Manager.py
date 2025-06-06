import os
from pathlib import Path
import inspect
import sys


def Create_Make_Return_Dir(base_path, path_list=[], parents=True, exist_ok=True):
    # joining file path from list
    # https://stackoverflow.com/questions/33299248/join-elements-of-a-list-into-a-path
    file_path = os.path.join(base_path, *path_list)
    Path(file_path).mkdir(parents=parents, exist_ok=exist_ok)

    return file_path


def variable_name_extract(variable):
    """"Simple function to extract variable name"""
    # Ref: # https://www.geeksforgeeks.org/how-to-print-a-variables-name-in-python/
    current_frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(current_frame)[1]
    local_vars = caller_frame.frame.f_locals

    for name, value in local_vars.items():
        if value is variable:
            return name


def get_file_paths(directory):
    """"Function to return all file path inside a given folder"""
    # Ref:
    # https://stackoverflow.com/questions/9816816/get-absolute-paths-of-all-files-in-a-directory
    path = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            full = os.path.abspath(os.path.join(dirpath, f))
            path.append(full)

    return path


def test_path(path):
    # Ref:
    # https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions?page=1&tab=scoredesc#tab-top
    test_path_result = os.path.isfile(path)

    return test_path_result


def file_dir_create(path):
    # Test if variable provided is list; if not convert string or provided file to list
    if not isinstance(path, list):
        path = [path]
    #  Loop through file list and create directory if doesn't exist
    for p in path:
        if not os.path.exists(p):
            os.makedirs(p)
        else:
            continue


def get_base_path():
    # Ref:
    # https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
    # https://stackoverflow.com/questions/66734987/absolute-path-of-exe-file-not-working-properly-in-python
    # modified to be used as module import
    """Base path function condition gate to determine if file is running as script of as executable"""
    # Old:
    # if getattr(sys, 'frozen', False):
    #     path_return = os.path.dirname(sys.executable)
    # elif __file__:
    #     path_return = os.path.dirname(__file__)
    #
    # return path_return

    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)  # get apps location
    else:
        return os.path.dirname(os.path.abspath(sys.argv[0]))
        # invoke absolute path (i.e.: the apps that call in the function)
