import logging

import cv2


def canny_edge_detection(image, blur=7, threshold1=40, threshold2=100):
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        logging.warning("Image may already be grey so skipping step")

    image = cv2.GaussianBlur(image, (blur, blur), 0)
    return cv2.Canny(image=image, threshold1=threshold1, threshold2=threshold2)


def invert_black_white(image):
    return cv2.bitwise_not(image)
