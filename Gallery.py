import json
import cfg


class Gallery:
    def __init__(self, image_id=None, image_viewer=None):
        self.image_id = image_id
        self.image_viewer = image_viewer
        self._name = ""
        self._description = ""
        self._created_date = ""
        self._uuids = []

    def load_file(self, filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = json.load(f)

            if isinstance(content, dict):
                self._name = content.get('gallery_name', '')
                self._description = content.get('description', '')
                self._created_date = content.get('created_date', '')

                self._uuids = []
                for item in content.get('images', []):
                    if self.image_id and hasattr(self.image_id, 'get_uuid'):
                        resolved = self.image_id.get_uuid(item)
                        self._uuids.append(resolved if resolved is not None else item)
                    else:
                        self._uuids.append(item)
            elif isinstance(content, list):
                self._uuids = content
        except Exception as err:
            print(f"Error carregant la galeria: {err}")

    def load_from_json(self, filepath: str):
        self.load_file(filepath)

    def show(self):
        for uid in self._uuids:
            if self.image_viewer:
                if hasattr(self.image_viewer, 'show'):
                    self.image_viewer.show(uid)
                elif hasattr(self.image_viewer, 'show_image'):
                    self.image_viewer.show_image(uid)

    def add_image_at_end(self, uuid_str: str):
        if uuid_str and uuid_str not in self._uuids:
            self._uuids.append(uuid_str)

    def remove_first_image(self):
        if self._uuids:
            self._uuids.pop(0)

    def remove_last_image(self):
        if self._uuids:
            self._uuids.pop()

    def get_ids(self) -> list:
        return self._uuids

    def __len__(self):
        return len(self._uuids)

    def __str__(self):
        return f"Gallery '{self._name}' ({len(self._uuids)} imatges)"