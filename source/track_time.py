#!/usr/bin/env python
"""Track time.

Usage:
  track_time.py <contract_hours> <vacation_hours> <worked> <vacation> <holiday> <sick>
  track_time.py (-h | --help)
  track_time.py --version

Options:
  -h --help       Show this screen.
  --version       Show version.
  contract_hours  Contract hours, per week.
  vacation_hours  Hours vaction, per year.
  worked          Name of file containing hours worked.
  vacation        Name of file containing vaction hours.
  holiday         Name of file containing holiday hours.
  sick            Name of file containing hours sick.
"""
import docopt
import sys
import track_time


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__, version="Track Time 0.2")
    contract_hours = int(arguments["<contract_hours>"])
    vacation_hours = int(arguments["<vacation_hours>"])
    worked = TrackTime.parse(file(arguments["<worked>"]))
    vacation = TrackTime.parse(file(arguments["<vacation>"]))
    holiday = TrackTime.parse(file(arguments["<holiday>"]))
    sick = TrackTime.parse(file(arguments["<sick>"]))
    aggregator = TrackTime.Aggregator(contract_hours, vacation_hours, worked,
        sick, vacation, holiday)
    aggregator.print_report(sys.stdout)
    sys.exit(0)
