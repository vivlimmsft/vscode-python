import pathlib
import re


TPN_SECTION = re.compile(
    r"%% (?P<name>.+?) (?P<version>\S+) NOTICES AND INFORMATION BEGIN HERE \((?P<url>http.+?)\)\n=+\n(?P<license>.+?)=+\nEND OF (?P=name) NOTICES AND INFORMATION",
    re.DOTALL,
)


def parse_tpn(text):
    """Break the TPN text up into individual project details."""
    licenses = {}
    for match in TPN_SECTION.finditer(text):
        details = match.groupdict()
        name = details.pop("name")
        licenses[name] = details
    return licenses
