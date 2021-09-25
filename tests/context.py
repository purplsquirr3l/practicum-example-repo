# -*- coding: utf-8 -*-
"""Add the modules to our environment."""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from textken import extract
from textken import constants
from textken import generate