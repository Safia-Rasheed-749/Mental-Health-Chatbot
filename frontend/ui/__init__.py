# ui/__init__.py
# This file makes the ui directory a Python package and exports modules

from . import dashboard
from . import chat
from . import mood
from . import journal

__all__ = ['dashboard', 'chat', 'mood', 'journal']
