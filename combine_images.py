import math

import cv2
import numpy as np

from page_settings import adj_a4_h, adj_a4_w, adj_flash_card_h, adj_flash_card_w
from utils.folder_info import get_all_files_in_folder
from utils.serialize_image import ImageSerialize


def convert_to_rgb(image):
    if len(image.shape) == 2:  # Check if image is grayscale
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return image


def resize_image(image):
    image = convert_to_rgb(image)
    dim = (int(adj_flash_card_w), int(adj_flash_card_h))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


def add_border(image, border_size=1, border_color=(0, 0, 0)):
    b_s = border_size
    return cv2.copyMakeBorder(
        image, b_s, b_s, b_s, b_s, cv2.BORDER_CONSTANT, value=border_color
    )


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


def combine_images_into_grid(images, rows=4, cols=2):
    num_pages = math.ceil(len(images) / (rows * cols))
    a4_images = []
    for page_num in range(num_pages):
        # Calculate the start and end indices for the images on this page
        start_idx = page_num * rows * cols
        end_idx = min((page_num + 1) * rows * cols, len(images))

        # Create a white canvas for the A4-sized page

        canvas = 255 * np.ones((adj_a4_h, adj_a4_w, 3), dtype=np.uint8)

        for i, img_idx in enumerate(range(start_idx, end_idx)):
            image = add_border(images[img_idx])
            image = resize_image(image)

            # Calculate the position for each image on the page
            row = i // cols
            col = i % cols
            start_row = int(row * adj_flash_card_h)
            end_row = int(start_row + adj_flash_card_h)

            start_col = int(col * adj_flash_card_w)
            end_col = int(start_col + adj_flash_card_w)

            canvas[start_row:end_row, start_col:end_col, :] = image

        a4_images.append(canvas)

    return a4_images


def run():
    images = get_all_images()
    a4_images = combine_images_into_grid(images)
    ImageSerialize().output_image(a4_images[0], "test.png", "images/flash_cards_a4")


if __name__ == "__main__":
    run()
