#!/usr/bin/env python
"""Track Time

Usage:
    track_time.py query project [--project=<pattern>] [--no_aggregate]
        <timesheet>
    track_time.py query vacation <vacation> <timesheet>
    track_time.py query hours [--period=<weeks>] <contract> <timesheet>

Arguments:
    contract             Number of hours to work per week.
    timesheet            Name of timesheet.
    vacation             Number of hours vacation per year.

Options:
    --help               Show this screen.
    --no_aggregate       Don't aggregate per project.
    --period=<weeks>     Number of weeks to report [default: 3].
    --project=<pattern>  Name of project [default: *].
    --version            Show version.
"""
import datetime
import docopt
import sys
import track_time
import prettytable


@track_time.checked_call
def query_project(
        timesheet_pathname,
        project_pattern,
        aggregate):
    records = track_time.parse(file(timesheet_pathname, "r"))
    selected_records = track_time.filter_projects_by_name(records,
        project_pattern)
    merged_records = track_time.merge_records_by_project(selected_records)

    if aggregate:
        merged_records = track_time.merge_child_projects_with_parents(
            merged_records)

    table = prettytable.PrettyTable(["Project", "Hours", "Days"])
    table.align["Project"] = "l"
    table.align["Hours"] = "r"
    table.align["Days"] = "r"
    table.sortby="Project"

    for record in merged_records:
        table.add_row([
            record.project_string(),
            "{:.2f}".format(record.nr_hours),
            "{:.2f}".format(record.nr_days)
        ])

    sys.stdout.write("{}\n".format(table))


@track_time.checked_call
def query_vacation(
        timesheet_pathname,
        nr_hours_vacation):
    records = track_time.parse(file(timesheet_pathname, "r"))
    merged_records = track_time.merge_records_by_category(records)

    record_by_category = {record.project_string(): record for record in
        merged_records}
    vacation_record = record_by_category["vacation"]
    nr_hours_spent = vacation_record.nr_hours
    nr_hours_left = nr_hours_vacation - nr_hours_spent
    nr_days_left = nr_hours_left / 8.0

    table = prettytable.PrettyTable(["Available", "Spent", "Balance (h)",
        "Balance (d)"])
    table.align = "r"

    table.add_row([
        "{:.2f}".format(nr_hours_vacation),
        "{:.2f}".format(nr_hours_spent),
        "{:.2f}".format(nr_hours_left),
        "{:.2f}".format(nr_days_left)
    ])

    sys.stdout.write("{}\n".format(table))


@track_time.checked_call
def query_hours(
        timesheet_pathname,
        nr_hours_to_work,
        nr_weeks_to_report):
    records = track_time.parse(file(timesheet_pathname, "r"))
    to_time_point = track_time.last_day_of_week(datetime.date.today())
    from_time_point = to_time_point - datetime.timedelta(
        days=nr_weeks_to_report * 7)
    selected_records = track_time.filter_projects_by_date(records,
        from_time_point, to_time_point)
    merged_records = track_time.merge_records_by_date(selected_records)
    merged_records = sorted(merged_records, key=lambda record: record.date)

    # Hours per day (work + sick + holiday + vacation).
    table = prettytable.PrettyTable(["Date", "Hours"])
    table.align = "r"

    for record in merged_records:
        table.add_row([
            "{} {}".format(record.date.strftime("%a"), record.date),
            "{:.2f}".format(record.nr_hours)
        ])

    sys.stdout.write("{}\n".format(table))

    merged_records = track_time.merge_records_by_week(selected_records)
    merged_records = sorted(merged_records, key=lambda record: record.date)

    # Weekly balance.
    table = prettytable.PrettyTable(["Week", "Balance"])
    table.align = "r"

    for record in merged_records:
        table.add_row([
            "{} {}".format(record.date.strftime("%a"), record.date),
            "{:+.2f}".format(record.nr_hours - nr_hours_to_work)
        ])

    sys.stdout.write("{}\n".format(table))

    ### # Overall balance of the period.
    ### table = prettytable.PrettyTable(["Period", "Balance"])
    ### table.align = "r"

    ### for record in merged_records:
    ###     table.add_row([
    ###         "{} {}".format(record.date.strftime("%a"), record.date),
    ###         "{:+.2f}".format(record.nr_hours - nr_hours_to_work)
    ###     ])

    ### sys.stdout.write("{}\n".format(table))


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__, version="Track Time 0.0.1")

    if arguments["query"]:
        if arguments["project"]:
            timesheet_pathname = arguments["<timesheet>"]
            project_pattern = arguments["--project"]
            aggregate = not arguments["--no_aggregate"]
            status = query_project(timesheet_pathname, project_pattern,
                aggregate)
        elif arguments["vacation"]:
            timesheet_pathname = arguments["<timesheet>"]
            nr_hours_vacation = int(arguments["<vacation>"])
            status = query_vacation(timesheet_pathname, nr_hours_vacation)
        elif arguments["hours"]:
            nr_hours_to_work = int(arguments["<contract>"])
            timesheet_pathname = arguments["<timesheet>"]
            nr_weeks_to_report = int(arguments["--period"])
            status = query_hours(timesheet_pathname, nr_hours_to_work,
                nr_weeks_to_report)

    sys.exit(status)
