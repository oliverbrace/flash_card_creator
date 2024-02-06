import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from page_settings import adj_flash_card_h, adj_flash_card_w
from utils.serialize_image import ImageSerialize


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def create_text_image(text, font_size=400, font=cv2.FONT_HERSHEY_TRIPLEX):
    # Need values to be whole numbers
    image_height = int(adj_flash_card_h * 4)
    image_width = int(adj_flash_card_w * 4)
    # Create a white image
    image = np.ones((image_height, image_width, 3), dtype=np.uint8) * 255

    # Convert the image to RGB (OpenCV uses BGR)
    cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Pass the image to PIL
    pil_im = Image.fromarray(cv2_im_rgb)
    draw = ImageDraw.Draw(pil_im)
    # use a truetype font
    font = ImageFont.truetype("MSMINCHO.ttf", font_size)

    # Get the text size
    text_width, text_height = textsize(text, font)

    if text_width > image_width:
        text = text.replace(" ", "\n")
        text_width, text_height = textsize(text, font)
        if text_width > image_width:
            raise Exception("Word is too long. Get back to coding monkey")

    # Calculate the position to center the text
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2

    # Draw the text
    draw.text((x, y), text, font=font, align="center", fill=(0, 0, 0))

    # Get back the image to OpenCV
    return cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)


def read_image_paths_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        # Read lines from the file and remove leading/trailing whitespaces
        image_paths = [line.strip() for line in file.readlines()]
    return image_paths


def run():
    japanese_words_path = "words/japanese_words.txt"
    words = read_image_paths_from_file(japanese_words_path)
    for word in words:
        japanese_word, english_word = word.split(":")
        word_image = create_text_image(japanese_word)
        ImageSerialize().output_image(
            word_image, f"{english_word}_j.png", "images/katakana_images"
        )


if __name__ == "__main__":
    run()
