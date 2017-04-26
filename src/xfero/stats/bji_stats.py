#!/usr/bin/env python
''' Boldon James Impart Transfer Details '''
import logging.config
import /xfero/.get_conf as get_conf
import re
import shutil
import time
import os

def collect():
    '''

    **Purpose:**

    The collect function collects transfer statistics from Boldon James Impart.

    **Usage Notes:**

    At the start of this processing rename the plog and the qlog. There is no
    need to create a new one as BJI will do that for us

    *Example usage:*

    ```collect()```

    **Process Flow**

    None

    *External dependencies*

    os (/xfero/.stats.bji_stats)
    re (/xfero/.stats.bji_stats)
    shutil (/xfero/.stats.bji_stats)
    time (/xfero/.stats.bji_stats)
    /xfero/
      get_conf (/xfero/.stats.bji_stats)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/12/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 27/10/2014 | Chris Falck | modified call to get_conf                     |
    +------------+-------------+-----------------------------------------------+

    '''
    try:
        (xfero_logger,.xfero_database, outbound_directory, transient_directory,
         error_directory, xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s', err)
        raise err

    logging.config.fileConfig(xfero_logger)

    timestamp = time.time()

    plog = "/Users/chrisfalck/Documents/workspace/XFERO/src/tools/plog"
    plog_tmp = plog + '_' + timestamp
    qlog = "/Users/chrisfalck/Documents/workspace/XFERO/src/tools/qlog/TEST01_LRSP"
    qlog_tmp = qlog + '_' + timestamp

    prevline = ''
    num_lines = 0

    # create logger
    logger = logging.getLogger('bjisendstats')

    try:
        shutil.move(plog, plog_tmp)

        lines = open(plog_tmp, "r").readlines()

        for line in lines:
            if re.search(r"^ ", line):
                print(prevline)
                print(line)
                logger.info('%s', prevline)
                logger.info('%s', line)
            prevline = line
            num_lines += 1

        try:
            os.remove(plog_tmp)
        except OSError as err:
            logger.error('OSError deleting %s: %s', plog_tmp, err)

    except OSError as err:
        logger.error('OSError Moving %s to %s: %s', plog, plog_tmp, err)

    prevline = ''
    num_lines = 0

    # create logger
    logger = logging.getLogger('bjirecvstats')
    try:
        shutil.move(qlog, qlog_tmp)

        lines = open(qlog_tmp, "r").readlines()

        for line in lines:
            if re.search(r"^ ", line):
                print(prevline)
                print(line)
                logger.info('%s', prevline)
                logger.info('%s', line)
            prevline = line
            num_lines += 1

        try:
            os.remove(qlog_tmp)
        except OSError as err:
            logger.error('OSError deleting %s: %s', qlog_tmp, err)

    except OSError as err:
        logger.error('OSError Moving %s to %s: %s', qlog, qlog_tmp, err)
