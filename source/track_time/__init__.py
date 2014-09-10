"""
**********
track_time
**********
The track_time package contains code needed for tracking time periods worked
on projects.

.. automodule:: track_time.record
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: track_time.aggregator
   :members:
   :undoc-members:
   :show-inheritance:
"""
### import datetime
### import re
### import track_time.record
### from track_time.aggregator import Aggregator
### from track_time.record import Record

import functools
import sys
import traceback
from track_time.parse import *
from track_time.query import *


def checked_call(
        function):
    """
    Execute *function*. In case an exception is thrown, the traceback is
    written to sys.stderr, and 1 is returned. If no exception is thrown, the
    *function*'s result is returned, or 0 if *function* didn't return anything.

    This function is useful when creating a commandline application.
    """
    @functools.wraps(function)
    def wrapper(
            *args,
            **kwargs):
        result = 0
        try:
            result = function(*args, **kwargs)
        except:
            traceback.print_exc(file=sys.stderr)
            result = 1
        return 0 if result is None else result
    return wrapper
