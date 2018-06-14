import io
import pathlib
import tarfile

import requests


def projects(package_data):
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


def package_filenames(tarball_paths):
    """Transform the iterable of npm tarball paths to the files contained within the package."""
    paths = []
    for path in tarball_paths:
        parts = pathlib.PurePath(path).parts
        if parts[0] == "package":
            paths.append("/".join(parts[1:]))
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


def find_license(filenames):
    """Find the file name for the license file."""
    for filename in filenames:
        if filename.lower() in LICENSE_FILENAMES:
            return filename
    else:
        raise ValueError("no license file found")


def fetch_license(tarball_url):
    """Download and extract the license file."""
    url_request = requests.get(tarball_url)
    with tarfile.open(mode="r:gz", fileobj=io.BytesIO(url_request.content)) as tarball:
        filenames = package_filenames(tarball.getnames())
        license_filename = find_license(filenames)
        with tarball.extractfile(f"package/{license_filename}") as file:
            return file.read().decode("utf-8")
