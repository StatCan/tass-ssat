import json
from ..log.logging import getLogger
from pathlib import Path
from .singleton import Singleton


log = getLogger(__name__)


class PageReader(metaclass=Singleton):
    def __init__(self):
        self._page_dict = {}

        # Make the pages directory if it doesn't exist.
        # TODO: Move to "Install" script?
        self._page_root = Path('pages')
        self._page_root.mkdir(exist_ok=True)

    def _page(self, file_key, page_key):
        if file_key in self._page_dict:
            pom = self._page_dict[file_key]
        else:
            pom = self._load_pages(file_key)
        
        try:
            return pom[page_key]
        except KeyError as e:
            log.error(f"No such page model exists. Page: \"{page_key}\" in POM: \"{file_key}\" not found.")
            raise e

    def _load_pages(self, file_key):
        file_name = file_key + '.json'
        page = self._page_root.resolve() / file_name
        try:
            file = open(page, encoding='utf-8')
        except IOError as e:
            log.error("An IOError occured: %s" % e)
            raise e
        with file:
            self._page_dict[file_key] = json.load(file)
        return self._page_dict[file_key]

    def get_element(self, file_key,
                    page_key, element_key,
                    default=None, llist=None):
        if llist and [file_key, page_key] in llist:
            # If page has already been checked return None
            # llist will only be None on the top level page in the inheritance schema.
            # Prevents possible infinite loops (a calls b calls a...)
            return None
        elif llist is None:
            llist = []
        try:
            llist.append([file_key, page_key])
            page = self._page(file_key, page_key)
            if ('elements' in page
                    and element_key in page['elements']):

                element = page['elements'][element_key]
            elif ('inherits' in page):
                for f, p in page['inherits']:
                    element = self.get_element(f, p, element_key,
                                               default=default, llist=llist)
                    if element:
                        break

            # copy of element is returned to prevent
            # modifications to the element during run time
            return element.copy()

        except KeyError as e:
            if default:
                log.warning(f'One or more keys not found -> POM: \"{file_key}\", Page: \"{page_key}\". Falling back to default: {default}')
            else:
                log.error(f"Element not in POM with no fallback specified. Unable to continue.")
                raise e
        """
        TODO: Finish default implementation.
        If a given key is not found in the POM, then the given value should be treated using the "default"
        value given. Potential use for dynamic or temporary pages that are not mapped to POMs.
        """
        return default

    def get_url(self, file_key,
                page_key, url_key='url',
                default=None, llist=None):
        if llist and [file_key, page_key] in llist:
            # llist will only be None on the top level page in the inheritance schema.
            # If page has already been checked return None
            # Prevents possible infinite loops (a calls b calls a...)
            return None
        elif llist is None:
            llist = []
        try:
            llist.append([file_key, page_key])
            page = self._page(file_key, page_key)

            if url_key in page:
                return page[url_key]
            elif ('inherits' in page):
                for f, p in page['inherits']:
                    url = self.get_url(f, p, url_key,
                                       default=default, llist=llist)
                    if url:
                        return url

        except KeyError as e:
            if default:
                log.warning(f'One or more keys not found -> POM: \"{file_key}\", Page: \"{page_key}\". Falling back to default: {default}')
            else:
                log.error(f"URL not in POM with no fallback specified. Unable to continue.")
                raise e
        """
        TODO: Finish default implementation.
        If a given key is not found in the POM, then the given value should be treated using the "default"
        value given. Potential use for dynamic or temporary pages that are not mapped to POMs.
        """
        return default

    def get_page_title(self, file_key, page_key, default=None, llist=None):
        if llist and [file_key, page_key] in llist:
            # llist will only be None on the top level page in the inheritance schema.
            # If page has already been checked return None
            # Prevents possible infinite loops (a calls b calls a...)
            return None
        elif llist is None:
            llist = []
        try:
            llist.append([file_key, page_key])
            page = self._page(file_key, page_key)

            if 'title' in page:

                return page['title']

            elif ('inherits' in page):
                for f, p in page['inherits']:
                    title = self.get_page_title(f, p,
                                                default=default, llist=llist)
                    if title:
                        return title
        except KeyError as e:
            if default:
                log.warning(f'One or more keys not found -> POM: \"{file_key}\", Page: \"{page_key}\". Falling back to default: {default}')
            else:
                log.warning(f"Title not in POM with no fallback specified. Unable to continue.")
                raise e
        """
        TODO: Finish default implementation.
        If a given key is not found in the POM, then the given value should be treated using the "default"
        value given. Potential use for dynamic or temporary pages that are not mapped to POMs.
        """
        return default

    def get_page_id(self, file_key, page_key, default=None, llist=None):
        if llist and [file_key, page_key] in llist:
            # llist will only be None on the top level page in the inheritance schema.
            # If page has already been checked return None
            # Prevents possible infinite loops (a calls b calls a...)
            return None
        elif llist is None:
            llist = []
        try:
            llist.append([file_key, page_key])
            page = self._page(file_key, page_key)

            if 'page_id' in page:
                page_id = page['page_id']

            elif ('inherits' in page):
                for f, p in page['inherits']:
                    page_id = self.get_page_id(f, p,
                                               default=default, llist=llist)
                    if page_id:
                        break

            # copy of page_id is returned to prevent
            # modifications to the page id during run time
            return page_id.copy()

        except KeyError as e:
            if default:
                log.warning(f'One or more keys not found -> POM: \"{file_key}\", Page: \"{page_key}\". Falling back to default: {default}')
            else:
                log.warning(f"Page ID not in POM with no fallback specified. Unable to continue.")
                raise e
        """
        TODO: Finish default implementation.
        If a given key is not found in the POM, then the given value should be treated using the "default"
        value given. Potential use for dynamic or temporary pages that are not mapped to POMs.
        """
        return default

    def is_empty(self):
        return bool(self._page_dict)

    def add_page(self, page_key, page):
        custom_key = 'custom'
        if (custom_key not in self._page_dict):
            self._page_dict[custom_key] = {}
        p = self._page_dict[custom_key]
        p[page_key] = page
