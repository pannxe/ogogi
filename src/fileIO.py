import codecs
import os
import abb


def read(path):
    if os.path.exists(path):
        with codecs.open(path, "r", "utf-8") as f:
            return f.read().replace("\r", "")
    print(abb.error + path + " not found.")
    return ""


def write(path, data):
    with codecs.open(path, "w", "utf-8") as f:
        f.write(data.replace("\r", ""))
