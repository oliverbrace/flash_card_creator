import cv2
import numpy as np
from PIL import Image, ImageDraw


def num_channels_check(img):
    return img.ndim


def get_image_size(image):
    """_summary_

    Args:
        image (_type_): _description_

    Returns:
        _type_: height, width
    """
    image_shape = image.shape
    return image_shape[0], image_shape[1]


def get_pixel_count(image):
    height, width = get_image_size(image)
    return height * width


def mean_squared_error(img1, img2):
    h, w, _ = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err / (float(h * w))
    return mse


def percentage_black_pixels(image):
    """_summary_

    Args:
        image (_type_):
    """
    return percentage_colour_pixels(image, 0)


def percentage_white_pixels(image):
    """_summary_

    Args:
        image (_type_):
    """
    return percentage_colour_pixels(image, 255)


def percentage_colour_pixels(image, colour):
    """_summary_

    Args:
        image (_type_): image
        colour (int): _description_

    Returns:
        _type_: _description_
    """
    return np.sum(image == colour) / get_pixel_count(image)


def text_size(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height
