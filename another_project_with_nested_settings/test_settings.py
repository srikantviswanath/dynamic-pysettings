import unittest
from another_project_with_nested_settings.subdir.settings import another_project_settings


class TestNestedSettingsProject(unittest.TestCase):
    def test_simple_settings_get(self):
        with another_project_settings('prd'):
            self.assertEqual(another_project_settings.priority_level, 'prd_priority_level')
            self.assertEqual(another_project_settings.SETTINGS_ENV, 'prd')
        with another_project_settings('dev'):
            self.assertEqual(another_project_settings.priority_level, 'dev_priority_level')
            self.assertEqual(another_project_settings.SETTINGS_ENV, 'dev')
        with self.assertRaises(EnvironmentError):
            print(another_project_settings.priority_level)


if __name__ == '__main__':
    unittest.main()
