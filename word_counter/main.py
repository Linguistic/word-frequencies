import sys

from os import path, mkdir
from word_counter.counter import WordCounter


os_languages = [
    "af",
    "ar",
    "bg",
    "bn",
    "br",
    "bs",
    "ca",
    "cs",
    "da",
    "de",
    "el",
    "en",
    "eo",
    "es",
    "et",
    "eu",
    "fa",
    "fi",
    "fr",
    "gl",
    "he",
    "hi",
    "hr",
    "hu",
    "hy",
    "id",
    "is",
    "it",
    "ja",
    "ka",
    "kk",
    "ko",
    "lt",
    "lv",
    "mk",
    "ml",
    "ms",
    "nl",
    "no",
    "pl",
    "pt",
    "pt_br",
    "ro",
    "ru",
    "si",
    "sk",
    "sl",
    "sq",
    "sr",
    "sv",
    "ta",
    "te",
    "th",
    "tl",
    "tr",
    "uk",
    "ur",
    "vi",
    "ze_en",
    "ze_zh",
    "zh_cn",
    "zh_tw",
]


def process_language(language: str):
    print("\nProcessing language: " + language + "...\n")
    WordCounter(language).run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_language(sys.argv[1])
    else:
        for lang in os_languages:
            process_language(lang)
