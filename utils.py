import os


def get_name(path):
    filename, extension = os.path.splitext(path)

    if not os.path.isfile(path):
        return path
    else:
        index = 1
        while True:
            new_name = f"{filename} ({index}){extension}"

            if not os.path.isfile(new_name):
                return new_name
            else:
                index += 1


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
