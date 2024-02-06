import cv2

from page_settings import card_ratio


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
