import unittest
from tass.base.core.page_reader import PageReader


class TestPageReader(unittest.TestCase):

    page = {
        "title": "Page One",
        "url": "tests/pages/page1.html",
        "alt-url": "alt/url",
        "page_id":
        {
            "method": "element",
            "identifier": "btnColor"
        },
        "elements":
        {
            "btnColor":
            {
                "by": "id",
                "value": "btnColor"
            },
            "nameField":
            {
                "by": "id",
                "value": "nameField"
            },
            "btnX":
            {
                "by": "id",
                "value": "btn-x"
            }
        }
    }

    page2 = {
        "title": "Page Basic",
        "alt-url": "not/a/url",
        "page_id":
        {
            "method": "element",
            "identifier": "btnColor"
        },
        "elements":
        {
            "btnColor":
            {
                "by": "id",
                "value": "btnColor"
            },
            "nameField":
            {
                "by": "id",
                "value": "nameField"
            },
            "btnX":
            {
                "by": "id",
                "value": "btn-x"
            }
        }
    }

    page1 = {
        "title": "Page Two",
        "inherits": [["custom", "page-two"], ["custom", "page-one"]]
    }

    def tearDown(self):
        PageReader.reset()

    def test_addPage(self):
        self.assertFalse(PageReader().is_empty())
        PageReader().add_page('test', self.page)
        self.assertTrue(PageReader().pages_loaded('custom'))

    def test_getPageId(self):
        PageReader().add_page('test', self.page)
        id = PageReader().get_page_id('custom', 'test')
        self.assertEqual(id, self.page['page_id'])

    def test_getUrl(self):
        PageReader().add_page('test', self.page)
        url = PageReader().get_url('custom', 'test')
        self.assertEqual(url, self.page['url'])

    def test_getAlternateUrl(self):
        PageReader().add_page('test', self.page)
        url = PageReader().get_url('custom', 'test', 'alt-url')
        self.assertEqual(url, self.page['alt-url'])

    def test_getTitle(self):
        PageReader().add_page('test', self.page)
        title = PageReader().get_page_title('custom', 'test')
        self.assertEqual(title, self.page['title'])

    def test_getElement(self):
        PageReader().add_page('test', self.page)
        element = PageReader().get_element('custom', 'test', 'btnColor')
        self.assertEqual(element, self.page['elements']['btnColor'])

    def test_pageInheritance(self):
        PageReader().add_page('page-one', self.page)
        PageReader().add_page('page-two', self.page2)
        PageReader().add_page('test', self.page1)

        title = PageReader().get_page_title('custom', 'test')
        alt_url = PageReader().get_url('custom', 'test', url_key='alt-url')
        url = PageReader().get_url('custom', 'test')

        self.assertEqual(title, self.page1['title'])
        self.assertEqual(alt_url, self.page2['alt-url'])
        self.assertEqual(url, self.page['url'])
