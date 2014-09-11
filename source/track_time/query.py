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


def merge_records(
        timesheet_records):
    # Given a list of timesheet records, merge those records into one and
    # return the resulting record.
    # Merging records will render the resulting record's date useless. It
    # will be set to None.
    assert len(timesheet_records) > 0

    result = timesheet_records[0]
    for record in timesheet_records[1:]:
        result += record

    return result


def merge_records_by_project(
        timesheet_records):
    # Given a list of timesheet records, merge those records that are
    # associated with the same project. Child projects will be merged with
    # child projects, and not with associated parent projects.
    # Merging records will render the resulting record's date useless. It
    # will be set to None.

    # Create a dict with project as the key and the records as value.
    records_by_project = {}
    for record in timesheet_records:
        records_by_project.setdefault(record.project_string(), []).append(
            record)

    for project_name in records_by_project:
        records_by_project[project_name] = merge_records(
            records_by_project[project_name])

    return records_by_project.values()


def merge_child_projects_with_parents(
        timesheet_records):
    # Given a list of timesheet records, merge those records that are
    # associated with a child-project with its parent project, if available.
    # Merging records will render the resulting record's date useless. It
    # will be set to None.

    # Create a dict with parent project as the key and the records as value.
    records_by_project = {}
    for record in timesheet_records:
        records_by_project.setdefault(record.project[0], []).append(record)

    for project_name in records_by_project:
        records_by_project[project_name] = merge_records(
            records_by_project[project_name])
        records_by_project[project_name].project = \
            [records_by_project[project_name].project[0]]

    return records_by_project.values()
