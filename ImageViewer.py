# -*- coding: utf-8 -*-
import os
import cfg
from PIL import Image


class ImageViewer:
    def __init__(self, image_data):
        self._image_data = image_data

    @property
    def image_data(self):
        return self._image_data

    def print_image(self, uuid_str: str):
        if uuid_str not in getattr(self._image_data, 'data', {}):
            print('ERROR: UUID not found.')
            return

        dims = self._image_data.get_dimensions(uuid_str)
        if dims:
            print(' Dimensions:', f"{dims[0]}x{dims[1]}")

        prompt = self._image_data.get_prompt(uuid_str)
        if prompt and len(prompt) > 50:
            prompt = prompt[:47] + "..."

        print(' Prompt:', prompt)
        print(' Model:', self._image_data.get_model(uuid_str))
        print(' Seed:', self._image_data.get_seed(uuid_str))
        print(' CFG Scale:', self._image_data.get_cfg_scale(uuid_str))
        print(' Steps:', self._image_data.get_steps(uuid_str))
        print(' Sampler:', self._image_data.get_sampler(uuid_str))
        print(' Generated:', self._image_data.get_generated(uuid_str))
        print(' Created Date:', self._image_data.get_created_date(uuid_str))
        print(' UUID:', uuid_str)

        filename = self._image_data.get_filename(uuid_str)
        if filename:
            path = filename
            if hasattr(cfg, 'get_root'):
                try:
                    path = os.path.realpath(os.path.join(cfg.get_root(), filename))
                except Exception:
                    pass
            print(' Path del arxiu:', path)

    def show_file(self, filepath: str):
        if not os.path.isfile(filepath):
            print('ERROR: The file does not exist.')
            return

        if getattr(cfg, 'DISPLAY_MODE', 0) > 0:
            try:
                img = Image.open(filepath)
                img.show()
            except Exception:
                print('ERROR: Cannot show file')

    def show_image(self, uuid_str: str, mode=None):
        if uuid_str not in getattr(self._image_data, 'data', {}):
            print('ERROR: UUID not found.')
            return None

        if mode is None:
            mode = getattr(cfg, 'DISPLAY_MODE', 0)

        filename = self._image_data.get_filename(uuid_str)
        path = filename
        if hasattr(cfg, 'get_root'):
            try:
                path = os.path.realpath(os.path.join(cfg.get_root(), filename))
            except Exception:
                pass

        if mode == 0:
            self.print_image(uuid_str)
            return None
        elif mode in (1, 2):
            if mode == 1:
                self.print_image(uuid_str)
            try:
                img = Image.open(path)
                if mode > 0:
                    img.show()
                return img
            except Exception:
                print('ERROR: Cannot show the image')
                return None
        return None

    def show(self, uuid_str: str, mode=None):
        return self.show_image(uuid_str, mode)

    def __len__(self):
        return len(getattr(self._image_data, 'data', {}))

    def __str__(self):
        return f"ImageViewer amb {len(self)} imatges"