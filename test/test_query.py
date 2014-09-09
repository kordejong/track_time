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
        # TODO
        pass

    def test_merge_child_projects_with_parents(self):
        # TODO
        pass

if __name__ == "__main__":
    unittest.main()
