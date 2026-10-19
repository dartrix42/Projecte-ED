from PIL import Image
class ImageViewer:
    def __init__(self, image_data):
        self.image_data = image_data

    def show(self, uuid):
        path = self.image_data.get_filename(uuid)
        if path is not None:
            try:
                img = Image.open(path)
                img.show()
                return img
            except Exception:
                return None
        return None

    def __str__(self):
        return str(self.image_data)

    def __len__(self):
        return len(self.image_data)