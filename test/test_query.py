import datetime
import StringIO
import sys
import unittest
sys.path.append("../source")
import track_time


class TestQuery(unittest.TestCase):

    def test_filter_projects_by_name(self):
        records = track_time.parse(file("sub_projects-001.txt"))
        self.assertEqual(len(records), 20)

        selected_records = track_time.filter_projects_by_name(records)
        self.assertEqual(len(selected_records), 20)

        selected_records = track_time.filter_projects_by_name(records,
            project_name_pattern="my_project_b/*")
        self.assertEqual(len(selected_records), 10)

        selected_records = track_time.filter_projects_by_name(records,
            project_name_pattern="*/blog")
        self.assertEqual(len(selected_records), 4)

    def test_filter_projects_by_date(self):
        records = track_time.parse(file("sub_projects-001.txt"))
        selected_records = track_time.filter_projects_by_date(records,
            from_time_point=datetime.date(2014, 2, 2),
            to_time_point=datetime.date(2014, 2, 5))
        self.assertEqual(len(selected_records), 5)

    def test_merge_records_by_project(self):
        records = track_time.parse(file("sub_projects-001.txt"))

        merged_records = track_time.merge_records_by_project(records)
        self.assertEqual(len(merged_records), 14)

    def test_merge_records_by_date(self):
        records = track_time.parse(file("sub_projects-001.txt"))

        merged_records = track_time.merge_records_by_date(records)
        self.assertEqual(len(merged_records), 16)

    def test_merge_records_by_week(self):
        records = track_time.parse(file("sub_projects-001.txt"))

        merged_records = track_time.merge_records_by_week(records)
        self.assertEqual(len(merged_records), 5)
        self.assertEqual(merged_records[0].date, datetime.date(2013, 12, 30))
        self.assertEqual(merged_records[1].date, datetime.date(2014, 1, 6))
        self.assertEqual(merged_records[2].date, datetime.date(2014, 1, 27))
        self.assertEqual(merged_records[3].date, datetime.date(2014, 2, 3))
        self.assertEqual(merged_records[4].date, datetime.date(2014, 2, 10))

        self.assertEqual(merged_records[0].nr_hours, 30)
        self.assertEqual(merged_records[1].nr_hours, 18)
        self.assertEqual(merged_records[2].nr_hours, 13)
        self.assertEqual(merged_records[3].nr_hours, 23)
        self.assertEqual(merged_records[4].nr_hours, 12)

    def test_merge_records_by_category(self):
        records = track_time.parse(file("categories-001.txt"))

        merged_records = track_time.merge_records_by_category(records)
        self.assertEqual(len(merged_records), 4)

        self.assertEqual(merged_records[0].project, ["project"])
        self.assertEqual(merged_records[1].project, ["holiday"])
        self.assertEqual(merged_records[2].project, ["vacation"])
        self.assertEqual(merged_records[3].project, ["sick"])

    def test_merge_child_projects_with_parents(self):
        records = track_time.parse(file("sub_projects-001.txt"))

        merged_records = track_time.merge_child_projects_with_parents(records)
        self.assertEqual(len(merged_records), 2)

        self.assertEqual(merged_records[0].date, None)
        self.assertEqual(merged_records[0].nr_hours, 48)
        self.assertEqual(merged_records[0].project, ["my_project_a"])

        self.assertEqual(merged_records[1].date, None)
        self.assertEqual(merged_records[1].nr_hours, 48)
        self.assertEqual(merged_records[1].project, ["my_project_b"])


if __name__ == "__main__":
    unittest.main()
