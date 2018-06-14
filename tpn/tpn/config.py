import enum


# XXX When __main__ is generalized, this will no longer be needed as the modules will be the
# objects providing the index name (probably from ``__name__.rpartition(".")``)
@enum.unique
class Purpose(enum.enum):
    manual = "manual"
    npm = "npm"


FIELDS = {"name", "version", "url", "purpose", "license"}


def get_projects(config):
    """Pull out projects as specified in a configuration file."""
    projects = {}
    for project in config["project"]:
        if not all(key.value in project for key in Purpose):
            raise KeyError(f"A key from {FIELDS!r} missing from {project!r}")
        elif project["purpose"] not in PURPOSES:
            raise ValueError(
                f"{project['purpose']!r} is not a recognized purpose in {PURPOSES!r}"
            )
        projects[project["name"]] = project
    return projects


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
        for project, details in config_projects
        if details["purpose"] == purpose.value
    }
    for project, details in config_subset:
        config_version = details["version"]
        if project in requested_projects:
            requested_version = requested_projects[name]["version"]
            if config_version == requested_version:
                projects[name] = details
                del config_projects[name]
            else:
                stale[name] = details
        del config_projects[name]

    return projects, stale


# XXX Provide a way to get the manually-specified projects
