import os


def get_all_files_in_folder(folder_path):
    file_paths = []
    files = os.listdir(folder_path)
    for file in files:
        file_paths.append(file)
    return file_paths
