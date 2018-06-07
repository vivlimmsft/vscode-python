"""Third-party notices generation.

Usage: tpn [--npm=<package-lock.json>] [--pypi=<requirements.txt>] <tpn_path>

Options:
    --npm=<package-lock.json>   Path to a package-lock.json file for npm.
    --pypi=<requirements.txt>   Path to a requirements.txt file for pip.

"""
import pathlib

import docopt

from . import manual
from . import npm


def main(tpn_path, *, npm_path=None, pypi_path=None):
    tpn_path = pathlib.Path(tpn_path)
    licenses = {}
    if tpn_path.exists():
        known_licenses = manual.parse_license(tpn_path.read_text())
    else:
        known_licenses = {}
    # XXX manually-specified licenses
    if npm_path:
        with open(npm_path) as file:
            package_data = json.load(file)
        npm_projects = npm.projects(package_data)
        for name, details in list(npm_projects.items()):
            if name in known_licenses:
                known_details = known_licenses[name]
                if details["version"] == known_details["version"]:
                    licenses[name] = known_details
                    del npm_projects[name]
        for name, details in npm_projects:
            details["license"] = npm.fetch_license(details["url"])
            # XXX ! fill_in_licenses() which could be made concurrent
            # XXX ! warn if copyleft
    if pypi_path:
        # XXX ! Repeat above for PyPI.
        pass
    # XXX Generate TPN.


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    main(arguments["<tpn_path>"], npm_path=arguments["--npm"], pypi_path=arguments["--pypi"])
