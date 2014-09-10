#!/usr/bin/env python
"""Track Time

Usage:
    track_time.py query project [--project=<pattern>] [--no_aggregate]
        <timesheet>

Arguments:
    timesheet            Name of timesheet to use

Options:
    --help               Show this screen.
    --no_aggregate       Don't aggregate per project.
    --project=<pattern>  Name of project [default: *]
    --version            Show version.
"""
import docopt
import sys
import track_time


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

    for record in merged_records:
        sys.stdout.write("{project}: {nr_hours}\n".format(
            project=record.project_string(),
            nr_hours=record.nr_hours))


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__, version="Track Time 0.0.1")

    if arguments["query"]:
        if arguments["project"]:
            timesheet_pathname = arguments["<timesheet>"]
            project_pattern = arguments["--project"]
            aggregate = not arguments["--no_aggregate"]

            status = query_project(timesheet_pathname, project_pattern,
                aggregate)

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
