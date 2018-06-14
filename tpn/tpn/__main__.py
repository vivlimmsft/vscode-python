"""Third-party notices generation.

Usage: tpn [--npm=<package-lock.json>] [--pypi=<requirements.txt>] --config=<TPN.toml> <tpn_path>

Options:
    --npm=<package.json>            Path to a package-lock.json for npm.
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
# (and think of both making CELA's life easier and also figuring out whether
# there is a license file with an odd name; probably will want a custom object
# which contains all the details necessary to help facilitate finding the license)

# XXX Verbose mode to emit where a license was found, otherwise only worry about
# errors.


def handle_index(module, raw_path, config_projects, cached_projects):
    _, _, index_name = module.__name__.rpartition(".")
    with open(raw_path, encoding="utf-8") as file:
        raw_data = file.read()
    requested_projects = module.projects_from_data(raw_data)
    projects, stale = config.sort(index_name, config_projects, requested_projects)
    for name, details in projects.items():
        print(f"{name} {details['version']}: configuration file")
    valid_cache_entries = tpnfile.sort(cached_projects, requested_projects)
    for name, details in valid_cache_entries.items():
        print(f"{name} {details['version']}: TPN cache")
    projects.update(valid_cache_entries)
    failures = module.fill_in_licenses(requested_projects)
    projects.update(requested_projects)
    return projects, stale, failures


def main(tpn_path, *, config_path, npm_path=None, pypi_path=None):
    tpn_path = pathlib.Path(tpn_path)
    config_path = pathlib.Path(config_path)
    config_data = toml.loads(config_path.read_text(encoding="utf-8"))
    config_projects = config.get_projects(config_data)
    projects = config.get_explicit_entries(config_projects)
    if tpn_path.exists():
        cached_projects = tpnfile.parse_tpn(tpn_path.read_text(encoding="utf-8"))
    else:
        cached_projects = {}
    if npm_path:
        npm_projects, stale, failures = handle_index(
            npm, npm_path, config_projects, cached_projects
        )
        projects.update(npm_projects)
        for name in stale:
            print("STALE:", name)
        # XXX Failures
    if pypi_path:
        # XXX Implement
        pypi_projects, stale, failures = handle_index(
            pypi, pypi_path, config_projects, cached_projects
        )
        projects.update(pypi_projects)
    with open(tpn_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(tpnfile.generate_tpn(config_data, projects))


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    main(
        arguments["<tpn_path>"],
        config_path=arguments["--config"],
        npm_path=arguments["--npm"],
        pypi_path=arguments["--pypi"],
    )
