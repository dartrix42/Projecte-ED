import uuid
class ImageID:
    def __init__(self, image_files):
        self.ids = {}
        for file in image_files.get_files():
            new_id = str(uuid.uuid4())
            self.ids[new_id]=file

    def get_file(self, id):
        return self.ids.get(id)

    def get_ids(self):
        return list(self.ids.keys())

    def __len__(self):
        return len(self.ids)

    def __str__(self):
        return str(self.ids)