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

    def _page(self, file_key, page_key):
        if self.pages_loaded(file_key):
            return self.page_dict[file_key][page_key]
        else:
            return self._load_pages(file_key)[page_key]

    def _load_pages(self, file_key):
        file_name = file_key + '.json'
        page = self._page_root.resolve() / file_name
        with open(page, encoding='utf-8') as file:
            self.page_dict[file_key] = json.load(file)
        return self.page_dict[file_key]

    def get_element(self, file_key, page_key, element_key, default=None):
        try:
            return self._page(
                            file_key,
                            page_key)['elements'].get(
                                            element_key,
                                            default)
        except KeyError:
            print('One or more keys not found. Falling back to default')
            return default

    def get_url(self, file_key, page_key, default=None):
        try:
            return self._page(file_key, page_key).get('url', default)
        except KeyError:
            print('One or more keys not found. Falling back to default')
            return default

    def get_page_title(self, file_key, page_key, default=None):
        try:
            return self._page(file_key, page_key).get('title', default)
        except KeyError:
            print('One or more keys not found. Falling back to default')
            return default

    def get_page_id(self, file_key, page_key):
        return self._page(file_key, page_key).get('page_id', None)

    def pages_loaded(self, key):
        return key in self.page_dict

    def is_empty(self):
        return bool(self.page_dict)

    def add_page(self, page_key, page):
        custom_key = 'custom'
        if (not self.pages_loaded(custom_key)):
            self.page_dict[custom_key] = {}
        p = self.page_dict[custom_key]
        p[page_key] = page
