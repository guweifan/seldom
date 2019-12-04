import os
import sys
import argparse
import logging
import platform
from seldom import __description__, __version__

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PY3 = sys.version_info[0] == 3

versions = sorted(['32', '64'], key=lambda v: not platform.machine().endswith(v))
os_opts = [('win', 'win', '.exe'), ('darwin', 'mac', ''), ('linux', 'linux', '')]

current_os = None
ext = ''
for o in os_opts:
    if o[0] in platform.system().lower():
        current_os = o[1]
        ext = o[2]


def main():
    """
    API test: parse command line options and run commands.
    """

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        '-v', '--version', dest='version', action='store_true',
        help="show version")

    parser.add_argument(
        '--project',
        help="Create an Seldom automation test project.")

    parser.add_argument(
        '-r',
        help="run test case")

    parser.add_argument(
        '-install',
        help="Install the browser driver, For example, 'chromedriver', 'geckodriver' ")

    args = parser.parse_args()

    if args.version:
        print("version {}".format(__version__), )
        return 0

    project_name = args.project
    if project_name:
        create_scaffold(project_name)
        return 0

    run_file = args.r
    if run_file:
        if PY3:
            py_version = "python3 -V"
            ret = os.system(py_version)
            if ret != 0:
                command = "python " + run_file
            else:
                command = "python3 " + run_file
        else:
            py_version = "python -V"
            os.system(py_version)
            command = "python " + run_file
        os.system(command)
        return 0

    driver_name = args.install
    if driver_name:
        install_driver(driver_name)
        return 0


def create_scaffold(project_name):
    """
    create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        logger.info(u"Folder {} exists, please specify a new folder name.".format(project_name))
        return

    logger.info("Start to create new test project: {}".format(project_name))
    logger.info("CWD: {}\n".format(os.getcwd()))

    def create_folder(path):
        os.makedirs(path)
        msg = "created folder: {}".format(path)
        logger.info(msg)

    def create_file(path, file_content=""):
        with open(path, 'w') as f:
            f.write(file_content)
        msg = "created file: {}".format(path)
        logger.info(msg)

    test_sample = '''import seldom


class YouTest(seldom.TestCase):

    def test_case(self):
        """a simple test case """
        self.open("https://www.baidu.com")
        self.type(id_="kw", text="seldom")
        self.click(css="#su")
        self.assertTitle("seldom")


if __name__ == '__main__':
    seldom.main("test_sample.py")

'''
    run_test = """import seldom


if __name__ == '__main__':
    # run test
    # seldom.main("./test_dir/")
    seldom.main("./test_dir/test_sample.py")

"""
    create_folder(project_name)
    create_folder(os.path.join(project_name, "test_dir"))
    create_folder(os.path.join(project_name, "reports"))
    create_file(os.path.join(project_name, "test_dir", "test_sample.py"), test_sample)
    create_file(os.path.join(project_name, "run.py"), run_test)


def install_driver(driver_name):
    """
    Download and install the browser driver
    :param driver_name:
    """
    pass
