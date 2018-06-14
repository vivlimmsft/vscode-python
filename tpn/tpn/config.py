import enum


FIELDS = {"name", "version", "url", "purpose", "license"}


def get_projects(config):
    """Pull out projects as specified in a configuration file."""
    projects = {}
    for project in config["project"]:
        if not all(key in project for key in FIELDS):
            raise KeyError(
                f"A key from {sorted(FIELDS)!r} is missing from {sorted(project.keys())!r}"
            )
        projects[project["name"]] = project
    return projects


def get_explicit_entries(config_projects):
    """Pull out and return the projects in the config that were explicitly entered.

    The projects in the returned dict are deleted from config_projects.

    """
    explicit_projects = {
        name: details
        for name, details in config_projects.items()
        if details["purpose"] == "explicit"
    }
    for project in explicit_projects:
        del config_projects[project]
    return explicit_projects


def sort(purpose, config_projects, requested_projects):
    """Sort projects in the config for the specified 'purpose' into valid and stale entries.

    The config_projects mapping will have all 'purpose' projects deleted from it
    in the end. The requested_projects mapping will have any project which was
    appropriately found in config_projects deleted.

    """
    projects = {}
    stale = {}
    config_subset = {
        project: details
        for project, details in config_projects.items()
        if details["purpose"] == purpose
    }
    for name, details in config_subset.items():
        config_version = details["version"]
        if name in requested_projects:
            requested_version = requested_projects[name]["version"]
            if config_version == requested_version:
                projects[name] = details
                del requested_projects[name]
            else:
                stale[name] = details
            del config_projects[name]

    return projects, stale
