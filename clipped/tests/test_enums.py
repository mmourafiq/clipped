from unittest import TestCase

from clipped.enums_utils import (
    PEnum,
    enum_to_choices,
    enum_to_list,
    enum_to_set,
    values_to_choices,
)


class Dummy1Enum(PEnum):
    A = 1
    B = 2


class Dummy2Enum(PEnum):
    A = "A"
    B = "B"


class TestEnums(TestCase):
    def test_enum_to_choices(self):
        assert enum_to_choices(Dummy1Enum) == ((1, 1), (2, 2))
        assert Dummy1Enum.to_choices() == ((1, 1), (2, 2))
        assert enum_to_choices(Dummy2Enum) == (("A", "A"), ("B", "B"))
        assert Dummy2Enum.to_choices() == (("A", "A"), ("B", "B"))

    def test_values_to_choices(self):
        assert values_to_choices({1, 2}) == ((1, 1), (2, 2))
        assert values_to_choices(["A", "B"]) == (("A", "A"), ("B", "B"))

    def test_enum_to_set(self):
        assert enum_to_set(Dummy1Enum) == {1, 2}
        assert Dummy1Enum.to_set() == {1, 2}
        assert enum_to_set(Dummy2Enum) == {"A", "B"}
        assert Dummy2Enum.to_set() == {"A", "B"}

    def test_enum_to_list(self):
        assert enum_to_list(Dummy1Enum) == [1, 2]
        assert Dummy1Enum.to_list() == [1, 2]
        assert enum_to_list(Dummy2Enum) == ["A", "B"]
        assert Dummy2Enum.to_list() == ["A", "B"]

    def test_enum_member(self):
        assert Dummy1Enum.members() == ["A", "B"]
        assert Dummy2Enum.members() == ["A", "B"]
