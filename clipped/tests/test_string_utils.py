from unittest import TestCase

from clipped.utils.strings import is_protected_type, slugify


class TestUtils(TestCase):
    def test_is_protected_type(self):
        assert is_protected_type(None) is True
        assert is_protected_type(1) is True
        assert is_protected_type(1.1) is True
        assert is_protected_type("foo") is False


class TestSlugify(TestCase):
    def test_slugify(self):
        self.assertEqual(
            slugify(
                " Jack & Jill like numbers 1,2,3 and 4 and silly characters ?%.$!/"
            ),
            "Jack-Jill-like-numbers-123-and-4-and-silly-characters-",
        )

    def test_unicode(self):
        self.assertEqual(
            slugify("Un \xe9l\xe9phant \xe0 l'or\xe9e du bois"),
            "Un-elephant-a-loree-du-bois",
        )

    def test_non_string_input(self):
        self.assertEqual(slugify(123), "123")
