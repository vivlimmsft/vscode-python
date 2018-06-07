import io
import pathlib
import tarfile

import requests


def projects(package_data):
    """Retrieve the list of projects from the package data.

    'package_data' is assumed to be from a 'package-lock.json' file. The
    projects returned only consist of the top-level dependencies listed in the
    data that are not development dependencies.

    """
    packages = {}
    for name, details in package_data["dependencies"].items():
        if details.get("dev", False):
            continue
        packages[name] = {"version": details["version"], "url": details["resolved"]}
    return packages


def fetch(tarball_url):
    """Download an npm tarball and return a tarfile.Tarfile instance."""
    url_request = requests.get(tarball_url)
    return tarfile.open(mode="r:gz", fileobj=io.BytesIO(url_request.content))


def package_filenames(tarball_paths):
    """Transform the iterable of npm tarball paths to the files contained within the package."""
    paths = []
    for path in tarball_paths:
        parts = pathlib.PurePath(path).parts
        if parts[0] == "package":
            paths.append("/".join(parts[1:]))
    return frozenset(paths)


LICENSE_FILENAMES = frozenset({"license", "license.txt"})


def find_license(filenames):
    """Find the file name for the license file."""
    for filename in filenames:
        if filename.lower() in LICENSE_FILENAMES:
            return filename
    else:
        raise ValueError("no license file found")


def fetch_license(tarball_url):
    """Download and extract the license file."""
    with fetch(tarball_url) as tarball:
        filenames = package_filenames(tarball)
        license_filename = find_license(filenames)
        with tarball.extractfile(f"package/{license_filename}") as file:
            return file.read().decode("utf-8")
