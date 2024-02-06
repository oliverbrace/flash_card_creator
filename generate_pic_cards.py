import cv2

from page_settings import adj_flash_card_h, adj_flash_card_w
from utils.folder_info import get_all_files_in_folder
from utils.image_preprocessing import canny_edge_detection, invert_black_white
from utils.image_transform import change_ratio
from utils.serialize_image import ImageSerialize


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


def run():
    original_image_path = "images/picture_images"
    contour_image_path = "images/contour_images"
    file_names = get_all_files_in_folder(original_image_path)
    for file_name in file_names:
        original_image_s = ImageSerialize()
        original_image_s.load_file_image(file_name, original_image_path)

        cropped_image = change_ratio(original_image_s.original_image)
        contoured_image = canny_edge_detection(cropped_image)
        inverted_contoured_image = invert_black_white(contoured_image)

        _, width = inverted_contoured_image.shape[:2]
        card_width = adj_flash_card_w * 8
        card_height = adj_flash_card_h * 8
        if card_width < width:
            inverted_contoured_image = cv2.resize(
                inverted_contoured_image,
                (int(card_width), int(card_height)),
            )

        add_subtext_to_image(inverted_contoured_image, file_name)
        ImageSerialize().output_image(
            inverted_contoured_image, file_name, contour_image_path
        )


if __name__ == "__main__":
    run()
