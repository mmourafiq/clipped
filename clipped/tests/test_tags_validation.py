from unittest import TestCase

from clipped.utils.validation import validate_tags


class TestTagsValidation(TestCase):
    def test_validate_tags(self):
        assert ["foo", "bar"] == validate_tags("foo,bar")
        assert ["foo", "bar"] == validate_tags("  , foo,    bar,   ")
        assert ["foo", "bar"] == validate_tags(["foo", "bar"])
        assert ["foo", "bar"] == validate_tags(["foo", "bar", 1, 2])
        assert [] == validate_tags([{}, {}, 1, 2])

    def test_validate_tags_with_yaml(self):
        assert ["foo", "bar"] == validate_tags("foo,bar", validate_yaml=True)
        assert ["foo", "bar"] == validate_tags("[foo,bar]", validate_yaml=True)
        assert ["foo", "bar"] == validate_tags(
            "  , foo,    bar,   ", validate_yaml=True
        )
        assert ["foo", "bar"] == validate_tags(
            "['foo ', ' bar  ' ]", validate_yaml=True
        )
        assert ["foo", "bar"] == validate_tags(
            "  [  foo,    bar,  ] ", validate_yaml=True
        )
        assert ["foo", "bar"] == validate_tags(["foo", "bar"], validate_yaml=True)
        assert ["foo", "bar"] == validate_tags(["foo", "bar", 1, 2], validate_yaml=True)
        assert ["foo", "bar"] == validate_tags(
            '["foo", "bar", 1, 2]', validate_yaml=True
        )
        assert [] == validate_tags("[{}, {}, 1, 2]", validate_yaml=True)
