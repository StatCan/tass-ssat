import json
from ..log.logging import getLogger
from pathlib import Path
from .singleton import Singleton


log = getLogger(__name__)


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
        try:
            file = open(page, encoding='utf-8')
        except IOError as e:
            log.error("An IOError occured: %s" % e)
            return
        with file:
            self.page_dict[file_key] = json.load(file)
        return self.page_dict[file_key]

    def get_element(self, file_key,
                    page_key, element_key,
                    default=None, llist=[]):
        if [file_key, page_key] in llist:
            # If page has already been checked return None
            # Prevents possible infinite loops (a calls b calls a...)
            return None
        try:
            # llist is copied due to mutability.
            # In short changing llist directly affects all future calls as well
            _list = llist.copy()
            _list.append([file_key, page_key])
            page = self._page(file_key, page_key)
            if ('elements' in page
                    and element_key in page['elements']):

                element = page['elements'][element_key]
            elif ('inherits' in page):
                for f, p in page['inherits']:
                    element = self.get_element(f, p, element_key,
                                               default=default, llist=_list)
                    if element:
                        break

            # copy of element is returned to prevent
            # modifications to the element during run time
            return element.copy()

        except KeyError:
            print('One or more keys not found. Falling back to default')
        return default

    def get_url(self, file_key,
                page_key, url_key='url',
                default=None, llist=[]):
        if [file_key, page_key] in llist:
            # If page has already been checked return None
            # Prevents possible infinite loops (a calls b calls a...)
            return None
        try:
            # llist is copied due to mutability.
            # In short changing llist directly affects all future calls as well
            _list = llist.copy()
            _list.append([file_key, page_key])
            page = self._page(file_key, page_key)

            if url_key in page:
                return page[url_key]
            elif ('inherits' in page):
                for f, p in page['inherits']:
                    url = self.get_url(f, p, url_key,
                                       default=default, llist=_list)
                    if url:
                        return url

        except KeyError:
            print('One or more keys not found. Falling back to default')
        return default

    def get_page_title(self, file_key, page_key, default=None, llist=[]):
        if [file_key, page_key] in llist:
            # If page has already been checked return None
            # Prevents possible infinite loops (a calls b calls a...)
            return None
        try:
            # llist is copied due to mutability.
            # In short changing llist directly affects all future calls as well
            _list = llist.copy()
            _list.append([file_key, page_key])
            page = self._page(file_key, page_key)

            if 'title' in page:

                return page['title']

            elif ('inherits' in page):
                for f, p in page['inherits']:
                    title = self.get_page_title(f, p,
                                                default=default, llist=_list)
                    if title:
                        return title
        except KeyError:
            print('One or more keys not found. Falling back to default')
        return default

    def get_page_id(self, file_key, page_key, default=None, llist=[]):
        if [file_key, page_key] in llist:
            # If page has already been checked return None
            # Prevents possible infinite loops (a calls b calls a...)
            return None
        try:
            # llist is copied due to mutability.
            # In short changing llist directly affects all future calls as well
            _list = llist.copy()
            _list.append([file_key, page_key])
            page = self._page(file_key, page_key)

            if 'page_id' in page:
                page_id = page['page_id']

            elif ('inherits' in page):
                for f, p in page['inherits']:
                    page_id = self.get_page_id(f, p,
                                               default=default, llist=_list)
                    if page_id:
                        break

            # copy of page_id is returned to prevent
            # modifications to the page id during run time
            return page_id.copy()

        except KeyError:
            print('One or more keys not found. Falling back to default')
        return default

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
