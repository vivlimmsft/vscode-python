from concurrent import futures
import io
import json
import pathlib
import tarfile

import requests


def _projects(package_data):
    """Retrieve the list of projects from the package data.

    'package_data' is assumed to be from a 'package-lock.json' file. All
    dev-related dependencies are ignored.

    """
    packages = {}
    for name, details in package_data["dependencies"].items():
        if details.get("dev", False):
            continue
        packages[name] = {
            "name": name,
            "version": details["version"],
            "url": details["resolved"],
        }
    return packages


def projects_from_data(raw_data):
    """Create the requested projects from the data string provided."""
    json_data = json.loads(raw_data)
    return _projects(json_data)


def _top_level_package_filenames(tarball_paths):
    """Transform the iterable of npm tarball paths to the top-level files contained within the package."""
    paths = []
    for path in tarball_paths:
        parts = pathlib.PurePath(path).parts
        if parts[0] == "package" and len(parts) == 2:
            paths.append(parts[1])
    return frozenset(paths)


# While ``name.lower().startswith("license")`` would works in all of the cases
# below, it is better to err on the side of being conservative and be explicit
# rather than just assume that there won't be an e.g. LICENCE_PLATES or LICENSEE
# file which isn't an actual license.
LICENSE_FILENAMES = frozenset(
    x.lower()
    for x in (
        "license",
        "license.md",
        "license.mkd",
        "license.txt",
        "LICENSE-MIT",
        "LICENSE-MIT.txt",
    )
)


def _find_license(filenames):
    """Find the file name for the license file."""
    for filename in filenames:
        if filename.lower() in LICENSE_FILENAMES:
            return filename
    else:
        raise ValueError("no license file found")


def _fetch_license(tarball_url):
    """Download and extract the license file."""
    url_request = requests.get(tarball_url)
    with tarfile.open(mode="r:gz", fileobj=io.BytesIO(url_request.content)) as tarball:
        filenames = _top_level_package_filenames(tarball.getnames())
        license_filename = _find_license(filenames)
        with tarball.extractfile(f"package/{license_filename}") as file:
            return file.read().decode("utf-8")


def fill_in_licenses(requested_projects):
    """Add the missing licenses to requested_projects.

    Any failures in the searching for licenses are returned.

    """
    names = list(requested_projects.keys())
    urls = (requested_projects[name]["url"] for name in names)
    licenses = futures.ThreadPoolExecutor.map(_fetch_license, urls)
    for name, license in zip(names, urls):
        details = requested_projects[name]
        details["license"] = license
        print(f"{name} {details['version']}: {details['url']}")
    return {}  # XXX Failures
