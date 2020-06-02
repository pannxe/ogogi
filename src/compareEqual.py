import fileIO


def compareEqual(path_1, path_2):
    cleaned_1 = fileIO.read(path_1).strip()
    cleaned_2 = fileIO.read(path_2).strip()

    lines_1 = [line.rstrip() for line in cleaned_1.splitlines()]
    lines_2 = [line.rstrip() for line in cleaned_2.splitlines()]

    return lines_1 == lines_2
