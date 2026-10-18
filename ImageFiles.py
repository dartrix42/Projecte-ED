import os

class ImageFiles:
    def __init__(self, path):
        self.imatges=[]
        for file in os.listdir(path):
            if file.lower().endswith(".png"):
                fullpath = os.path.join(path, file)
                self.imatges.append(fullpath)


    def get_files(self):
        return self.imatges

    def __len__(self):
        return len(self.imatges)

    def __str__(self):
        return str(self.imatges)