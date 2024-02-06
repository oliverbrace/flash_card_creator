import math

import cv2
import numpy as np

from page_settings import (
    adj_a4_h,
    adj_a4_w,
    adj_flash_card_h,
    adj_flash_card_w,
    card_ratio,
)
from utils.image_preprocessing import convert_to_rgb


def change_ratio(image, target_ratio=card_ratio):
    # Get the current height and width
    height, width = image.shape[:2]

    # Calculate the target width based on the desired ratio
    target_width = int(height * target_ratio)
    border_width = abs(target_width - width) // 2
    border_color = [255, 255, 255]

    if target_width > width:
        return cv2.copyMakeBorder(
            image,
            0,
            0,
            border_width,
            border_width,
            cv2.BORDER_CONSTANT,
            value=border_color,
        )
    else:
        start_col = (width - target_width) // 2
        end_col = start_col + target_width
        return image[:, start_col:end_col]


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


def add_subtext_to_image(image, text, thickness=1, font=cv2.FONT_HERSHEY_TRIPLEX):
    text_color = (255, 255, 255)
    border_color = (0, 0, 0)
    height, width = image.shape[:2]
    font_size = height / 400
    text_size = cv2.getTextSize(text, font, font_size, thickness)[0]
    text_width = (width - text_size[0]) // 2
    text_height = text_size[1]
    position = (int(text_width), int(height - text_height * (1.1)))
    cv2.putText(
        image, text, position, font, font_size, border_color, thickness + 2, cv2.LINE_AA
    )
    cv2.putText(
        image, text, position, font, font_size, text_color, thickness, cv2.LINE_AA
    )
