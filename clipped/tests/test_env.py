from unittest import TestCase
from unittest.mock import patch, MagicMock

from clipped.utils.env import get_py_packages


class GetPyPackagesTest(TestCase):
    """Test cases for the get_py_packages function."""

    def test_get_py_packages_with_pkg_resources(self):
        mock_package1 = MagicMock()
        mock_package1.key = "package1"
        mock_package1.version = "1.0.0"
        mock_package2 = MagicMock()
        mock_package2.key = "package2"
        mock_package2.version = "2.0.0"

        with patch("pkg_resources.working_set", [mock_package1, mock_package2]):
            sorted_results, packages_results = get_py_packages([])
            self.assertEqual(len(sorted_results), 2)
            self.assertEqual(sorted_results[0], ("package1", "1.0.0"))
            self.assertEqual(sorted_results[1], ("package2", "2.0.0"))
            self.assertEqual(packages_results, {})

    def test_get_py_packages_with_importlib_metadata(self):
        mock_package1 = MagicMock()
        mock_package1.name = "package1"
        mock_package1.version = "1.0.0"
        mock_package2 = MagicMock()
        mock_package2.name = "package2"
        mock_package2.version = "2.0.0"

        with (
            patch("pkg_resources.working_set", side_effect=ImportError()),
            patch(
                "importlib.metadata.distributions",
                return_value=[mock_package1, mock_package2],
            ),
        ):
            sorted_results, packages_results = get_py_packages([])
            self.assertEqual(len(sorted_results), 2)
            self.assertEqual(sorted_results[0], ("package1", "1.0.0"))
            self.assertEqual(sorted_results[1], ("package2", "2.0.0"))
            self.assertEqual(packages_results, {})

    def test_get_py_packages_with_specific_packages(self):
        mock_package1 = MagicMock()
        mock_package1.key = "package1"
        mock_package1.version = "1.0.0"
        mock_package2 = MagicMock()
        mock_package2.key = "package2"
        mock_package2.version = "2.0.0"

        with patch("pkg_resources.working_set", [mock_package1, mock_package2]):
            sorted_results, packages_results = get_py_packages(["package1"])
            self.assertEqual(len(sorted_results), 2)
            self.assertEqual(packages_results, {"package1": "1.0.0"})

    def test_get_py_packages_with_case_insensitive_packages(self):
        mock_package1 = MagicMock()
        mock_package1.key = "Package1"
        mock_package1.version = "1.0.0"
        mock_package2 = MagicMock()
        mock_package2.key = "Package2"
        mock_package2.version = "2.0.0"

        with patch("pkg_resources.working_set", [mock_package1, mock_package2]):
            sorted_results, packages_results = get_py_packages(["package1"])
            self.assertEqual(len(sorted_results), 2)
            self.assertEqual(packages_results, {"package1": "1.0.0"})

    def test_get_py_packages_with_no_packages_found(self):
        with (
            patch("pkg_resources.working_set", []),
            patch("importlib.metadata.distributions", return_value=[]),
        ):
            sorted_results, packages_results = get_py_packages(["nonexistent"])
            self.assertEqual(len(sorted_results), 0)
            self.assertEqual(packages_results, {})

    def test_get_py_packages_with_real_packages(self):
        """Test that the function returns actual installed packages."""
        sorted_results, packages_results = get_py_packages([])

        # Verify we get some results
        assert len(sorted_results) > 0
        assert packages_results == {}

        # Verify the structure of results
        for name, version in sorted_results:
            self.assertIsInstance(name, str)
            self.assertIsInstance(version, str)
            self.assertGreater(len(name), 0)
            self.assertGreater(len(version), 0)

    def test_get_py_packages_with_specific_real_packages(self):
        """Test filtering specific packages that we know should be installed."""
        # These packages should be installed as they are in requirements
        test_packages = ["click", "pytz", "pyyaml", "requests"]

        sorted_results, packages_results = get_py_packages(test_packages)

        # Verify we get results
        assert len(sorted_results) > 0

        # Verify we found at least some of our test packages
        found_packages = {name.lower() for name, _ in sorted_results}
        self.assertTrue(any(pkg.lower() in found_packages for pkg in test_packages))

        # Verify packages_results contains at least some of our test packages
        assert len(packages_results) > 0
        assert any(pkg.lower() in packages_results for pkg in test_packages)
