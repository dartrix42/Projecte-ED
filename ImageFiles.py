import os
import cfg

class ImageFiles:
    def __init__(self, path=None):
        self._prev_files = set()
        self._current_files = set()
        if path:
            self.reload_fs(path)

    def reload_fs(self, path: str):
        """Re-explora el directori i actualitza l'estat dels fitxers PNG."""
        self._prev_files = set(self._current_files)
        self._current_files = set()

        if path and os.path.exists(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith('.png'):
                        abs_path = os.path.abspath(os.path.join(root, file))
                        self._current_files.add(abs_path)

    def files_added(self) -> list:
        """Fitxers que s'han afegit des de l'última cerca."""
        return list(self._current_files - self._prev_files)

    def files_removed(self) -> list:
        """Fitxers que s'han esborrat des de l'última cerca."""
        return list(self._prev_files - self._current_files)

    def get_files(self) -> list:
        """Retorna la llista ordenada de rutes de fitxers PNG trobats."""
        return sorted(list(self._current_files))

    def __len__(self):
        return len(self._current_files)

    def __str__(self):
        return "\n".join(sorted(self._current_files))