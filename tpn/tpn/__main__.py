"""Third-party notices generation.

Usage: tpn [--npm=<package-lock.json>] [--pypi=<requirements.txt>] <tpn_path>

Options:
    --npm=<package-lock.json>   Path to a package-lock.json file for npm.
    --pypi=<requirements.txt>   Path to a requirements.txt file for pip.

"""
import pathlib

import docopt

from . import manual
from . import npm as npmtools

def main(tpn_path, *, npm=None, pypi=None):
    tpn_path = pathlib.Path(tpn_path)
    licenses = {}
    if tpn_path.exists():
        known_licenses = manual.parse_license(tpn_path.read_text())
    else:
        known_licenses = {}
    if npm:
        with open(npm) as file:
            package_data = json.load(file)
        # XXX Get list of dependencies from package-lock.json.
        npm_projects = npmtools.projects(package_data)
        for name, details in list(npm_projects.items()):
            if name in known_licenses:
                known_details = known_licenses[name]
                if details["version"] == known_details["version"]:
                    licenses[name] = known_details
                    del npm_projects[name]
        # XXX Download npm package for the project.
        # XXX Extract project name and version.
        # XXX ! Warn if license is copyleft.
        # XXX Read license file for project.
    if pypi:
        # XXX ! Repeat above for PyPI.
        pass
    # XXX Generate TPN.


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    main(**arguments)
