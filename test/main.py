from enum import Enum, IntEnum
import unittest
import click
import json
import sys
from pathlib import Path
from helium import kill_browser
from jaspr_integration_testing.jaspr_testcase import JasprTestCase, Browser, get_driver
from jaspr_integration_testing.config import Config, TechnicianConfig, Auth, RequiredAuth

DEFAULT_BASE_URL = "https://jaspr-test--release.app.jaspr-development.com"
DEFAULT_MODULE = 'jaspr_integration_testing.test_userflows'


class Environment(Enum):
    PRODUCTION  = "production"
    DEVELOPMENT = "development"
    INTEGRATION = "integration"
    RELEASE     = "release"

    @classmethod
    def all(clz):
        result = []
        for env in clz:
            result.append(env.value)
        return result



def load_env_vars(environment):
    file_path = Path(f"./data/{environment.name}.json").resolve()
    f = open(file_path, "rb")
    result = json.load(f)
    f.close()
    return result


def get_config(environment, base_url, driver):
    vars = load_env_vars(environment)
    tech = TechnicianConfig(**vars["technician"])
    auth = Auth(
        **vars["auth"],
        status=RequiredAuth.LOGGED_OUT
    )
    config = Config(
        technician=tech,
        auth=auth,
        driver=driver,
        base_url=base_url
    )
    return config


@click.command()
@click.option('--environment',
              type=click.Choice(Environment.all()),
              default=Environment.RELEASE.value,
              help='The environment you want to test. Release, development, integration, production')
@click.option('--browser',
              type=click.Choice(Browser.all()),
              default=Browser.CHROME.value,
              help='What browser you want to test in: Chrome 1, FireFox 2')
@click.option('--baseurl', default=DEFAULT_BASE_URL, help=f'The protocol and domain name to be used. e.g. {DEFAULT_BASE_URL}')
@click.option('--module', default=DEFAULT_MODULE, help='What tests you want to run. Default runs them all.')
def main(environment:str, browser:str, baseurl:str, module:str):
    print("Starting Test Run...")
    print(f"Environment: {environment}")
    print(f"Browser: {browser}")
    print(f"Baseurl: {baseurl}")
    print(f"--------------------------------------")
    browser = Browser(browser)
    environment = Environment(environment)
    driver = get_driver(browser)
    JasprTestCase.config = get_config(environment, baseurl, driver)
    unittest.main(
        module = module,
        exit = False,
        argv = ["test",] # This is just a hack to stop unittest from evaluating the CLI arguments
    )
    JasprTestCase.config = None
    kill_browser()
    print("Test Run Complete.")


if __name__ == "__main__":
    main()
