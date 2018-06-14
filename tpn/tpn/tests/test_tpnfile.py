import pytest

import copy

from .. import tpnfile


PROJECT_DATA = {
    "Arch": {
        "name": "Arch",
        "version": "1.0.3",
        "license": "Some license.\n\nHopefully it's a nice one.",
        "url": "https://someplace.com/on/the/internet",
    },
    "Python programming language": {
        "name": "Python programming language",
        "version": "3.6.5",
        "license": "The PSF license.\n\nIt\nis\nvery\nlong!",
        "url": "https://python.org",
    },
}

EXAMPLE = """A header!

With legal stuff!


1. Arch 1.0.3 (https://someplace.com/on/the/internet)
2. Python programming language 3.6.5 (https://python.org)


%% Arch 1.0.3 NOTICES AND INFORMATION BEGIN HERE (https://someplace.com/on/the/internet)
=========================================
Some license.

Hopefully it's a nice one.
=========================================
END OF Arch NOTICES AND INFORMATION

%% Python programming language 3.6.5 NOTICES AND INFORMATION BEGIN HERE (https://python.org)
=========================================
The PSF license.

It
is
very
long!
=========================================
END OF Python programming language NOTICES AND INFORMATION
"""


def test_parse_tpn():
    licenses = tpnfile.parse_tpn(EXAMPLE)
    assert "Arch" in licenses
    assert licenses["Arch"] == PROJECT_DATA["Arch"]
    assert "Python programming language" in licenses
    assert (
        licenses["Python programming language"]
        == PROJECT_DATA["Python programming language"]
    )


def test_generate_tpn():
    settings = {"metadata": {"header": "A header!\n\nWith legal stuff!"}}

    assert tpnfile.generate_tpn(settings, PROJECT_DATA) == EXAMPLE
