class SearchMetadata:
    def __init__(self, image_data):
        self.image_data = image_data

    def _ids(self):
        return self.image_data.get_ids()

    def generated(self, subcadena):
        needle = str(subcadena).casefold()
        return [uid for uid in self._ids()
                if needle in str(self.image_data.get_metadata(uid) or {}).casefold()]

    def dimensions(self, width, height):
        return [uid for uid in self._ids()
                if self.image_data.get_dimensions(uid) == (width, height)]

    def __str__(self):
        return f"SearchMetadata({len(self._ids())} imatges)"
