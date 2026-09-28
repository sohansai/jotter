import importlib.metadata

from jotter import __version__


def test_package_metadata_matches_code_version():
    assert __version__ == importlib.metadata.version("jotter")
