from os import mkdir, path
from string import punctuation
from unicodedata import category


punc = (
    "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
    + punctuation
)

# https://en.wikipedia.org/wiki/Unicode_character_property#General_Category
printable_prefixes = [
    "L",
    "M",
    "N",
    "P",
]


def is_printable(word: str):
    return all(
        not c.isdigit() and c not in punc and category(c)[0] in printable_prefixes
        for c in word
    )


def get_temp_dir():
    dir = ".tmp"
    if not path.exists(dir):
        mkdir(dir)
    return dir


def get_out_dir():
    dir = "data"
    if not path.exists(dir):
        mkdir(dir)
    return dir
