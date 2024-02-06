import cv2
import numpy as np

from page_settings import adj_flash_card_h, adj_flash_card_w
from utils.serialize_image import ImageSerialize


def create_text_image(text, font_size=8, thickness=1, font=cv2.FONT_HERSHEY_TRIPLEX):
    # Need values to be whole numbers
    height = int(adj_flash_card_h * 4)
    width = int(adj_flash_card_w * 4)
    # Create a white image
    image = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Calculate the position to center the text
    text_size = cv2.getTextSize(text, font, font_size, thickness)[0]
    x = (width - text_size[0]) // 2
    y = (height + text_size[1]) // 2

    # Add text to the image
    cv2.putText(image, text, (x, y), font, font_size, (0, 0, 0), thickness)
    return image


def run():
    word = "Hello world"
    word_image = create_text_image(word)
    ImageSerialize().output_image(word_image, "test.png", "images/romanized_images")


if __name__ == "__main__":
    run()
