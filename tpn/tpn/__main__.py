"""Third-party notices generation.

Usage: tpn [--npm=<package.json> --npm-lock=<package-lock.json>] [--pypi=<requirements.txt>] --config=<TPN.toml> <tpn_path>

Options:
    --npm=<package.json>            Path to a package.json for node.
    --npm-lock=<package-lock.json>  Path to a package-lock.json file for npm.
    --pypi=<requirements.txt>       Path to a requirements.txt file for pip.

"""
import json
import pathlib

import docopt
import pytoml as toml

from . import manual
from . import npm


def main(tpn_path, *, config_path, npm_path=None, npm_lock_path=None, pypi_path=None):
    tpn_path = pathlib.Path(tpn_path)
    config_path = pathlib.Path(config_path)
    config = toml.loads(config_path.read_text(encoding="utf-8"))
    projects = manual.projects_from_config(config)
    for project in projects.values():
        print(project["name"], project["version"], ":", config_path)
    if tpn_path.exists():
        known_projects = manual.parse_tpn(tpn_path.read_text())
    else:
        known_projects = {}
    # XXX manually-specified licenses
    if npm_path and npm_lock_path:
        with open(npm_path) as file:
            package_data = json.load(file)
        with open(npm_lock_path) as file:
            package_lock_data = json.load(file)
        npm_projects = npm.projects(package_data, package_lock_data)
        for name, details in list(npm_projects.items()):
            if name in projects:
                if details["version"] == projects[name]["version"]:
                    del npm_projects[name]
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
    with open(tpn_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(manual.generate_tpn(config, projects))


if __name__ == "__main__":
    print("Running ...")
    arguments = docopt.docopt(__doc__)
    main(
        arguments["<tpn_path>"],
        config_path=arguments["--config"],
        npm_path=arguments["--npm"],
        npm_lock_path=arguments["--npm-lock"],
        pypi_path=arguments["--pypi"],
    )
