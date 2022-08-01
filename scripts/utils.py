import os


def get_name(path: str) -> str:
    """Menggenerate nama file yang valid di dalam suatu direktory agar tidak terjadi overwrite

    Args:
        path (str): file path

    Returns:
        str: full path dari nama file yang valid
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
