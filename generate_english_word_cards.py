from utils.create_cards import create_english_text_image
from utils.serialize_image import ImageSerialize


def run():
    word = "Hello world"
    word_image = create_english_text_image(word)
    ImageSerialize().output_image(word_image, "test.png", "images/romanized_images")


if __name__ == "__main__":
    run()
