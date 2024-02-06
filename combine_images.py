from utils.folder_processing import get_all_images
from utils.image_transform import combine_images_into_grid
from utils.serialize_image import ImageSerialize


def run():
    images = get_all_images()
    a4_images = combine_images_into_grid(images)
    ImageSerialize().output_image(a4_images[0], "test.png", "images/flash_cards_a4")


if __name__ == "__main__":
    run()
