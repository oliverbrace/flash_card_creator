from utils.create_cards import generate_pic_image
from utils.folder_processing import get_all_files_in_folder
from utils.serialize_image import ImageSerialize


def run():
    original_image_path = "images/picture_images"
    file_names = get_all_files_in_folder(original_image_path)
    contour_image_path = "images/contour_images"
    for file_name in file_names:
        original_image_s = ImageSerialize()
        original_image_s.load_file_image(file_name, original_image_path)
        pic_image = generate_pic_image(original_image_s.original_image, file_name)
        ImageSerialize().output_image(pic_image, file_name, contour_image_path)


if __name__ == "__main__":
    run()
