import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from page_settings import adj_flash_card_h, adj_flash_card_w
from utils.image_analysis import text_size
from utils.image_preprocessing import canny_edge_detection, invert_black_white
from utils.image_transform import add_subtext_to_image, change_ratio


def create_english_text_image(
    text, font_size=8, thickness=1, font=cv2.FONT_HERSHEY_TRIPLEX
):
    # Create a white image
    image = np.ones((adj_flash_card_h, adj_flash_card_w, 3), dtype=np.uint8) * 255

    # Calculate the position to center the text
    text_size = cv2.getTextSize(text, font, font_size, thickness)[0]
    x = (adj_flash_card_w - text_size[0]) // 2
    y = (adj_flash_card_h + text_size[1]) // 2

    # Add text to the image
    cv2.putText(image, text, (x, y), font, font_size, (0, 0, 0), thickness)
    return image


def create_japanese_text_image(text, font_size=100, font=cv2.FONT_HERSHEY_TRIPLEX):
    # Create a white image
    image = np.ones((adj_flash_card_h, adj_flash_card_w, 3), dtype=np.uint8) * 255

    # Convert the image to RGB (OpenCV uses BGR)
    cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Pass the image to PIL
    pil_im = Image.fromarray(cv2_im_rgb)
    draw = ImageDraw.Draw(pil_im)
    # use a truetype font
    font = ImageFont.truetype("MSMINCHO.ttf", font_size)

    # Get the text size
    text_width, text_height = text_size(text, font)

    if text_width > adj_flash_card_w:
        text = text.replace(" ", "\n")
        text_width, text_height = text_size(text, font)
        if text_width > adj_flash_card_w:
            raise Exception("Word is too long. Get back to coding monkey")

    # Calculate the position to center the text
    x = (adj_flash_card_w - text_width) // 2
    y = (adj_flash_card_h - text_height) // 2

    # Draw the text
    draw.text((x, y), text, font=font, align="center", fill=(0, 0, 0))

    # Get back the image to OpenCV
    return cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)


def generate_pic_image(image, text):
    cropped_image = change_ratio(image)
    contoured_image = canny_edge_detection(cropped_image)
    inverted_contoured_image = invert_black_white(contoured_image)

    _, width = inverted_contoured_image.shape[:2]
    card_width = adj_flash_card_w
    card_height = adj_flash_card_h
    if card_width < width:
        inverted_contoured_image = cv2.resize(
            inverted_contoured_image, (card_width, card_height)
        )

    add_subtext_to_image(inverted_contoured_image, text)
    return inverted_contoured_image
