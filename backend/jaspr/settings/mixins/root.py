"""
Root settings to build other settings files upon.
"""

import sys
from pathlib import Path

import environ

# * NOTE/TODO: Do we really need this below? Also what's the purpose of `__status__`?
__copyright__ = "Copyright 2020, Jaspr Health"
__license__ = "Proprietary"
__status__ = "Base"

# Absolute filesystem path to the project.
ROOT_DIR = Path(__file__).parents[3]

#  Allow any module in `ROOT_DIR` to be accessed directly.
sys.path.insert(0, str(ROOT_DIR))

APPS_DIR = ROOT_DIR / "jaspr" / "apps"

env = environ.Env()
