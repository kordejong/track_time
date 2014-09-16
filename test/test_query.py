import datetime
import StringIO
import sys
import unittest
sys.path.append("../source")
import track_time


class TestQuery(unittest.TestCase):

    def test_grep_project(self):
        records = track_time.parse(file("sub_projects-001.txt"))
        self.assertEqual(len(records), 20)

        selected_records = track_time.grep_projects(records)
        self.assertEqual(len(selected_records), 20)

        selected_records = track_time.grep_projects(records,
            project_name_pattern="my_project_b/*")
        self.assertEqual(len(selected_records), 10)

        selected_records = track_time.grep_projects(records,
            project_name_pattern="*/blog")
        self.assertEqual(len(selected_records), 4)

    def test_merge_records_by_project(self):
        records = track_time.parse(file("sub_projects-001.txt"))

        merged_records = track_time.merge_records_by_project(records)
        self.assertEqual(len(merged_records), 14)

    def test_merge_records_by_category(self):
        records = track_time.parse(file("categories-001.txt"))

        merged_records = track_time.merge_records_by_category(records)
        self.assertEqual(len(merged_records), 3)

        self.assertEqual(merged_records[0].project, ["project"])
        self.assertEqual(merged_records[1].project, ["vacation"])
        self.assertEqual(merged_records[2].project, ["sick"])

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
