import os


def get_name(path: str) -> str:
    """Generate valid (not existed) filename from

    Args:
        path (str): file path

    Returns:
        str: full path not existed filename
    """
    if not os.path.exists(path):
        return path

    filename, extension = os.path.splitext(path)
    index = 1
    while True:
        new_name = f"{filename} ({index}){extension}"

        if not os.path.exists(new_name):
            return new_name
        else:
            index += 1
