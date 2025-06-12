from unittest import TestCase

from clipped.utils.env import get_py_packages


class GetPyPackagesTest(TestCase):
    """Test cases for the get_py_packages function."""

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
