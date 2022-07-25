# coding=utf-8
import os
import re
import ast
import json as sys_json
import inspect
import unittest
import webbrowser
from typing import Dict, List, Any

from XTestRunner import HTMLTestRunner
from XTestRunner import XMLTestRunner
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from seldom.driver import Browser
from seldom.logging import log
from seldom.logging.exceptions import SeldomException
from seldom.running.DebugTestRunner import DebugTestRunner
from seldom.running.config import Seldom, BrowserConfig
from seldom.running.loader_extend import seldomTestLoader


INIT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "__init__.py")
_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open(INIT_FILE, 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

seldom_str = """
              __    __              
   ________  / /___/ /___  ____ ____ 
  / ___/ _ \/ / __  / __ \/ __ ` ___/
 (__  )  __/ / /_/ / /_/ / / / / / /
/____/\___/_/\__,_/\____/_/ /_/ /_/  v{v}
-----------------------------------------
                             @itest.info
""".format(v=version)


class TestMain(object):
    """
    Reimplemented Seldom Runner, Support for Web and API
    """
    TestSuits = []

    def __init__(self, path=None, case=None, browser=None, base_url=None, debug=False, timeout=10,
                 report=None, title="Seldom Test Report", tester="Anonymous", description="Test case execution",
                 rerun=0, save_last_run=False, language="en", whitelist=[], blacklist=[], open=True, auto=True):
        """
        runner test case
        :param path:
        :param case:
        :param browser:
        :param base_url:
        :param report:
        :param title:
        :param tester:
        :param description:
        :param debug:
        :param timeout:
        :param rerun:
        :param save_last_run:
        :param language:
        :param whitelist:
        :param blacklist:
        :param open:
        :param auto:
        :return:
        """
        print(seldom_str)
        self.path = path
        self.case = case
        self.browser = browser
        self.report = report
        self.title = BrowserConfig.REPORT_TITLE = title
        self.tester = tester
        self.description = description
        self.debug = debug
        self.rerun = rerun
        self.save_last_run = save_last_run
        self.language = language
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.open = open
        self.auto = auto

        if isinstance(timeout, int) is False:
            raise TypeError("Timeout {} is not integer.".format(timeout))

        if isinstance(debug, bool) is False:
            raise TypeError("Debug {} is not Boolean type.".format(debug))

        Seldom.timeout = timeout
        Seldom.debug = debug
        Seldom.base_url = base_url

        # ----- Global open browser -----
        self.open_browser()
        if self.case is not None:
            self.TestSuits = seldomTestLoader.loadTestsFromName(self.case)

        elif self.path is None:
            stack_t = inspect.stack()
            ins = inspect.getframeinfo(stack_t[1][0])
            print(ins.filename)
            file_dir = os.path.dirname(os.path.abspath(ins.filename))
            file_path = ins.filename
            if "\\" in file_path:
                this_file = file_path.split("\\")[-1]
            elif "/" in file_path:
                this_file = file_path.split("/")[-1]
            else:
                this_file = file_path
            self.TestSuits = seldomTestLoader.discover(file_dir, this_file)
        else:
            if len(self.path) > 3:
                if self.path[-3:] == ".py":
                    if "/" in self.path:
                        path_list = self.path.split("/")
                        path_dir = self.path.replace(path_list[-1], "")
                        self.TestSuits = seldomTestLoader.discover(path_dir, pattern=path_list[-1])
                    else:
                        self.TestSuits = seldomTestLoader.discover(os.getcwd(), pattern=self.path)
                else:
                    self.TestSuits = seldomTestLoader.discover(self.path)
            else:
                self.TestSuits = seldomTestLoader.discover(self.path)

        if self.auto is True:
            self.run(self.TestSuits)

            # ----- Close browser globally -----
            self.close_browser()

    def run(self, suits):
        """
        run test case
        """
        if self.debug is False:
            for filename in os.listdir(os.getcwd()):
                if filename == "reports":
                    break
            else:
                os.mkdir(os.path.join(os.getcwd(), "reports"))

            if (self.report is None) and (BrowserConfig.REPORT_PATH is not None):
                report_path = BrowserConfig.REPORT_PATH
            else:
                report_path = BrowserConfig.REPORT_PATH = os.path.join(os.getcwd(), "reports", self.report)

            with(open(report_path, 'wb')) as fp:
                if report_path.split(".")[-1] == "xml":
                    runner = XMLTestRunner(output=fp)
                    runner.run(suits)
                else:
                    runner = HTMLTestRunner(stream=fp, title=self.title, tester=self.tester, description=self.description,
                                            language=self.language, blacklist=self.blacklist, whitelist=self.whitelist)
                    runner.run(suits, rerun=self.rerun, save_last_run=self.save_last_run)

            log.printf("generated html file: file:///{}".format(report_path))
            log.printf("generated log file: file:///{}".format(BrowserConfig.LOG_PATH))
            if self.open is True:
                webbrowser.open_new("file:///{}".format(report_path))
        else:
            runner = DebugTestRunner(
                blacklist=self.blacklist,
                whitelist=self.whitelist,
                verbosity=2)
            runner.run(suits)
            log.success("A run the test in debug mode without generating HTML report!")

    def open_browser(self):
        """
        If you set up a browser, open the browser
        """
        if self.browser is not None:
            BrowserConfig.NAME = self.browser
            Seldom.driver = Browser(BrowserConfig.NAME)

    @staticmethod
    def close_browser():
        """
        How to open the browser, close the browser
        """
        if isinstance(Seldom.driver, SeleniumWebDriver):
            Seldom.driver.quit()
            Seldom.driver = None


class TestMainExtend(TestMain):
    """
    TestMain tests class extensions.
    1. Collect use case information and return to the list
    2. Execute the use cases based on the use case list
    """

    def __init__(self, path=None, browser=None, base_url=None, debug=False, timeout=10,
                 report=None, title="Seldom Test Report", description="Test case execution",
                 rerun=0, save_last_run=False, whitelist=[], blacklist=[]):

        if path is None:
            raise FileNotFoundError("Specify a file path")

        super().__init__(path=path, browser=browser, base_url=base_url, debug=debug, timeout=timeout,
                         report=report, title=title, description=description,
                         rerun=rerun, save_last_run=save_last_run, whitelist=whitelist, blacklist=blacklist,
                         open=False, auto=False)

    @staticmethod
    def collect_cases(json=False, level="data"):
        """
        Return the collected case information.
        SeldomTestLoader.collectCaseInfo = True
        :param json: Return JSON format
        :param level: Parse the level of use cases:
                * data: Each piece of test data is parsed into a use case.
                * method: Each method is resolved into a use case
        """
        if level not in ["data", "method"]:
            raise ValueError("level value error.")

        cases = seldomTestLoader.collectCaseList

        if level == "method":
            # Remove the data-driven use case end number
            cases_backup_1 = []
            for case in cases:
                case_name = case["method"]["name"]
                if "_" not in case_name:
                    cases_backup_1.append(case)
                else:
                    try:
                        int(case_name.split("_")[-1])
                    except ValueError:
                        cases_backup_1.append(case)
                    else:
                        case_name_end = case_name.split("_")[-1]
                        case["method"]["name"] = case_name[:-(len(case_name_end) + 1)]
                        cases_backup_1.append(case)

            # Remove duplicate use cases
            cases_backup_2 = []
            case_full_list = []
            for case in cases_backup_1:
                case_full = f'{case["file"]}.{case["class"]["name"]}.{case["method"]["name"]}'
                if case_full not in case_full_list:
                    case_full_list.append(case_full)
                    cases_backup_2.append(case)

            cases = cases_backup_2

        if json is True:
            return sys_json.dumps(cases, indent=2, ensure_ascii=False)

        return cases

    def _load_testsuite(self) -> Dict[str, List[Any]]:
        """
        load test suite and convert to mapping
        """
        mapping = {}

        for suits in self.TestSuits:
            for cases in suits:
                if isinstance(cases, unittest.suite.TestSuite) is False:
                    log.warning(f"Case analysis failed. {cases}")
                    continue

                for case in cases:
                    file_name = case.__module__
                    class_name = case.__class__.__name__

                    key = "{}.{}".format(file_name, class_name)
                    if mapping.get(key, None) is None:
                        mapping[key] = []

                    mapping[key].append(case)

        return mapping

    def run_cases(self, data: list) -> None:
        """
        run list case
        :param data: test case list
        :return:
        """
        if isinstance(data, list) is False:
            raise TypeError("Use cases must be lists.")

        if len(data) == 0:
            log.error("There are no use cases to execute")
            return

        suit = unittest.TestSuite()

        case_mapping = self._load_testsuite()
        for d in data:
            d_file = d.get("file", None)
            d_class = d.get("class").get("name", None)
            d_method = d.get("method").get("name", None)
            if (d_file is None) or (d_class is None) or (d_method is None):
                raise SeldomException(
                    """Use case format error, please refer to: 
                    https://seldomqa.github.io/platform/platform.html""")

            cases = case_mapping.get("{}.{}".format(d_file, d_class), None)
            if cases is None:
                continue

            for case in cases:
                method_name = str(case).split(" ")[0]
                if "_" not in method_name:
                    if method_name == d_method:
                        suit.addTest(case)
                else:
                    try:
                        int(method_name.split("_")[-1])
                    except ValueError:
                        if method_name == d_method:
                            suit.addTest(case)
                    else:
                        if method_name.startswith(d_method):
                            suit.addTest(case)

        self.run(suit)
        self.close_browser()


main = TestMain

if __name__ == '__main__':
    main()
