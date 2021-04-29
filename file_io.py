class FileIO:
    def __init__(self, file_name):
        self.content = ''
        self.__file_name = file_name

    def read(self):
        with open(self.__file_name, encoding='utf8', mode="r") as f:
            self.content += f.read()
        return self.content
