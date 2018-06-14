import copy

import pytest

from .. import config


PROJECT_DATA = {
    "Arch": {
        "name": "Arch",
        "version": "1.0.3",
        "license": "Some license.\n\nHopefully it's a nice one.",
        "url": "https://someplace.com/on/the/internet",
        "purpose": "npm",
    },
    "Python programming language": {
        "name": "Python programming language",
        "version": "3.6.5",
        "license": "The PSF license.\n\nIt\nis\nvery\nlong!",
        "url": "https://python.org",
        "purpose": "manual",
    },
}


def test_get_projects():
    example = {"project": list(PROJECT_DATA.values())}
    assert config.get_projects(example) == PROJECT_DATA

    bad_data = copy.deepcopy(example)
    del bad_data["project"][0]["url"]
    with pytest.raises(KeyError):
        config.get_projects(bad_data)

    bad_data = copy.deepcopy(example)
    bad_data["project"][0]["purpose"] = "nonsense"
    with pytest.raises(ValueError):
        config.get_projects(bad_data)


def test_sort():
    # XXX
    pass
