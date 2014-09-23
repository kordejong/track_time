import fnmatch
import track_time.record


def filter_projects_by_name(
        timesheet_records,
        project_name_pattern="*"):
    result = []

    for record in timesheet_records:
        # Select those records for which the project's string representation
        # matches the name pattern passed in, according to fnmatch.
        if fnmatch.fnmatch(record.project_string(), project_name_pattern):
            result.append(record)

    return result


def filter_projects_by_date(
        timesheet_records,
        from_time_point,
        to_time_point):
    result = []

    for record in timesheet_records:
        # Select those records for which the date lies within the time period
        # [from_time_point, to_time_point].
        if from_time_point <= record.date <= to_time_point:
            result.append(record)

    return result


def merge_records(
        timesheet_records,
        project=None):
    # Given a list of timesheet records, merge those records into one and
    # return the resulting record.
    # Merging records will render the resulting record's date useless. It
    # will be set to None.

    if len(timesheet_records) == 0:
        result = track_time.record.Record(None, 0.0, project)
    else:
        result = timesheet_records[0]
        for record in timesheet_records[1:]:
            result += record

        if project is not None:
            result.project = project
        else:
            result.project = timesheet_records[0].project

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


def merge_records_by_date(
        timesheet_records):
    # Given a list of timesheet records, merge those records that are
    # associated with the same date.

    # Create a dict with date as the key and the records as value.
    records_by_date = {}
    for record in timesheet_records:
        records_by_date.setdefault(record.date, []).append(record)

    for date in records_by_date:
        records_by_date[date] = merge_records(records_by_date[date])

    return records_by_date.values()


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
            records_by_project[project_name],
            [records_by_project[project_name][0].project[0]])

    return records_by_project.values()


def category(
        project):
    if len(project) != 1:
        result = "project"
    else:
        if project[0] in ["holiday", "sick", "vacation"]:
            result = project[0]
        else:
            result = "project"

    return result


def merge_records_by_category(
        timesheet_records):
    # Given a list of timesheet records, merge those records that are
    # associated with the same category (work, sick, vacation).
    # Merging records will render the resulting record's date useless. It
    # will be set to None.

    # Create a dict with category as the key and the records as value.
    records_by_category = {
        "holiday": [],
        "project": [],
        "sick": [],
        "vacation": []
    }

    for record in timesheet_records:
        records_by_category[category(record.project)].append(record)

    for category_name in records_by_category:
        records_by_category[category_name] = merge_records(
            records_by_category[category_name], [category_name])

    return records_by_category.values()
