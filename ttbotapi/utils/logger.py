# -*- coding: utf-8 -*-

"""
ttbotapi.utils.logger
~~~~~~~~~~~~~~~~~~~~~
This submodule provides logger utility functions that are consumed internally
:copyright: (c) 2022 by Mustafa Asaad.
:license: GPLv2, see LICENSE for more details.
"""
import logging
import sys


logger = logging.getLogger('ttbotapi')
formatter = logging.Formatter('[%(asctime)s][%(levelname)s]-> %(threadName)s: "%(message)s"')
console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)
logger.setLevel(logging.ERROR)