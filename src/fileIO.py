import codecs
import os


def read(filename: os.path) -> str:
    if not os.path.exists(filename):
        raise FileNotFoundError
    with codecs.open(filename, "r", "utf-8") as f:
        return f.read().replace("\r", "")


def write(filename: os.path, data: str):
    with codecs.open(filename, "w", "utf-8") as f:
        f.write(data.replace("\r", ""))
