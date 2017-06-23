# -*- coding: utf-8 -*-

'''
@file  main.py
@brief Application entry point.
'''

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Project Company Inc, and all authors.'
__license__   = 'The MIT License'


from os.path import isfile
import sys
import json
import logging

import drivers
from router.router import (set_driver, server_worker)


# Create module level instances.
# =============================================================================
_LOGGER = logging.getLogger('plen-ControlServer')
_LOGGER.addHandler(logging.NullHandler())


def init_logger(level=logging.INFO):
    from datetime import datetime

    log_file = './logs/{0:%Y%m%d}.log'.format(datetime.now())
    handler  = logging.FileHandler(log_file, encoding='utf-8')

    handler.formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s [%(name)s] : %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(level)


def splash():
    print("""
- * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * -
       ______    ____________________________________________________
      /      `  |                                                    |
      | @  @ | <  "Control Server" is a HTTP server to control PLEN! |
      `:====:'  |____________________________________________________|

- * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * -
"""[1:-1])

    sys.stdout.flush()


def bootstrap():
    '''
    @brief Bootstrap script for the application.
    '''

    # Initialize logging settings.
    # -------------------------------------------------------------------------
    init_logger()

    # Get configurations.
    # -------------------------------------------------------------------------
    if isfile('config.json'):
        with open('config.json', 'r') as fin:
            CONFIG = json.load(fin)

    else:
        _LOGGER.error('"config.json" is not found!')

        sys.exit()

    # Get device mapping.
    # -------------------------------------------------------------------------
    if isfile('device_map.json'):
        with open('device_map.json', 'r') as fin:
            DEVICE_MAP = json.load(fin)

    else:
        _LOGGER.error('"device_map.json" is not found!')

        sys.exit()

    # Get a data transfer driver.
    # -------------------------------------------------------------------------
    try:
        Driver = drivers.DRIVER_MAP[CONFIG['driver']['name']]

    except:
        _LOGGER.error('Driver "{}" is not found!'.format(CONFIG['driver']['name']))

        sys.exit()

    # Starting up the application.
    # -------------------------------------------------------------------------
    splash()

    set_driver(Driver(DEVICE_MAP, CONFIG['driver']['options']))
    server_worker(CONFIG['port'])


# Application entry point.
# =============================================================================
if __name__ == '__main__':
    bootstrap()
