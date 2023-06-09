import datetime

from unittest import TestCase

from clipped.utils.humanize import humanize_timedelta, humanize_timesince
from clipped.utils.tz import now


class HumanizeTimesinceTest(TestCase):
    def test_humanize_timesince(self):
        current_date = now()
        self.assertEqual(humanize_timesince(current_date), "a few seconds ago")
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(minutes=1)),
            "1 minute ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(minutes=10)),
            "10 minutes ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(hours=1)),
            "1 hour ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(hours=10)),
            "10 hours ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(hours=24)),
            "1 day ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(hours=72)),
            "3 days ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(hours=168)),
            "1 week ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(weeks=1)),
            "1 week ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(weeks=3)),
            "3 weeks ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(weeks=53)),
            "1 year ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(days=366)),
            "1 year ago",
        )
        self.assertEqual(
            humanize_timesince(current_date - datetime.timedelta(days=800)),
            "2 years ago",
        )

    def test_humanize_times_in_the_future(self):
        self.assertEqual(
            humanize_timesince(now() + datetime.timedelta(minutes=1)),
            "a few seconds ago",
        )

    def test_humanize_timesince_few_seconds(self):
        self.assertEqual(
            "Last update: " + humanize_timesince(now()),
            "Last update: a few seconds ago",
        )


class HumanizeTimeDeltaTest(TestCase):
    """A test case for the `humanize_timedelta`."""

    def test_works_as_expected_for_valid_values(self):
        test_data = [
            (7200, "2h"),
            (36, "36s"),
            (3600, "1h"),
            (3800, "1h 3m"),
            (33000, "9h 10m"),
            (720000, "8d 8h"),
            (1000000, "11d 13h 46m"),
        ]
        for value, expected in test_data:
            result = humanize_timedelta(value)
            self.assertEqual(result, expected)
