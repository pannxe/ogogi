def read(filename):
    if not os.path.exists(filename):
        return ""
    f = codecs.open(filename, "r", "utf-8")
    d = f.read()
    f.close()
    return d.replace("\r", "")


def write(filename, data):
    f = codecs.open(filename, "w", "utf-8")
    f.write(data.replace("\r", ""))
    f.close()