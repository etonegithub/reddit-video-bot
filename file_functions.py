import os
import shutil
import pathlib


def is_dir_empty(dir_path: str) -> bool:
    if os.path.isdir(dir_path):
        if not os.listdir(dir_path):
            return True
        else:
            return False
    else:
        print('Failed to check {path}. Reason: {err}'.format(path=dir_path, err="Given directory does not exist"))
        return False


def is_dir_empty_of_files(dir_path: str) -> bool:
    if os.path.isdir(dir_path):
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                return False
        return True
    else:
        print('Failed to check {path}. Reason: {err}'.format(path=dir_path, err="Given directory does not exist"))


def clear_dir(dir_path: str, clear_dirs: bool) -> bool:
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                if clear_dirs:
                    shutil.rmtree(file_path)
                else:
                    clear_dir(file_path, clear_dirs)
        except Exception as e:
            print('Failed to delete {path}. Reason: {err}'.format(path=file_path, err=e))
            return False
    return True


def delete_file_by_name(file_name: str, dir_path: str) -> bool:
    file_path = os.path.join(dir_path, file_name)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
            return True
        else:
            print('Failed to delete file at {path}. Reason: {err}'.format(path=file_path, err="Not a file or link"))
            return False
    except Exception as e:
        print('Failed to delete file at {path}. Reason: {err}'.format(path=file_path, err=e))
        return False


def delete_dir_by_name(dir_path: str) -> bool:
    try:
        if os.path.isdir(dir_path):
            os.rmdir(dir_path)
            return True
        else:
            print('Failed to delete directory at {path}. Reason: {err}'.format(path=dir_path, err="Not a directory"))
            return False
    except Exception as e:
        print('Failed to delete directory at {path}. Reason: {err}'.format(path=dir_path, err=e))
        return False


def create_dir(dir_parent_path: str, dir_name: str) -> bool:
    dir_path = os.path.join(dir_parent_path, dir_name)
    try:
        pathlib.Path(dir_path).mkdir()
        return True
    except Exception as e:
        print('Failed to create directory at {path}. Reason: {err}'.format(path=dir_path, err=e))
        return False
