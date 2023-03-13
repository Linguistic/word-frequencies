from os import mkdir, path
from string import punctuation


punc = (
    "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
    + punctuation
)


def is_alpha(word: str):
    return any(not c.isdigit() and c not in punc for c in word)


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
