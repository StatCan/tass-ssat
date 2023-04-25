import json
from pathlib import Path
from tass.core.singleton import Singleton

class PageReader(metaclass=Singleton):
    def __init__(self):
        self.page_dict = {}

        # Make the pages directory if it doesn't exist.
        # TODO: Move to "Install" script?
        self._page_root = Path('pages')
        self._page_root.mkdir(exist_ok=True)

    def load_pages(self, file_key):
        # TODO: read pages from file
        file_name = file_key + '.json'
        page = self._page_root.resolve() / file_name
        with open(page, encoding='utf-8') as file:
            self.page_dict[file_key] = json.load(file)
        return self.page_dict[file_key]

    def get_element(self, file_key, page_key, element_key):
        # TODO: return the locator object from the page
        if self.pages_loaded(file_key):
            return self.page_dict[file_key][page_key][element_key]
        else:
            return self.load_pages(file_key)[page_key][element_key]

    def pages_loaded(self, key):
        return key in self.page_dict

    def is_empty(self):
        return bool(self.page_dict)
