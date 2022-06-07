from typing import List
from unittest import TestCase
from helium import *
from enum import Enum, IntEnum
from .config import Config, RequiredAuth

class Browser(Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"
    IE = "ie"
    SAFARI = "safari"

    @classmethod
    def all(cls):
        result = []
        for b in cls:
            result.append(b.value)
        return result


def get_driver(browser:Browser):
    if browser is Browser.FIREFOX:
        driver = start_chrome()
        driver.set_window_size(1100, 800)
        return driver
    if browser is Browser.CHROME:
        driver = start_chrome()
        driver.set_window_size(1100, 800)
        return driver
    raise Exception("Driver is not available for that browser")


def get_by_test_id(id: str):
    return S(f"[data-testid=\"{id}\"]")


class JasprTestCase(TestCase):

    config:Config = None

    def transition_auth(self):
        """
        This function handles moving a user from any auth state
        to any other auth state. For example, it can transition a logged in technician to a logged in patient.
        :return: None
        """
        req_auth = self.required_auth()
        if req_auth is not self.config.auth.status:
            if req_auth is RequiredAuth.LOGGED_OUT:
                self.logout()
            elif req_auth is RequiredAuth.TECHNICIAN_LOGGED_IN:
                if self.config.auth.status is RequiredAuth.PATIENT_LOGGED_IN:
                    self.logout()
                self.technician_login()
            elif req_auth is RequiredAuth.PATIENT_LOGGED_IN:  # This could be an else, leaving it in for readability
                if self.config.auth.status is RequiredAuth.LOGGED_OUT:
                    self.technician_login()
                self.patient_login(self.config.technician.ssid)

    def setUp(self) -> None:
        super().setUp()
        self.config = self.__class__.config
        self.transition_auth()
        page_url = self.page_url()
        if page_url is not None:
            go_to(page_url)

    def tearDown(self) -> None:
        super().tearDown()
        self.config = None

    def page_url(self) -> str:
        raise NotImplemented("Please implement this in your test case class")

    def make_url(self, *args):
        result = self.config.base_url
        for arg in args:
            result += arg
        return result

    def required_auth(self) -> RequiredAuth:
        return RequiredAuth.LOGGED_OUT

    def technician_login(self):
        go_to(self.make_url(self.config.auth.login_url))
        write(self.config.auth.username, into=S('#username'))
        write(self.config.auth.password, into=S('#password'))
        click("Login")
        wait_until(S('input[type=search]').exists)
        self.config.auth.status = RequiredAuth.TECHNICIAN_LOGGED_IN

    def patient_login(self, ssid: str):
        go_to(self.make_url(self.config.technician.search_url))
        write(ssid, into=S('input[type=search]'))
        wait_until(get_by_test_id("expand").exists)
        click(get_by_test_id("expand"))
        wait_until(get_by_test_id("open-session").exists)
        click(get_by_test_id("open-session"))
        click(Button('Confirm Patient Identity'))
        click(Button('Start Patient Session'))
        wait_until(S('[data-selected=true]').exists)
        self.config.auth.status = RequiredAuth.PATIENT_LOGGED_IN

    def logout(self):
        go_to(self.make_url(self.config.auth.logout_url))
        click(S("#menu"))
        click(S("#logout"))
        wait_until(S('#username').exists)
        self.config.auth.status = RequiredAuth.LOGGED_OUT
