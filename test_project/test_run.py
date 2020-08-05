import unittest
from ..settings import


class TestDynamicPySettingsAsClient(unittest.TestCase):

    def test_get_value_simple_by_context_manager(self):
        with test_project_settings('dev'):
            self.assertEqual(test_project_settings.downstream_host, 'https://dev.thanos.com')
        with test_project_settings('prd'):
            self.assertEqual(test_project_settings.downstream_host, 'https://thanos.com')
        with self.assertRaises(EnvironmentError):
            print(test_project_settings.downstream_host)


if __name__ == '__main__':
    unittest.main()

