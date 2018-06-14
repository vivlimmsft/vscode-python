"""Third-party notices generation.

Usage: tpn [--npm=<package-lock.json>] [--pypi=<requirements.txt>] --config=<TPN.toml> <tpn_path>

Options:
    --npm=<package.json>            Path to a package-lock.json for node.
    --pypi=<requirements.txt>       Path to a requirements.txt file for pip.

"""
import json
import pathlib

import docopt
import pytoml as toml

from . import config
from . import tpnfile
from . import npm

# XXX Support teams that have e.g. 501 NPM entries
# XXX Cached projects from TPN
# XXX Manually-entered project from configuration file
# XXX Generalize so that supporting a new index is simply implementing a module:
# XXX   Needed projects from index
# XXX   If there's an entry in the configuration file, use it
# XXX   Warn about stale entries for the index in the configuration file
# XXX   If there's an entry from the cache, use it
# XXX   Get license from index (and record any failure)
# XXX   Warn about any failures
# XXX Generate TPN (if no failures)


def main(tpn_path, *, config_path, npm_path=None, pypi_path=None):
    tpn_path = pathlib.Path(tpn_path)
    config_path = pathlib.Path(config_path)
    config = toml.loads(config_path.read_text(encoding="utf-8"))
    projects = config.get_projects(config)
    if tpn_path.exists():
        known_projects = tpnfile.parse_tpn(tpn_path.read_text(encoding="utf-8"))
    else:
        known_projects = {}
    if npm_path:
        with open(npm_path, encoding="utf-8") as file:
            package_data = json.load(file)
        npm_projects = npm.projects(package_data)
        # XXX Factor out
        for name, details in list(npm_projects.items()):
            details_version = details["version"]
            if name in projects:
                projects_version = projects[name]["version"]
                if details_version == projects_version:
                    del npm_projects[name]
                    print(name, details_version, ":", config_path)
                else:
                    del project[name]
                    print(
                        name,
                        f"is outdated in {config_path}",
                        f"({projects_version} != {details_version}",
                    )
            elif name in known_projects:
                known_details = known_projects[name]
                if details["version"] == known_details["version"]:
                    projects[name] = known_details
                    del npm_projects[name]
                    print(name, details["version"], ":", tpn_path)
        for name, details in npm_projects.items():
            print(name, details["version"], ":", details["url"])
            details["license"] = npm.fetch_license(details["url"])
            projects[name] = details
            # XXX ! fill_in_licenses() which could be made concurrent
            # XXX ! warn if copyleft
    if pypi_path:
        # XXX ! Repeat above for PyPI.
        pass
    # XXX Check for stale config entries
    with open(tpn_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(tpnfile.generate_tpn(config, projects))


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    main(
        arguments["<tpn_path>"],
        config_path=arguments["--config"],
        npm_path=arguments["--npm"],
        pypi_path=arguments["--pypi"],
    )
