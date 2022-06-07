from jaspr.apps.test_infrastructure.testcases import JasprSimpleTestCase

from jaspr.settings.mixins.base import convert_static_url_to_regex
import re


class TestConstraints(JasprSimpleTestCase):

    def setUp(self):
        super().setUp()

    def test_frontend_regex_creation(self):
        reg = convert_static_url_to_regex("https://*.app.jasprhealth.com")
        self.assertEqual(reg, "^https://[a-zA-Z0-9\-]+\.app\.jasprhealth\.com$")

    def test_dev_branch_regex_creation(self):
        reg = convert_static_url_to_regex("https://*--ebpi-917-subdomain-clinic-slug.app.jaspr-development.com")
        self.assertEqual(reg, "^https://[a-zA-Z0-9\-]+\-\-ebpi\-917\-subdomain\-clinic\-slug\.app\.jaspr\-development\.com$")

    def test_frontend_regex_matching(self):
        reg = convert_static_url_to_regex("https://*.app.jasprhealth.com")
        result = re.match(reg, "https://noclinic.app.jasprhealth.com")
        self.assertEqual(result is not None, True)

    def test_dev_branch_regex_matching(self):
        url = "https://*--ebpi-917-subdomain-clinic-slug.app.jaspr-development.com"
        reg = convert_static_url_to_regex(url)
        test_host = "https://jaspr-test--ebpi-917-subdomain-clinic-slug.app.jaspr-development.com"
        result = re.match(reg, test_host)
        self.assertEqual(reg, "^https://[a-zA-Z0-9\-]+\-\-ebpi\-917\-subdomain\-clinic\-slug\.app\.jaspr\-development\.com$")
        self.assertEqual(result is not None, True)
