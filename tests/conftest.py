import pytest
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

driver = None

#def pytest_addoption(parser):
#    parser.addoption(
#        "--browser_name", action="store", default="chrome"
#    )

@pytest.fixture(scope="class")
def setup(request):
    global driver
    #browser_name = request.config.getoption("browser_name")
    #if browser_name == "chrome":
    #    service_obj = Service("/Users/chromedriver.exe")
    #    options = webdriver.ChromeOptions()
    #    options.add_experimental_option("detach", True)
    #    driver = webdriver.Chrome(options=options, service=service_obj)
    #elif browser_name == "firefox":
    #    service_obj = Service("/Users/geckodriver.exe")
    #    driver = webdriver.Firefox(service=service_obj)
    service_obj = Service("/Users/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, service=service_obj)
    driver.get("https://magento.softwaretestingboard.com/")
    driver.implicitly_wait(5)
    act = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    request.cls.driver = driver
    request.cls.act = act
    request.cls.wait = wait
    yield
    driver.close()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
        driver.get_screenshot_as_file(name)