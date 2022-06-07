from dataclasses import dataclass
from selenium.webdriver.remote.webdriver import WebDriver
from enum import Enum


class RequiredAuth(Enum):
    PATIENT_LOGGED_IN = 1
    TECHNICIAN_LOGGED_IN = 2
    LOGGED_OUT = 3


@dataclass
class TechnicianConfig:
    search_url: str
    ssid:str
    mrn:str


@dataclass
class Auth:
    login_url: str
    logout_url: str
    username: str
    password: str
    status: RequiredAuth


@dataclass
class Config:
    technician:TechnicianConfig
    auth:Auth
    driver:WebDriver
    base_url:str
