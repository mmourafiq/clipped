import os
import tarfile
import tempfile

from unittest import TestCase

from clipped.path_utils import (
    append_basename,
    create_tarfile_from_path,
    get_files_by_paths,
    get_files_in_path_context,
)


class TestFiles(TestCase):
    def test_create_tarfile_from_path(self):
        files = ["tests/__init__.py"]
        with create_tarfile_from_path(files, "project_name") as tar_file_name:
            assert os.path.exists(tar_file_name)
            with tarfile.open(tar_file_name) as tf:
                members = tf.getmembers()
                assert set([m.name for m in members]) == set(files)
        assert not os.path.exists(tar_file_name)

    def test_get_files_in_path_context_raises(self):
        filepaths = ["tests/__init__.py"]
        with get_files_by_paths("repo", filepaths) as (files, files_size):
            assert len(filepaths) == len(files)

    def test_append_basename(self):
        assert append_basename("foo", "bar") == "foo/bar"
        assert append_basename("foo", "moo/bar") == "foo/bar"
        assert append_basename("/foo", "bar") == "/foo/bar"
        assert append_basename("/foo/moo", "bar") == "/foo/moo/bar"
        assert append_basename("/foo/moo", "boo/bar.txt") == "/foo/moo/bar.txt"

    def test_get_files_in_path_context(self):
        dirname = tempfile.mkdtemp()
        fpath1 = dirname + "/test1.txt"
        with open(fpath1, "w") as f:
            f.write("data1")

        fpath2 = dirname + "/test2.txt"
        with open(fpath2, "w") as f:
            f.write("data2")

        dirname2 = tempfile.mkdtemp(prefix=dirname + "/")
        fpath3 = dirname2 + "/test3.txt"
        with open(fpath3, "w") as f:
            f.write("data3")

        dirname3 = tempfile.mkdtemp(prefix=dirname + "/")
        fpath4 = dirname3 + "/test4.txt"
        with open(fpath4, "w") as f:
            f.write("data1")

        fpath5 = dirname3 + "/test5.txt"
        with open(fpath5, "w") as f:
            f.write("data2")

        dirname4 = tempfile.mkdtemp(prefix=dirname3 + "/")
        fpath6 = dirname4 + "/test6.txt"
        with open(fpath6, "w") as f:
            f.write("data3")

        with get_files_in_path_context(dirname) as files:
            assert len(files) == 6
            assert set(files) == {fpath1, fpath2, fpath3, fpath4, fpath5, fpath6}

        with get_files_in_path_context(
            dirname, exclude=[dirname3.split("/")[-1]]
        ) as files:
            assert len(files) == 3
            assert set(files) == {fpath1, fpath2, fpath3}
