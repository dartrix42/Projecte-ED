import os
import cfg
from PIL import Image

class ImageData:
    def __init__(self, image_id=None):
        self._store = {}  # {uuid: {'file': path, 'metadata': dict}}

        if image_id is not None:
            if hasattr(image_id, 'get_ids'):
                for uid in image_id.get_ids():
                    filepath = image_id.get_file(uid)
                    if filepath:
                        self.add_image(uid, filepath)

    def add_image(self, uuid_str: str, filename: str):
        if uuid_str and filename:
            self._store[uuid_str] = {'file': filename, 'metadata': {}}
            self.load_metadata(uuid_str)

    def remove_image(self, uuid_str: str):
        self._store.pop(uuid_str, None)

    def load_metadata(self, uuid_str: str):
        if uuid_str not in self._store:
            return

        filename = self._store[uuid_str]['file']
        full_path = filename
        if hasattr(cfg, 'get_root'):
            try:
                root = cfg.get_root()
                if root and not os.path.isabs(filename):
                    full_path = os.path.join(root, filename)
            except Exception:
                pass

        try:
            meta = cfg.read_png_metadata(full_path)
            self._store[uuid_str]['metadata'] = meta if isinstance(meta, dict) else {}
        except Exception:
            self._store[uuid_str]['metadata'] = {}

    def _get_field(self, uuid_str: str, possible_keys: list):
        if uuid_str not in self._store:
            return None
        metadata = self._store[uuid_str].get('metadata', {})
        for key in possible_keys:
            if key in metadata:
                return metadata[key]
        return None

    def get_prompt(self, uuid_str: str):
        return self._get_field(uuid_str, ['Prompt', 'prompt'])

    def get_model(self, uuid_str: str):
        return self._get_field(uuid_str, ['Model', 'model'])

    def get_seed(self, uuid_str: str):
        return self._get_field(uuid_str, ['Seed', 'seed'])

    def get_cfg_scale(self, uuid_str: str):
        return self._get_field(uuid_str, ['CFG Scale', 'CFG_Scale', 'cfg_scale'])

    def get_steps(self, uuid_str: str):
        return self._get_field(uuid_str, ['Steps', 'steps'])

    def get_sampler(self, uuid_str: str):
        return self._get_field(uuid_str, ['Sampler', 'sampler'])

    def get_generated(self, uuid_str: str):
        return self._get_field(uuid_str, ['Generated', 'generated', 'Sub', 'sub'])

    def get_created_date(self, uuid_str: str):
        return self._get_field(uuid_str, ['Created Date', 'Created_Date', 'created_date'])

    def get_filename(self, uuid_str: str):
        if uuid_str in self._store:
            return self._store[uuid_str].get('file')
        return None

    def get_file(self, uuid_str: str):
        return self.get_filename(uuid_str)

    def get_dimensions(self, uuid_str: str):
        if uuid_str not in self._store:
            return None
        filename = self._store[uuid_str]['file']
        full_path = filename
        if hasattr(cfg, 'get_root'):
            try:
                root = cfg.get_root()
                if root and not os.path.isabs(filename):
                    full_path = os.path.join(root, filename)
            except Exception:
                pass
        try:
            with Image.open(full_path) as img:
                return img.size
        except Exception:
            return None

    @property
    def data(self):
        return self._store

    def __len__(self):
        return len(self._store)

    def __str__(self):
        return f"ImageData ({len(self)} imatges)"