class FileIO:
    def __init__(self, file_name):
        self.__file_name = file_name

    def read(self):
        with open(self.__file_name) as f:
            content = f.read()
        return content
