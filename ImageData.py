from PIL import Image
import cfg

class ImageData:
    def __init__(self, imageid):
        self.id = imageid
        self.metadata={}
        self.dimensions = {}

        for uuid in self.id.get_ids():
            path = self.id.get_file(uuid)
            if path:
                try:
                    self.metadata[uuid] = cfg.read_png_metadata(path)
                except Exception:
                    self.metadata[uuid] = {}

                try:
                    with Image.open(path) as img:
                        self.dimensions[uuid] = img.size
                except Exception:
                    self.dimensions[uuid] = (0,0)


    def get_filename(self, uuid):
        return self.id.get_file(uuid)

    def get_dimensions(self, uuid):
        return self.dimensions.get(uuid)

    def __len__(self):
        return len(self.dimensions)

    def __str__(self):
        return str(self.dimensions)