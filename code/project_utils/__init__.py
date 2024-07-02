import os
import inspect
from typing import List


def get_caller_path() -> str:
    """
    Get the path of the script that called this function.

    Returns:
        str: The path of the script that called this function.
    """
    return os.path.abspath(inspect.stack()[-1].filename)


def set_working_dir() -> None:
    """
    Set the working directory to the directory of the script that called this function.
    """
    path = get_caller_path()
    path = os.path.dirname(path)
    os.chdir(path)


def get_script_name() -> str:
    """
    Get the name of the script that called this function without the extension.

    Returns:
        str: The name of the script that called this function without the extension.
    """
    return os.path.basename(get_caller_path().rsplit('.', 1)[0])


def get_list_from_config(line: str, dtype: type = str) -> List:
    """
    Get a list of values from a line in a config file.

    Args:
        line (str): Line from the config file.
        dtype (type): Data type of the values in the list.

    Returns:
        list: List of values of the specified data type.
    """
    return [dtype(x.strip()) for x in line.split(',')] 