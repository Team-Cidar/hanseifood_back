import os
import glob


def check_file_exists(path: str, file_name: str) -> bool:
    files: list = glob.glob(f"{path}/*")
    file_name = f"{path}/{file_name}"
    return file_name in files


def delete_file(file_path: str):
    os.system(f'rm {file_path}')
