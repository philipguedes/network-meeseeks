import os
import tempfile



class Graphs(object):
    def __init__(self):
        self.__file = None

    @property
    def path(self):
        return self.__file.name

    def create_tempfile(self):
        self.__file = tempfile.NamedTemporaryFile(delete=False)

    
        return 

    def __exit__(self, exc_type, exc_value, traceback):
        pass

def get_path():
    cwd = os.getcwd()
    folders = cwd.split(os.sep)
    
    folder = '' 
    while 