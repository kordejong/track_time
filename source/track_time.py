#!/usr/bin/env python
"""Track Time

Usage:
    track_time.py query project [--project=<pattern>] [--no_aggregate]
        <timesheet>
    track_time.py query vacation <contract> <vacation> <timesheet>
    track_time.py query hours [--project=<pattern>] [--period=<weeks>]
        <contract> <timesheet>

Arguments:
    contract             Number of hours to work per week
    timesheet            Name of timesheet
    vacation             Number of hours vacation per year

Options:
    --help               Show this screen
    --no_aggregate       Don't aggregate per project
    --period=<weeks>     Number of weeks to report [default: 3]
    --project=<pattern>  Name of project [default: *]
    --version            Show version
"""
import datetime
import docopt
import sys
import track_time
import prettytable


def write_table(
        table,
        header=None):
    # if header is not None:
    #     sys.stdout.write("{}\n".format(header))
    sys.stdout.write("{}\n".format(table))


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

    # Number of hours per projects ---------------------------------------------
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

    write_table(table)


    # Number of hours overall --------------------------------------------------
    table = prettytable.PrettyTable(["Hours", "Days"])
    table.align["Hours"] = "r"
    table.align["Days"] = "r"

    nr_hours = 0.0
    nr_days = 0.0
    for record in merged_records:
        nr_hours += record.nr_hours
        nr_days += record.nr_days

    table.add_row([
        "{:.2f}".format(nr_hours),
        "{:.2f}".format(nr_days)
    ])

    write_table(table)


@track_time.checked_call
def query_vacation(
        timesheet_pathname,
        nr_hours_to_work,  # Per week.
        nr_hours_vacation):  # Per year.
    records = track_time.parse(file(timesheet_pathname, "r"))
    merged_records = track_time.merge_records_by_category(records)

    # Vacation -----------------------------------------------------------------
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

    write_table(table, header="vacation")


    # Overtime -----------------------------------------------------------------
    # Number of hours that should have been spent on work, by the end of the
    # week.
    to_time_point = track_time.last_day_of_week(datetime.date.today())
    week_number = to_time_point.isocalendar()[1]
    nr_hours_to_work *= week_number

    # Number of hours that have been spent on work, in whatever way.
    nr_hours_spent_on_work = sum([record.nr_hours for record in merged_records])

    nr_hours_overtime = nr_hours_spent_on_work - nr_hours_to_work
    nr_days_overtime = nr_hours_overtime / 8.0

    table = prettytable.PrettyTable(["To work", "Worked", "Balance (h)",
        "Balance (d)"])
    table.align = "r"

    table.add_row([
        "{:.2f}".format(nr_hours_to_work),
        "{:.2f}".format(nr_hours_spent_on_work),
        "{:.2f}".format(nr_hours_overtime),
        "{:.2f}".format(nr_days_overtime)
    ])

    write_table(table, header="overtime")

    # Overall ------------------------------------------------------------------
    balance_vacation = nr_hours_left
    balance_overtime = nr_hours_overtime
    balance_in_hours = nr_hours_left + nr_hours_overtime
    balance_in_days = balance_in_hours / 8.0

    table = prettytable.PrettyTable(["Balance vacation", "Balance overtime",
        "Balance (h)", "Balance (d)"])
    table.align = "r"

    table.add_row([
        "{:.2f}".format(balance_vacation),
        "{:.2f}".format(balance_overtime),
        "{:.2f}".format(balance_in_hours),
        "{:.2f}".format(balance_in_days)
    ])

    write_table(table, header="balance")


@track_time.checked_call
def query_hours(
        timesheet_pathname,
        nr_hours_to_work,
        project_pattern,
        nr_weeks_to_report):
    selected_records = track_time.parse(file(timesheet_pathname, "r"))
    to_time_point = track_time.last_day_of_week(datetime.date.today())
    from_time_point = to_time_point - datetime.timedelta(
        days=(nr_weeks_to_report * 7) - 1)
    assert from_time_point.isocalendar()[2] == 1  # Monday.
    assert to_time_point.isocalendar()[2] == 7  # Sunday.
    selected_records = track_time.filter_projects_by_name(selected_records,
        project_pattern)
    selected_records = track_time.filter_projects_by_date(selected_records,
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

    write_table(table)

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

    write_table(table)

    # Balance of the whole period.
    if merged_records:
        table = prettytable.PrettyTable(["Period", "Balance"])
        table.align = "r"

        record = track_time.merge_records(selected_records)
        record.date = merged_records[0].date

        table.add_row([
            "{} {}".format(record.date.strftime("%a"), record.date),
            "{:+.2f}".format(record.nr_hours - (nr_weeks_to_report *
                nr_hours_to_work))
        ])

        write_table(table)


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
            nr_hours_to_work = int(arguments["<contract>"])
            nr_hours_vacation = int(arguments["<vacation>"])
            timesheet_pathname = arguments["<timesheet>"]
            status = query_vacation(timesheet_pathname, nr_hours_to_work,
                nr_hours_vacation)
        elif arguments["hours"]:
            nr_hours_to_work = int(arguments["<contract>"])
            timesheet_pathname = arguments["<timesheet>"]
            project_pattern = arguments["--project"]
            nr_weeks_to_report = int(arguments["--period"])
            status = query_hours(timesheet_pathname, nr_hours_to_work,
                project_pattern, nr_weeks_to_report)

    sys.exit(status)
