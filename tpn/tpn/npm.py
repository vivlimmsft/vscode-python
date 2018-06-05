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
