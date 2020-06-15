import unittest
from unittest import mock

from process_words import WordHandler


class TestWordHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = WordHandler()

    def test_set_word(self):
        self.handler.set_word("Cat")
        self.assertEqual(self.handler.get_current_word(), "Cat")

    def test_get_translate(self):
        self.handler.set_word("Cat")
        with mock.patch('process_words.WordHandler.get_translate') as mock_translate:
            mock_translate.return_value = "кошка"

        self.assertEqual(self.handler.get_translate(), "кошка")


if __name__ == '__main__':
    unittest.main()