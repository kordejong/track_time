import fnmatch


def grep_projects(
        timesheet_records,
        project_name_pattern="*"):
    result = []

    for record in timesheet_records:
        # Select those records for which the project's string representation
        # matches the name pattern passed in, according to fnmatch.
        if fnmatch.fnmatch(record.project_string(), project_name_pattern):
            result.append(record)

    return result


def merge_records_by_project(
        timesheet_records):
    # Given a list of timesheet records, merge those records that are
    # associated with the same project. Child projects will be merged with
    # child projects, and not with associated parent projects.
    # Merging records will render the resulting record's date useless. It
    # will be set to None.
    pass


def merge_child_projects_with_parents(
        timesheet_records):
    # Given a list of timesheet records, merge those records that are
    # associated with a child-project with its parent project, if available.
    # Merging records will render the resulting record's date useless. It
    # will be set to None.
    pass
