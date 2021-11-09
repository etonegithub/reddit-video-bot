import os, shutil


def is_dir_empty(dir_path):
    if os.path.isdir(dir_path):
        if not os.listdir(dir_path):
            return True
        else:
            return False
    else:
        print("Given directory does not exist.")
        return False


def clear_dir(dir_path):
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason %s' % (file_path, e))
