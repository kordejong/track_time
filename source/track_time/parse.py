import datetime
import re
import track_time.record


def parse_project(
        string):

    # Normalize the project string representation.
    # - Remove leading and trailing whitespace from sub-project names.
    # - Remove empty sub-project names. This removes double path seperators.
    string = string.strip().strip("/")
    project = [token.strip() for token in string.split("/") if
        len(token.strip()) > 0]

    return project


def parse(
        stream):
    """
    Parse `stream` for records with information about hours spent working,
    sick, holidaying, or vacationing per day and project.

    Return list of track_time.Record instances.
    """
    def date_time(
            date,
            tokens):
        assert(len(tokens) == 2)
        nr_hours = int(tokens[0])
        assert(0 <= nr_hours <= 24)
        nr_minutes = int(tokens[1])
        assert(0 <= nr_minutes <= 60)
        return datetime.datetime(date.year, date.month, date.day, nr_hours,
            nr_minutes)

    ### records = {}
    records = []
    period_pattern = r"\d{1,2}:\d{2}-\d{1,2}:\d{2}"
    nr_hours_pattern = r"\d{1,2}(\.\d{1,2})?"
    hours_pattern = r"(({period_pattern}) | ({nr_hours_pattern}))".format(
        period_pattern=period_pattern, nr_hours_pattern=nr_hours_pattern)
    hours_pattern = r"{hours_pattern}(\s*,\s* {hours_pattern})*".format(
        hours_pattern=hours_pattern)
    pattern = r"""
        (?P<date>\d{{8}})
        (\s*:\s*
            (?P<hours>{hours_pattern})
            (\s*:\s\s*
                (?P<project>\S+)
            )?
        )?
    """.format(hours_pattern=hours_pattern)

    pattern = re.compile(pattern, re.VERBOSE)
    line_nr = 0
    for line in stream:
        line_nr += 1
        # Split at the comment sign. The stuff before the sign is relevant.
        line = line.split("#")[0].strip()
        if len(line) == 0:
            continue

        match = re.match(pattern, line)

        if match is None:
            raise ValueError("Parse error: {}".format(line))
        elif match.end() != len(line):
            raise ValueError("Parse error at {}:{}: {}".format(
                line_nr, match.end() + 1, line))

        assert(not match.group("date") is None)
        date = match.group("date")
        date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))

        ### if not date in records:
        ###     records[date] = []

        if not match.group("hours"):
            ### records[date].append(track_time.record.Record(date=date,
            ###     nr_hours=8.0))
            records.append(track_time.record.Record(date=date, nr_hours=8.0))
        else:
            hours_strings = match.group("hours").split(",")
            nr_hours = 0.0

            for hours_string in hours_strings:
                if hours_string.find("-") == -1:
                    # Number or hours.
                    nr_hours += float(hours_string)
                else:
                    # Hour period.
                    # "9:30-12:00" -> ["9:30", "12:00"]
                    time_strings = [time_string.strip() for time_string in \
                        hours_string.split("-")]
                    assert(len(time_strings) == 2)

                    # "9:30" -> ["9", "30"]
                    tokens = time_strings[0].split(":")

                    start_time = date_time(date, time_strings[0].split(":"))
                    end_time = date_time(date, time_strings[1].split(":"))
                    assert end_time >= start_time, "{} !>= {}".format(
                        end_time, start_time)
                    period = end_time - start_time
                    nr_hours += period.total_seconds() / 60.0 / 60.0

            project = parse_project(match.group("project")) if match.group(
                "project") is not None else []
            ### records[date].append(track_time.record.Record(date=date,
            ###     nr_hours=nr_hours, project=project))
            records.append(track_time.record.Record(date=date,
                nr_hours=nr_hours, project=project))

    return records
