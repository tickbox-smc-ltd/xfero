#!/usr/bin/env python
'''
Get xfero Configuration details
'''

import os
import configparser

def get_xfero_config():

    '''

    **Purpose:**

    Retrieve xfero Configuration variables.

    *Example usage:*

    ```try:
        (xfero_logger,
         xfero_database,
         outbound_directory,
         transient_directory,
         error_directory,
         xfero_pid) = get_conf.get_xfero_config()
    except Exception as err:
        print('Cannot get xfero Config: %s' % err)
        raise err```

    :returns: log, db, outbound_directory, transient_directory, error_directory,
              xfero_pid

    **Unit Test Module:** None

    **Process Flow**

    None

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/07/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+

    '''

    try:
        xfero_conf = os.environ['XFERO_CONFIG']
    except OSError as err:
        print('Environment Variable XFERO_CONFIG is not set: Error %s' % err)
        raise err

    try:
        xfero_conf_dir = os.environ['XFERO_CONFIG_DIR']
    except OSError as err:
        print('Environment Variable XFERO_CONFIG_DIR is not set: Error %s' % err)
        raise err
    try:
        config = configparser.RawConfigParser()
    except OSError as err:
        print('Config Parser exception: Error %s' % err)
        raise err

    try:
        config.read(xfero_conf)
    except configparser.Error as err:
        print('Config Parser exception: Error %s' % err)
        raise err

    transient_directory = config.get('settings', 'transient_directory')
    outbound_directory = config.get('settings', 'outbound_directory')
    error_directory = config.get('settings', 'error_directory')
    xfero_database = config.get('database', 'db_location')
    xfero_logger = config.get('logging', 'loggers')
    xfero_pid = config.get('proc', 'pid_file')

    # Test if database is a filepath or just a filename
    if os.path.isfile(xfero_database):
        xfero_db = xfero_database
    else:
        xfero_db = xfero_conf_dir + os.sep + xfero_database

    # Test if logger file is a filepath or just a filename
    if os.path.isfile(xfero_logger):
        log = xfero_logger
    else:
        log = xfero_conf_dir + os.sep + xfero_logger
        if not os.path.isfile(log):
            print('Logger file does not exist %s' % log)
            raise OSError

    return (log, xfero_db, outbound_directory, transient_directory,
            error_directory, xfero_pid)

if __name__ == "__main__":

    (xferologger, xferodatabase, outbounddirectory,
     transientdirectory, errordirectory, xferopid) = get_xfero_config()

    print(xferologger + '\n' + xferodatabase + '\n' + outbounddirectory +
          '\n' + transientdirectory + '\n' + errordirectory + '\n' + xferopid)
