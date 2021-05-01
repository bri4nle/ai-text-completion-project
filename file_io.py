class FileIO:
    """
    This class provides file IO
    """
    def __init__(self, file_name):
        self.content = ''
        self.__file_name = file_name

    def read(self):
        """
        This function read the file input file and return its content
        :return:
        """
        with open(self.__file_name, encoding='utf8', mode="r") as f:
            self.content += f.read()
        return self.content
