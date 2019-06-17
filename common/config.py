#! python

"""this file contains all configuration options for python build"""

import datetime
import logging

__author__ = "Isha Geurtsen"
__date__ = datetime.date(2019, 6, 17)
__version__ = "Development"


# configure the logging module

class PrintHandler(logging.Handler):
    """prints records to screen"""
    def emit(self, record):
        print(self.format(record))

HANDLERS = [
    logging.FileHandler("python_build.log", "a", "UTF-8", False),
    PrintHandler(),
]

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    level=logging.INFO,
    handlers=HANDLERS,
)
