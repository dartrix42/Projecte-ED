class SearchMetadata:
    def __init__(self, image_data):
        self._image_data = image_data
        if hasattr(image_data, 'data'):
            self._dataset = image_data.data
        elif isinstance(image_data, dict):
            self._dataset = image_data
        else:
            self._dataset = {}

    def _filter_by_key(self, field_name: str, substring: str) -> list:
        results = []
        sub_lower = str(substring).lower()

        for uid, record in self._dataset.items():
            value = None
            getter = f"get_{field_name.lower()}"
            if hasattr(self._image_data, getter):
                value = getattr(self._image_data, getter)(uid)
            elif isinstance(record, dict) and 'metadata' in record:
                for k, v in record['metadata'].items():
                    if k.lower().replace(' ', '_') == field_name.lower():
                        value = v
                        break

            if value is not None and sub_lower in str(value).lower():
                results.append(uid)

        return results

    def prompt(self, sub: str) -> list:
        return self._filter_by_key('prompt', sub)

    def model(self, sub: str) -> list:
        return self._filter_by_key('model', sub)

    def seed(self, sub: str) -> list:
        return self._filter_by_key('seed', sub)

    def cfg_scale(self, sub: str) -> list:
        return self._filter_by_key('cfg_scale', sub)

    def steps(self, sub: str) -> list:
        return self._filter_by_key('steps', sub)

    def sampler(self, sub: str) -> list:
        return self._filter_by_key('sampler', sub)

    def date(self, sub: str) -> list:
        return self._filter_by_key('created_date', sub)

    def generated(self, sub: str) -> list:
        return self._filter_by_key('generated', sub)

    def dimensions(self, width: int, height: int) -> list:
        matches = []
        target = (width, height)
        for uid in self._dataset.keys():
            if hasattr(self._image_data, 'get_dimensions'):
                if self._image_data.get_dimensions(uid) == target:
                    matches.append(uid)
        return matches

    def and_operator(self, list1: list, list2: list) -> list:
        return list(set(list1) & set(list2))

    def or_operator(self, list1: list, list2: list) -> list:
        return list(set(list1) | set(list2))

    def __len__(self):
        return len(self._dataset)

    def __str__(self):
        return str(self._dataset)