import unittest
from tass.core.page_reader import PageReader


class TestPageReader(unittest.TestCase):

    page = {
        "title": "Page One",
        "url": "tests/pages/page1.html",
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

    def test_getTitle(self):
        PageReader().add_page('test', self.page)
        title = PageReader().get_page_title('custom', 'test')
        self.assertEqual(title, self.page['title'])

    def test_getElement(self):
        PageReader().add_page('test', self.page)
        element = PageReader().get_element('custom', 'test', 'btnColor')
        self.assertEqual(element, self.page['elements']['btnColor'])
