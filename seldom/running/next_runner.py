# coding=utf-8
import os
import time
import unittest
import webbrowser
from xmlrunner import XMLTestRunner
import inspect
from seldom.logging import log
from seldom.driver import Browser
from seldom.running.HTMLTestRunner import HTMLTestRunner
from seldom.running.config import Seldom, BrowserConfig

seldom_str = """
              __    __              
   ________  / /___/ /___  ____ ____ 
  / ___/ _ \/ / __  / __ \/ __ ` ___/
 (__  )  __/ / /_/ / /_/ / / / / / /
/____/\___/_/\__,_/\____/_/ /_/ /_/ 
-----------------------------------------
                             @itest.info
"""


class TestMain(object):
    """
    seldom 2.0 runner, development...
    """
    def __init__(self, path=None, browser=None, debug=False, timeout=10,
                 report=None, title="Seldom Test Report", description="Test case execution",
                 rerun=0, save_last_run=False):
        """
        runner test case
        :param path:
        :param browser:
        :param report:
        :param title:
        :param description:
        :param debug:
        :param rerun:
        :param save_last_run:
        :param timeout:
        :return:
        """
        self.path = path
        if self.path is None:
            stack_t = inspect.stack()
            ins = inspect.getframeinfo(stack_t[1][0])
            print(ins.filename)
            file_dir = os.path.dirname(os.path.abspath(ins.filename))
            file_path = ins.filename
            print("abc", file_path)
            if "\\" in file_path:
                this_file = file_path.split("\\")[-1]
            elif "/" in file_path:
                this_file = file_path.split("/")[-1]
            else:
                this_file = file_path
            suits = unittest.defaultTestLoader.discover(file_dir, this_file)
        else:
            if len(self.path) > 3:
                if self.path[-3:] == ".py":
                    if "/" in self.path:
                        path_list = self.path.split("/")
                        path_dir = self.path.replace(path_list[-1], "")
                        suits = unittest.defaultTestLoader.discover(path_dir, pattern=path_list[-1])
                    else:
                        suits = unittest.defaultTestLoader.discover(os.getcwd(), pattern=self.path)
                else:
                    suits = unittest.defaultTestLoader.discover(self.path)
            else:
                suits = unittest.defaultTestLoader.discover(self.path)

        self.browser = browser
        self.report = report
        self.title = title
        self.description = description
        self.debug = debug
        self.rerun = rerun
        self.save_last_run = save_last_run
        self.timeout = timeout

        # set browser
        if browser is None:
            BrowserConfig.name = "chrome"
        else:
            BrowserConfig.name = browser

        if isinstance(timeout, int) is False:
            raise TypeError("Timeout {} is not integer.".format(timeout))

        if isinstance(debug, bool) is False:
            raise TypeError("Debug {} is not Boolean type.".format(debug))

        # Global launch browser, timeout and debug.
        browser = Browser(BrowserConfig.name).driver
        Seldom.driver = browser
        Seldom.timeout = timeout
        Seldom.debug = debug

        self._run_test_case(suits)

        # Close browser globally
        Seldom.driver.quit()

    def _run_test_case(self, suits):
        if self.debug is False:
            for filename in os.listdir(os.getcwd()):
                if filename == "reports":
                    break
            else:
                os.mkdir(os.path.join(os.getcwd(), "reports"))

            if self.report is None:
                now = time.strftime("%Y_%m_%d_%H_%M_%S")
                report_path = os.path.join(os.getcwd(), "reports", now + "_result.html")
                BrowserConfig.report_path = report_path
            else:
                report_path = os.path.join(os.getcwd(), "reports", self.report)

            with(open(report_path, 'wb')) as fp:
                log.info(seldom_str)
                if self.report.split(".")[-1] == "xml":
                    runner = XMLTestRunner(output=fp)
                    runner.run(suits)
                else:
                    runner = HTMLTestRunner(stream=fp, title=self.title, description=self.description)
                    runner.run(suits, rerun=self.rerun, save_last_run=self.save_last_run)

            log.info("generated html file: file:///{}".format(report_path))
            webbrowser.open_new("file:///{}".format(report_path))
        else:
            runner = unittest.TextTestRunner(verbosity=2)
            log.info("A run the test in debug mode without generating HTML report!")
            log.info(seldom_str)
            runner.run(suits)


main2 = TestMain

if __name__ == '__main__':
    main2()