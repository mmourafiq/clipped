from unittest import TestCase

from clipped.config.exceptions import SchemaError
from clipped.config.spec import ConfigSpec


class TestConfigSpec(TestCase):
    def test_reads_yaml_files(self):
        config = ConfigSpec.read_from("tests/fixtures/parsing/yaml_file.yml")
        assert config == {"x": 10, "y": 20, "foo": "bar", "type": "yaml"}

    def test_reads_json_files(self):
        config = ConfigSpec.read_from("tests/fixtures/parsing/json_file.json")
        assert config == {"x": 1, "y": 2, "foo": "bar", "type": "json"}

    def test_reads_yaml_files_without_extension(self):
        config = ConfigSpec.read_from(
            ConfigSpec("tests/fixtures/parsing/yaml_file", config_type=".yml")
        )
        assert config == {"x": 10, "y": 20, "foo": "bar", "type": "yaml"}

    def test_reads_json_files_without_extension(self):
        config = ConfigSpec.read_from(
            ConfigSpec("tests/fixtures/parsing/json_file", config_type=".json")
        )
        assert config == {"x": 1, "y": 2, "foo": "bar", "type": "json"}

    def test_reads_non_existing_file(self):
        # Raises by default
        with self.assertRaises(SchemaError):
            ConfigSpec.read_from("tests/fixtures/parsing/no_file.yml")

        with self.assertRaises(SchemaError):
            ConfigSpec.read_from("tests/fixtures/parsing/no_file.json")

        with self.assertRaises(SchemaError):
            ConfigSpec.read_from(ConfigSpec("tests/fixtures/parsing/no_file"))

        with self.assertRaises(SchemaError):
            ConfigSpec.read_from(ConfigSpec("tests/fixtures/parsing/no_file.yml"))

        with self.assertRaises(SchemaError):
            ConfigSpec.read_from(ConfigSpec("tests/fixtures/parsing/no_file.json"))

        # Does not raise if set to ignore
        assert (
            ConfigSpec.read_from(
                ConfigSpec("tests/fixtures/parsing/no_file", check_if_exists=False)
            )
            == {}
        )

        assert (
            ConfigSpec.read_from(
                ConfigSpec("tests/fixtures/parsing/no_file.yml", check_if_exists=False)
            )
            == {}
        )

        assert (
            ConfigSpec.read_from(
                ConfigSpec("tests/fixtures/parsing/no_file.json", check_if_exists=False)
            )
            == {}
        )

    def test_reads_config_map(self):
        config = ConfigSpec.read_from([{"x": "y"}, {1: 2}, {"x": "override y"}])
        assert config == {"x": "override y", 1: 2}

        config = ConfigSpec.read_from(
            [
                {"x": "y"},
                {1: 2},
                {"x": "override y"},
                "tests/fixtures/parsing/yaml_file.yml",
                "tests/fixtures/parsing/json_file.json",
            ]
        )
        assert config == {"x": 1, "y": 2, 1: 2, "foo": "bar", "type": "json"}

    def test_reads_yaml_stream(self):
        stream = """---
        x: y
        1: 2
        """
        config = ConfigSpec.read_from(stream)
        assert config == {"x": "y", 1: 2}

    def test_reads_non_valid_yaml_stream(self):
        stream = ";sdfsd;sdff"
        with self.assertRaises(SchemaError):
            ConfigSpec.read_from(stream)

    def test_reads_json_stream(self):
        stream = """---
        {x: y, 1: 2}
        """
        config = ConfigSpec.read_from(stream)
        assert config is not None
