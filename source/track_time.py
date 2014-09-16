#!/usr/bin/env python
"""Track Time

Usage:
    track_time.py query project [--project=<pattern>] [--no_aggregate]
        <timesheet>
    track_time.py query vacation <vacation> <timesheet>

Arguments:
    contract             Number of hours to work per week.
    timesheet            Name of timesheet.
    vacation             Number of hours vacation per year.

Options:
    --help               Show this screen.
    --no_aggregate       Don't aggregate per project.
    --project=<pattern>  Name of project [default: *].
    --version            Show version.
"""
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
    selected_records = track_time.grep_projects(records, project_pattern)
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



    ### table = prettytable.PrettyTable(["Worked", "Vacation", "Sick",
    ###     "Hours left", "Days left"])
    ### table.align = "r"

    ### nr_hours_to_work = 

    ### nr_hours_left = 0.0
    ### nr_days_left = 0.0

    ### table.add_row([
    ###     "{:.2f}".format(record_by_category["project"].nr_hours),
    ###     "{:.2f}".format(record_by_category["vacation"].nr_hours),
    ###     "{:.2f}".format(record_by_category["sick"].nr_hours),
    ###     "{:.2f}".format(nr_hours_left),
    ###     "{:.2f}".format(nr_days_left)
    ### ])

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
            # nr_hours_to_work = int(arguments["<contract>"])
            timesheet_pathname = arguments["<timesheet>"]
            nr_hours_vacation = int(arguments["<vacation>"])
            status = query_vacation(timesheet_pathname, nr_hours_vacation)

    sys.exit(status)


### """Track time.
### 
### Usage:
###   track_time.py <contract_hours> <vacation_hours> <worked> <vacation> <holiday> <sick>
###   track_time.py (-h | --help)
###   track_time.py --version
### 
### Options:
###   -h --help       Show this screen.
###   --version       Show version.
###   contract_hours  Contract hours, per week.
###   vacation_hours  Hours vaction, per year.
###   worked          Name of file containing hours worked.
###   vacation        Name of file containing vaction hours.
###   holiday         Name of file containing holiday hours.
###   sick            Name of file containing hours sick.
### """

### if __name__ == "__main__":
###     arguments = docopt.docopt(__doc__, version="Track Time 0.2")
###     contract_hours = int(arguments["<contract_hours>"])
###     vacation_hours = int(arguments["<vacation_hours>"])
###     worked = TrackTime.parse(file(arguments["<worked>"]))
###     vacation = TrackTime.parse(file(arguments["<vacation>"]))
###     holiday = TrackTime.parse(file(arguments["<holiday>"]))
###     sick = TrackTime.parse(file(arguments["<sick>"]))
###     aggregator = TrackTime.Aggregator(contract_hours, vacation_hours, worked,
###         sick, vacation, holiday)
###     aggregator.print_report(sys.stdout)
###     sys.exit(0)
