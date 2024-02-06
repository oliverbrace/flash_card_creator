from utils.create_cards import create_japanese_text_image
from utils.folder_processing import get_all_japanese_words
from utils.serialize_image import ImageSerialize


def run():
    words = get_all_japanese_words()
    for word in words:
        japanese_word, english_word = word.split(":")
        word_image = create_japanese_text_image(japanese_word)
        ImageSerialize().output_image(
            word_image, f"{english_word}_j.png", "images/katakana_images"
        )


if __name__ == "__main__":
    run()
