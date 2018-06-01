from .. import manual


EXAMPLE = """
THIRD-PARTY SOFTWARE NOTICES AND INFORMATION
Do Not Translate or Localize

Some legal-ese.


1.	Arch (https://github.com/feross/arch)
2.	diff-match-patch (https://github.com/ForbesLindesay-Unmaintained/diff-match-patch)
3.	Files from the Python Project (https://www.python.org/)
4.	fuzzy (https://github.com/mattyork/fuzzy)
5.	Get-port (https://github.com/sindresorhus/get-port)
6.	Go for Visual Studio Code (https://github.com/Microsoft/vscode-go)
7.	Google Diff Match and Patch  (https://github.com/GerHobbelt/google-diff-match-patch)

%% Arch 1.0.3 NOTICES AND INFORMATION BEGIN HERE (https://someplace.com/on/the/internet)
========================================================================================
Some license.

Hopefully it's a nice one.
===================================
END OF Arch NOTICES AND INFORMATION

%% Python programming language 3.6.5 NOTICES AND INFORMATION BEGIN HERE (https://python.org)
============================================================================================
The PSF license.

It
is
very
long!
==========================================================
END OF Python programming language NOTICES AND INFORMATION

"""

def test_manual():
    licenses = manual.parse_tpn(EXAMPLE)
    assert "Arch" in licenses
    assert licenses["Arch"] == {"version": "1.0.3", "url": "https://someplace.com/on/the/internet", "license": "Some license.\n\nHopefully it's a nice one.\n"}
    assert "Python programming language" in licenses
    assert licenses["Python programming language"] == {"version": "3.6.5", "url": "https://python.org", "license": "The PSF license.\n\nIt\nis\nvery\nlong!\n"}
