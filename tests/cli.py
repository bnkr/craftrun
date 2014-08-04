import sys, os
sys.path.append(".")

from unittest import TestCase
from mock import Mock
from craftrun.cli import Settings

class SettingsTest(TestCase):
    def test_paths_are_relative(self):
        cli = Mock()
        cli.config = './bin/../etc/ycp-2.9.2.3.yml'
        conf = {'server_jar': 'cauldron-1.6.4-1.965.21.89-server.jar',
                'java_bin': '../jre1.7.0_65/bin/java', 'backup_dir':
                '../ycp-2.9.2.3/backup', 'server_name': 'ycp-2.9.2.3',
                'base_dir': '../ycp-2.9.2.3/server'}
        settings = Settings(cli, conf)

        old_pwd = os.getcwd()
        try:
            root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            os.chdir(root)
            path = os.path.join(root, 'jre1.7.0_65/bin/java')
            path = os.path.abspath(path)

            self.assertEquals(path, settings.java_bin)

            os.chdir('tests')
            self.assertEquals(path, settings.java_bin)
        finally:
            os.chdir(old_pwd)

if __name__ == "__main__":
    import unittest
    unittest.main()
