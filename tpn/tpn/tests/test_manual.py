from .. import manual

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


def test_projects_from_config():
    assert (
        manual.projects_from_config({"project": list(PROJECT_DATA.values())})
        == PROJECT_DATA
    )


def test_parse_tpn():
    licenses = manual.parse_tpn(EXAMPLE)
    assert "Arch" in licenses
    assert licenses["Arch"] == {
        "version": "1.0.3",
        "url": "https://someplace.com/on/the/internet",
        "license": "Some license.\n\nHopefully it's a nice one.\n",
    }
    assert "Python programming language" in licenses
    assert licenses["Python programming language"] == {
        "version": "3.6.5",
        "url": "https://python.org",
        "license": "The PSF license.\n\nIt\nis\nvery\nlong!\n",
    }


def test_generate_tpn():
    settings = {"metadata": {"header": "A header!\n\nWith legal stuff!"}}

    assert manual.generate_tpn(settings, PROJECT_DATA) == EXAMPLE
