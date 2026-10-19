import json


class Gallery:
   
    def __init__(self, image_id, image_viewer):
        self.image_id = image_id
        self.image_viewer = image_viewer
        self.images = []

    def add(self, uuid):
        uid = str(uuid)
        if self.image_id.get_file(uid) is None:
            return False
        if uid not in self.images:
            self.images.append(uid)
        return True

    def remove(self, uuid):
        uid = str(uuid)
        if uid not in self.images:
            return False
        self.images.remove(uid)
        return True

    def get_ids(self):
        return list(self.images)

    def load_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = data['images']
        if not isinstance(data, list):
            raise ValueError('La galeria JSON ha de contenir una llista')
        self.images = []
        for uid in data:
            self.add(uid)
        return self.get_ids()

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({'images': self.images}, f)

    def from_search(self, search):
        self.images = []
        for uid in search:
            self.add(uid)
        return self.get_ids()

    def show(self):
        return [self.image_viewer.show(uid) for uid in self.images]

    def __len__(self):
        return len(self.images)

    def __str__(self):
        return str(self.images)
