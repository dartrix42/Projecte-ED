import uuid
import cfg

class ImageID:
    def __init__(self, image_files=None):
        self._path_to_uuid = {}
        self._uuid_to_path = {}

        if isinstance(image_files, dict):
            self._path_to_uuid = dict(image_files)
            self._uuid_to_path = {v: k for k, v in self._path_to_uuid.items()}
        elif image_files is not None:
            file_list = []
            if hasattr(image_files, 'get_files'):
                file_list = image_files.get_files()
            elif isinstance(image_files, (list, tuple, set)):
                file_list = list(image_files)

            for path in file_list:
                self.generate_uuid(path)

    def generate_uuid(self, file_path: str) -> str:
        if file_path in self._path_to_uuid:
            return self._path_to_uuid[file_path]

        generated = None
        if hasattr(cfg, 'get_uuid'):
            try:
                generated = str(cfg.get_uuid(file_path))
            except Exception:
                generated = str(uuid.uuid4())
        else:
            generated = str(uuid.uuid4())
        while generated in self._uuid_to_path:
            generated = str(uuid.uuid4())

        self._path_to_uuid[file_path] = generated
        self._uuid_to_path[generated] = file_path
        return generated

    def get_uuid(self, file_path: str) -> str:
        return self._path_to_uuid.get(file_path)

    def get_file(self, uuid_str: str) -> str:
        return self._uuid_to_path.get(uuid_str)

    def get_ids(self) -> list:
        return list(self._uuid_to_path.keys())

    def remove_uuid(self, uuid_str: str):
        file_path = self._uuid_to_path.pop(uuid_str, None)
        if file_path:
            self._path_to_uuid.pop(file_path, None)

    def __len__(self):
        return len(self._path_to_uuid)

    def __str__(self):
        return str(self._path_to_uuid)