import os

from utils.serialize_image import ImageSerialize


def get_all_files_in_folder(folder_path):
    file_paths = []
    files = os.listdir(folder_path)
    for file in files:
        file_paths.append(file)
    return file_paths


def get_all_images():
    japanese_images_path = "images/katakana_images"
    contour_image_path = "images/contour_images"
    japanese_file_names = get_all_files_in_folder(japanese_images_path)
    contour_file_names = get_all_files_in_folder(contour_image_path)
    images = []
    for j_file_name in japanese_file_names:
        i_s = ImageSerialize()
        i_s.load_file_image(j_file_name, japanese_images_path)
        images.append(i_s.original_image)
    for c_file_name in contour_file_names:
        i_s = ImageSerialize()
        i_s.load_file_image(c_file_name, contour_image_path)
        images.append(i_s.original_image)

    return images


def read_image_paths_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        # Read lines from the file and remove leading/trailing whitespaces
        image_paths = [line.strip() for line in file.readlines()]
    return image_paths


def get_all_japanese_words():
    japanese_words_path = "words/japanese_words.txt"
    return read_image_paths_from_file(japanese_words_path)
