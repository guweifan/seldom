[GitHub](https://github.com/SeldomQA/seldom) | [Gitee](https://gitee.com/fnngj/seldom) |

![](seldom_logo.jpg)

[![PyPI version](https://badge.fury.io/py/seldom.svg)](https://badge.fury.io/py/seldom) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/seldom)

Seldom is an automation testing framework based on unittest.

> seldom 是基于unittest 的自动化测试框架。

### Features

- [x] web/app/api全功能测试框架
- [x] 提供脚手架快速创建自动化项目
- [x] 集成`XTestRunner`测试报告，现代美观
- [x] 提供丰富的断言
- [x] 提供强大的`数据驱动`
- [x] 平台化支持

### Install

```shell
pip install seldom==3.9.0
```

If you want to keep up with the latest version, you can install with github repository url:

```shell
> pip install -U git+https://github.com/SeldomQA/seldom.git@master
```

### 🤖 Quick Start

1、查看帮助：

```shell
seldom --help
Usage: seldom [OPTIONS]

  seldom CLI.

Options:
  --version                       Show version.
  --project-api TEXT              Create an API automation test project.
  --project-app TEXT              Create an App automation test project.
  --project-web TEXT              Create an Web automation test project.
  -cc, --clear-cache BOOLEAN      Clear all caches of seldom.
  -p, --path TEXT                 Run test case file path.
  -c, --collect / -nc, --no-collect
                                  Collect project test cases. Need the
                                  `--path`.
  -l, --level [data|method]       Parse the level of use cases. Need the
                                  --path.
  -j, --case-json TEXT            Test case files. Need the `--path`.
  -e, --env TEXT                  Set the Seldom run environment `Seldom.env`.
  -b, --browser [chrome|firefox|ie|edge|safari]
                                  The browser that runs the Web UI automation
                                  tests. Need the `--path`.
  -u, --base-url TEXT             The base-url that runs the HTTP automation
                                  tests. Need the `--path`.
  -d, --debug / -nd, --no-debug   Debug mode. Need the `--path`.
  -rr, --rerun INTEGER            The number of times a use case failed to run
                                  again. Need the `--path`.
  -r, --report TEXT               Set the test report for output. Need the
                                  `--path`.
  -m, --mod TEXT                  Run tests modules, classes or even
                                  individual test methods from the command
                                  line.
  -ll, --log-level [TRACE|DEBUG|INFO|SUCCESS|WARNING|ERROR]
                                  Set the log level.
  -h2c, --har2case TEXT           HAR file converts an seldom test case.
  -s2c, --swagger2case TEXT       Swagger file converts an seldom test case.
  --api-excel TEXT                Run the api test cases in the excel file.
  --help                          Show this message and exit.
```

2、创建项目：

```shell
> seldom --project-api myapi  # API automation test project.
> seldom --project-app myapp  # or App automation test project.
> seldom --project-web myweb  # or Web automation test project.
```

目录结构如下：

```shell
myweb/
├── test_dir/
│   ├── __init__.py
│   └── test_sample.py
├── test_data/
│   └── data.json
├── reports/
└── confrun.py
```

* `test_dir/` 测试用例目录。
* `test_data/` 测试数据文件目录。
* `reports/` 测试报告目录。
* `confrun.py` 运行配置文件。

3、运行项目：

* ❌️ 在`PyCharm`中右键执行。

* ✔️ 通过命令行工具执行。

```shell
> seldom -p test_dir # 运行 test_dir 测试目录


              __    __
   ________  / /___/ /___  ____ ____
  / ___/ _ \/ / __  / __ \/ __ ` ___/
 (__  )  __/ / /_/ / /_/ / / / / / /
/____/\___/_/\__,_/\____/_/ /_/ /_/  v3.x.x
-----------------------------------------
                             @itest.info
...

2022-04-30 18:37:36 log.py | INFO | ✅ Find 1 element: id=sb_form_q  -> input 'seldom'.
2022-04-30 18:37:39 log.py | INFO | 👀 assertIn title: seldom - 搜索.
.52022-04-30 18:37:39 log.py | INFO | 📖 https://cn.bing.com
2022-04-30 18:37:41 log.py | INFO | ✅ Find 1 element: id=sb_form_q  -> input 'poium'.
2022-04-30 18:37:42 log.py | INFO | 👀 assertIn title: poium - 搜索.
.62022-04-30 18:37:42 log.py | INFO | 📖 https://cn.bing.com
2022-04-30 18:37:43 log.py | INFO | ✅ Find 1 element: id=sb_form_q  -> input 'XTestRunner'.
2022-04-30 18:37:44 log.py | INFO | 👀 assertIn title: XTestRunner - 搜索.
.72022-04-30 18:37:44 log.py | INFO | 📖 http://www.itest.info
2022-04-30 18:37:52 log.py | INFO | 👀 assertIn url: http://www.itest.info/.
.82022-04-30 18:37:52 log.py | SUCCESS | generated html file: file:///D:\mypro\reports\2022_04_30_18_37_29_result.html
2022-04-30 18:37:52 log.py | SUCCESS | generated log file: file:///D:\mypro\reports\seldom_log.log
```

4、查看报告

你可以到 `mypro\reports\` 目录查看测试报告。

![test report](./test_report.png)

## 🔬 Demo

> seldom继承unittest单元测试框架，完全遵循unittest编写用例规范。

[demo](/demo) 提供了丰富实例，帮你快速了解seldom的用法。

### Web UI 测试

```python
import seldom
from seldom import Steps


class BaiduTest(seldom.TestCase):

    def test_case_one(self):
        """a simple test case """
        self.open("https://www.baidu.com")
        self.type(id_="kw", text="seldom")
        self.click(css="#su")
        self.assertTitle("seldom_百度搜索")

    def test_case_two(self):
        """method chaining """
        Steps().open("https://www.baidu.com").find("#kw").type("seldom").find("#su").click()
        self.assertTitle("seldom_百度搜索")


if __name__ == '__main__':
    seldom.main(browser="chrome")
```

__说明：__

* `seldom.main()` 通过 `browser` 指定运行的浏览器。

### HTTP 测试

seldom 2.0 支持HTTP测试

```python
import seldom


class TestRequest(seldom.TestCase):

    def test_put_method(self):
        self.put('/put', data={'key': 'value'})
        self.assertStatusCode(200)

    def test_post_method(self):
        self.post('/post', data={'key': 'value'})
        self.assertStatusCode(200)

    def test_get_method(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        self.get("/get", params=payload)
        self.assertStatusCode(200)

    def test_delete_method(self):
        self.delete('/delete')
        self.assertStatusCode(200)


if __name__ == '__main__':
    seldom.main(base_url="http://httpbin.org")
```

__说明：__

* `seldom.main()` 通过 `base_url` 指定接口项目基本URL地址。

### App 测试

seldom 3.0 支持App测试

```python
import seldom
from seldom.appium_lab.keyboard import KeyEvent
from seldom.appium_lab.android import UiAutomator2Options


class TestBingApp(seldom.TestCase):

    def start(self):
        self.ke = KeyEvent(self.driver)

    def test_bing_search(self):
        """
        test bing App search
        """
        self.sleep(2)
        self.click(id_="com.microsoft.bing:id/sa_hp_header_search_box")
        self.type(id_="com.microsoft.bing:id/sapphire_search_header_input", text="seldomQA")
        self.ke.press_key("ENTER")
        self.sleep(1)
        elem = self.get_elements(xpath='//android.widget.TextView')
        self.assertIn("seldom", elem[0].text.lower())


if __name__ == '__main__':
    capabilities = {
        'deviceName': 'ELS-AN00',
        'automationName': 'UiAutomator2',
        'platformName': 'Android',
        'appPackage': 'com.microsoft.bing',
        'appActivity': 'com.microsoft.sapphire.app.main.MainSapphireActivity',
        'noReset': True,
    }
    options = UiAutomator2Options().load_capabilities(capabilities)
    seldom.main(app_server="http://127.0.0.1:4723", app_info=options, debug=True)
```

__说明：__

* `seldom.main()` 通过 `app_info` 指定App信息； `app_server` 指定appium server 地址。

## 📖 Document

[中文文档](https://seldomqa.github.io/)

### 项目实例

基于seldom的web UI自动化项目：

https://github.com/SeldomQA/seldom-web-testing

基于seldom的接口自动化项目:

https://github.com/defnngj/seldom-api-testing

## 微信（WeChat）

> 欢迎添加微信，交流和反馈问题。

<div style="display: flex;justify-content: space-between;width: 100%">
    <p><img alt="微信" src="wechat.jpg" style="width: 200px;height: 100%" ></p>
</div>

### Star History

![Star History Chart](https://api.star-history.com/svg?repos=SeldomQA/seldom&type=Date)

### 感谢

感谢从以下项目中得到思路和帮助。

* [parameterized](https://github.com/wolever/parameterized)

* [utx](https://github.com/jianbing/utx)

### 贡献者

<a href="https://github.com/SeldomQA/seldom/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=SeldomQA/seldom" />
</a>

### 交流

QQ群：948994709
