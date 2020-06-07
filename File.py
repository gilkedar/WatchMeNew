
import Helpers

class File:

    def __init__(self,path,mode = 'r'):

        self.path = path
        self.mode = mode
        self.fileName = Helpers.strip_filename_from_path(self.path)
        self.folder = Helpers.get_folder_of_path(self.path)
