from time import sleep
from helium import *
from ..jaspr_testcase import JasprTestCase, RequiredAuth, get_by_test_id


class TechnicianTestCase(JasprTestCase):

    def page_url(self):
        return self.make_url(self.config.technician.search_url)

    def required_auth(self) -> RequiredAuth:
        return RequiredAuth.TECHNICIAN_LOGGED_IN

    def test_search_ssid(self):
        print("In search", self.config.technician.ssid)
        write(self.config.technician.ssid, into=S('input[type=search]'))
        wait_until(get_by_test_id("print").exists)
        press(ENTER)
        # TODO: Add a check that the correct patient gets returned

    def test_print_summary(self):
        click(get_by_test_id("print"))
        click(Button("Print Preview"))
        click(Button("Close"))
