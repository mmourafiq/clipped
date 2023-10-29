from unittest import TestCase

from clipped.utils.versions import (
    clean_version_for_check,
    clean_version_for_compatibility,
    clean_version_post_suffix,
)


class TestVersionCleaning(TestCase):
    def test_clean_version_for_compatibility(self):
        self.assertEqual(clean_version_for_compatibility("v1.2.3-4"), "1-2-3")
        self.assertEqual(clean_version_for_compatibility("1.2.3"), "1-2-3")
        self.assertEqual(clean_version_for_compatibility("v1-2-3"), "1-2-3")
        self.assertEqual(clean_version_for_compatibility(""), "")
        self.assertEqual(clean_version_for_compatibility("vv1.2.3"), "1-2-3")
        self.assertEqual(clean_version_for_compatibility("v1.2"), "1-2")
        self.assertEqual(clean_version_for_compatibility("1.2.3rc32"), "1-2-3rc32")
        self.assertEqual(clean_version_for_compatibility("v1.2.3rc32"), "1-2-3rc32")
        self.assertEqual(clean_version_for_compatibility("1.2.3-rc32"), "1-2-3")
        self.assertEqual(clean_version_for_compatibility("v1.2.3-rc32"), "1-2-3")
        self.assertEqual(clean_version_for_compatibility("1.2.3p0"), "1-2-3p0")
        self.assertEqual(clean_version_for_compatibility("v1.2.3p0"), "1-2-3p0")
        self.assertEqual(clean_version_for_compatibility("1.2.3-p0"), "1-2-3")
        self.assertEqual(clean_version_for_compatibility("v1.2.3-p0"), "1-2-3")

    def test_clean_version_for_check(self):
        self.assertEqual(clean_version_for_check("v1.2.3-4"), "1.2.3")
        self.assertEqual(clean_version_for_check("1.2.3"), "1.2.3")
        self.assertEqual(clean_version_for_check("v1-2-3"), "1.2.3")
        self.assertEqual(clean_version_for_check(""), "")
        self.assertEqual(clean_version_for_check(None), None)
        self.assertEqual(clean_version_for_check("vv1.2.3"), "1.2.3")
        self.assertEqual(clean_version_for_check("v1.2"), "1.2")
        self.assertEqual(clean_version_for_check("1.2.3rc32"), "1.2.3rc32")
        self.assertEqual(clean_version_for_check("v1.2.3rc32"), "1.2.3rc32")
        self.assertEqual(clean_version_for_check("1.2.3-rc32"), "1.2.3")
        self.assertEqual(clean_version_for_check("v1.2.3-rc32"), "1.2.3")
        self.assertEqual(clean_version_for_check("1.2.3p0"), "1.2.3p0")
        self.assertEqual(clean_version_for_check("v1.2.3p0"), "1.2.3p0")
        self.assertEqual(clean_version_for_check("1.2.3-p0"), "1.2.3")
        self.assertEqual(clean_version_for_check("v1.2.3-p0"), "1.2.3")

    def test_clean_version_post_suffix(self):
        self.assertEqual(clean_version_post_suffix("1.2.3rc0"), "1.2.3rc0")
        self.assertEqual(clean_version_post_suffix("v1.2.3rc0"), "v1.2.3rc0")
        self.assertEqual(clean_version_post_suffix("1.2.3-rc0"), "1.2.3-rc0")
        self.assertEqual(clean_version_post_suffix("v1.2.3-rc0"), "v1.2.3-rc0")
        self.assertEqual(clean_version_post_suffix("rc0"), "rc0")

        self.assertEqual(clean_version_post_suffix("1.2.3p0"), "1.2.3")
        self.assertEqual(clean_version_post_suffix("v1.2.3p0"), "v1.2.3")
        self.assertEqual(clean_version_post_suffix("1.2.3-p0"), "1.2.3")
        self.assertEqual(clean_version_post_suffix("v1.2.3-p0"), "v1.2.3")
        self.assertEqual(clean_version_post_suffix("1.2.3"), "1.2.3")
        self.assertEqual(clean_version_post_suffix("p0"), "")
        self.assertEqual(clean_version_post_suffix(""), "")
