from utils.folder_processing import get_all_images
from utils.image_transform import combine_images_into_grid
from utils.serialize_image import ImageSerialize


def run():
    images = get_all_images()
    a4_images = combine_images_into_grid(images)
    for i, a4_image in enumerate(a4_images):
        ImageSerialize().output_image(
            a4_image, f"a4_image_{i}.png", "images/flash_cards_a4"
        )


if __name__ == "__main__":
    run()
