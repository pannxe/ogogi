def compareEqual(path_1, path_2):
    with open(path_1) as f1, open(path_2) as f2:
        while True:
            f1_line = f1.readline()
            f2_line = f2.readline()
            if f1_line == "" and f2_line == "":
                return True
            if f1_line.rstrip() != f2_line.rstrip():
                return False