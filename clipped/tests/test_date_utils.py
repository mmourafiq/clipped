from datetime import datetime
from unittest import TestCase

from clipped.utils.dates import DateTimeFormatter, DateTimeFormatterException


class TestDateTimeFormatter(TestCase):
    def test_format_date_works_as_expected_for_given_datetime(self):
        result = DateTimeFormatter.format_date(datetime(2012, 12, 24))
        self.assertEqual(result, "2012-12-24")

    def test_format_date_accepts_rasies_for_none(self):
        with self.assertRaises(DateTimeFormatterException):
            DateTimeFormatter.format_date(None)

    def test_format_datetime_works_as_expected_for_given_datetime(self):
        result = DateTimeFormatter.format_datetime(datetime(2012, 12, 24, 16, 17, 18))
        self.assertEqual(result, "2012-12-24 16:17:18")

    def test_format_datetime_accepts_raises_for_none(self):
        with self.assertRaises(DateTimeFormatterException):
            DateTimeFormatter.format_datetime(None)

    def test_extract_date_works_as_expected_for_given_date_string(self):
        result = DateTimeFormatter.extract_date("2012-12-24", timezone="Europe/Berlin")
        self.assertEqual(result.year, 2012)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 24)

    def test_extract_date_accepts_raises_for_none(self):
        with self.assertRaises(DateTimeFormatterException):
            DateTimeFormatter.extract_date(None, timezone="Europe/Berlin")

    def test_extract_datetime_rejects_invalid_date(self):
        with self.assertRaises(DateTimeFormatterException):
            DateTimeFormatter.extract_date("foo", timezone="Europe/Berlin")

    def test_extract_datetime_works_as_expected_for_given_datetime_string(self):
        result = DateTimeFormatter.extract_datetime(
            "2012-12-24 16:17:18", timezone="Europe/Berlin"
        )
        self.assertEqual(result.year, 2012)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 24)
        self.assertEqual(result.hour, 16)
        self.assertEqual(result.minute, 17)
        self.assertEqual(result.second, 18)

    def test_extract_datetime_works_as_expected_for_given_timestamp(self):
        try:
            result = DateTimeFormatter.extract_datetime(
                "2012-12-24T16:17:18-02:00", timezone="Europe/Berlin"
            )
        except DateTimeFormatterException:
            # Python 3.6 does not support this
            return
        self.assertEqual(result.year, 2012)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 24)
        self.assertEqual(result.hour, 16)
        self.assertEqual(result.minute, 17)
        self.assertEqual(result.second, 18)

    def test_extract_datetime_accepts_raises_for_none(self):
        with self.assertRaises(DateTimeFormatterException):
            DateTimeFormatter.extract_datetime(None, timezone="Europe/Berlin")

    def test_extract_datetime_rejects_invalid_datetime(self):
        with self.assertRaises(DateTimeFormatterException):
            DateTimeFormatter.extract_datetime("foo", timezone="Europe/Berlin")

    def test_extract_works_as_expected_for_given_date_string(self):
        result = DateTimeFormatter.extract("2012-12-24", timezone="Europe/Berlin")
        self.assertEqual(result.year, 2012)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 24)

    def test_extract_works_as_expected_for_given_datetime_string(self):
        result = DateTimeFormatter.extract(
            "2012-12-24 16:17:18", timezone="Europe/Berlin"
        )
        self.assertEqual(result.year, 2012)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 24)
        self.assertEqual(result.hour, 16)
        self.assertEqual(result.minute, 17)
        self.assertEqual(result.second, 18)

    def test_extract_accepts_raises_for_none(self):
        with self.assertRaises(DateTimeFormatterException):
            DateTimeFormatter.extract(None, timezone="Europe/Berlin")

    def test_extract_rejects_invalid_datetime(self):
        with self.assertRaises(DateTimeFormatterException):
            DateTimeFormatter.extract("foo", timezone="Europe/Berlin")
