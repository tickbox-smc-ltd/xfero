#!/usr/bin/env python
'''
Directory Monitor module
'''

from queue import PriorityQueue
# from queue import Queue
import logging.config
import os
import re
import time
import sys
import uuid
import scandir
from xfero import get_conf as get_conf
from xfero.db import manage_route as db_route
from xfero.db import manage_control as db_control
from xfero.workflow_manager.copy_file import Copy_File
from xfero.workflow import Workflow_Thread
from xfero.xfer import Xfer_Thread
from xfero.dirlock import Lock as dirlock


def dirmon():
    '''

    **Purpose:**

    This function initiates a monitor task. Its primary purpose it to get a list
    of directories and filename patterns by querying the XFERO_Route table to
    select rows from the table.

    It is also responsible for starting workflow and xfer worker threads, so
    first it needs to access the XFERO_Control table to get the number of threads
    it is required to startup.

    It then create 2 Priority Queues which are used to allocate work items to
    the Workflow threads and the Xfer threads.

    Next active routes are retrieved from the XFERO_Route table and a lock acquired
    on the monitored directory to ensure that other instances of xfero running on
    another node can not access the directory.

    A list of files that match the filename pattern is retrieved. If no files
    are found to match the pattern, the monitor task will process the next route
    record. Once the rows are exhausted the monitor will simply terminate.

    When files are found, they will be moved to a transient directory in
    readiness for processing.

    Details of the file to be processed are then put to the Priority Queue for
    processing by the Workflow threads.

    **Usage Notes:**

    Creates queues, starts output and worker processes and puts workflow tasks
    to the input queue.

    It creates the input and output queues. These are Priority Queues, with a
    limit of 50% more than the number of workers to avoid locking up too much
    memory in buffered objects.

    Workflow threads get from the input queue and put to the output queue. The
    control thread then simply keeps the input queue loaded as long as long as
    it has work to do before sending the None values required to shut the worker
    threads down. Once the input queue is empty, the thread terminates.

    *Example usage:*

    ```dirmon()```

    :returns: None

    **Unit Test Module:** None

    **Process Flow**

    .. figure::  ../process_flow/monitor.png
       :align:   center

       Process Flow: Monitor

    *External dependencies:*

    os (xfero.monitor)
    re (xfero.monitor)
    scandir (xfero.monitor)
    time (xfero.monitor)
    xfero
      \-db
      | \-manage_control (xfero.monitor)
      | \-manage_route (xfero.monitor)
      \-dirlock (xfero.monitor)
      \-get_conf (xfero.monitor)
      \-workflow (xfero.monitor)
      \-workflow_manager
      | \-copy_file (xfero.monitor)
      \-xfer (xfero.monitor)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/07/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 03/05/2014 | Chris Falck | Modified to enable multiprocessing threads.   |
    |            |             | Code split into 3 modules using worker and    |
    |            |             | outputthreads.                                |
    +------------+-------------+-----------------------------------------------+
    | 12/05/2014 | Chris Falck | Added the creation of 'xfero_token' for each file|
    |            |             | that is processed by XFERO. This token is unique |
    |            |             | and is passed through all the methods for     |
    |            |             | logging purposes. This allows greping log     |
    |            |             | files to extract relevant parts of the log    |
    +------------+-------------+-----------------------------------------------+
    | 24/09/2014 | Chris Falck | Added retrieval of error_directory from the   |
    |            |             | config file. This is used to hold files that  |
    |            |             | have failed in workflow or transfer processing|
    +------------+-------------+-----------------------------------------------+
    | 27/09/2014 | Chris Falck | modified call to get_conf                     |
    +------------+-------------+-----------------------------------------------+
    | 15/10/2014 | Chris Falck | Added lockfile capability to lock a directory |
    |            |             | that is being processed via XFERO. This enables  |
    |            |             | XFERO to run as an Active/Active cluster.        |
    +------------+-------------+-----------------------------------------------+
    | 16/10/2014 | Chris Falck | To enable the use of Priority Queues for      |
    |            |             | Workflow and Xfer threads the following       |
    |            |             | modifications have been made:                 |
    |            |             | [1] Replaced call to count_XFERO_Route_Priority  |
    |            |             | withcall to count_XFERO_Route.                   |
    |            |             | [2] Replaced call to read_XFERO_Priority with    |
    |            |             | call to read_XFERO_Control to get num of threads |
    |            |             | [3] Replaced the use of standard FIFO queues  |
    |            |             | with Priority Queues. This allows             |
    |            |             | prioritisation of Transfers.                  |
    |            |             | [4] Added a call to retrieve Priorities in    |
    |            |             | Priority order using list_XFERO_Priority_Asc     |
    |            |             | function.                                     |
    |            |             | [5] Added new work item to pass into workflow |
    |            |             | thread so that it can set a priority for the  |
    |            |             | xfer threads.                                 |
    |            |             | [6] Remove parameters to dirmon function      |
    +------------+-------------+-----------------------------------------------+
    '''
    try:
        (xfero_logger,
         xfero_database,
         outbound_directory,
         transient_directory,
         error_directory,
         xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s' % err)
        raise err

    done = (999, 'NONE')

    # logging.config.fileConfig(conf_dir + os.sep + 'logging.conf')
    logging.config.fileConfig(xfero_logger)
    # create logger
    logger = logging.getLogger('monitor')

    logger.info('Selecting routes to be processed')

    try:
        # print('Priority = ', priority)
        count = db_route.count_XFERO_Route()
    except Exception as err:
        logger.error(
            'Unable to retrieve Routes from DB: Error %s',
            (err), exc_info=True)
        sys.exit(0)

    # Test if zero rows returned
    # print(count[0])
    number_of_rows = count
    if number_of_rows == 0:
        logger.error('No Rows returned from select from route table')
        sys.exit(0)

    # ----- Threading set up

    try:
        # row = db_priority.read_XFERO_Priority(priority)
        row = db_control.read_XFERO_Control(1)
    except Exception as err:
        logger.error(
            'Unable to retrieve XFERO_Control from DB: Error %s',
            (err), exc_info=True)
        sys.exit(0)

    # for item in row:
    workers = row[4]

    # Create workflow and xfer queues
    inq = PriorityQueue(maxsize=int(int(workers) * 1.5))
    outq = PriorityQueue(maxsize=int(int(workers) * 1.5))

    # creates and starts as many workflow and xfer threads as configured by
    # the WORKERS constant
    for i in range(workers):
        w_thread = Workflow_Thread(inq, outq)
        w_thread.start()

        out_thread = Xfer_Thread(outq, outbound_directory)
        out_thread.start()

    # -------------

    try:
        rows = db_route.list_XFERO_Route_Active()
    except Exception as err:
        logger.error(
            'Unable to retrieve Routes from DB: Error %s',
            (err), exc_info=True)
        sys.exit(0)

    # For each row retrieved from XFERO_Routes, the function interrogates the
    # directory to get a list of files that match the filename pattern. If no
    # matching files are found, the monitor task will process the next row.
    # Once the rows are exhausted the monitor will simply terminate.
    for route in rows:
        # print('in route loop')
        route_id = route['route_id']
        route_monitoreddir = route['route_monitoreddir']
        route_filenamepattern = route['route_filenamepattern']
        route_active = route['route_active']
        route_priority = route['route_priority']
        logger.info(
            'Processing: route_id = {0}, route_monitoreddir = {1}, \
            route_filenamepattern = {2}, route_active = {3}, route_priority \
            = {4}'.format(
                route_id,
                route_monitoreddir,
                route_filenamepattern,
                route_active,
                route_priority))

        # interrogates the directory
        if os.path.isdir(route_monitoreddir) is False:
            logger.error(
                'Monitored Directory supplied is not a directory: %s',
                route_monitoreddir)
            sys.exit(0)

        # Acquire a lock in the directory
        try:
            with dirlock(route_monitoreddir + os.sep + "XFERO") as lock:
                logger.info('Lock acquired.')
                # Do something with the locked file

                for found_file in scandir.scandir(route_monitoreddir):

                    fullpath = os.path.join(route_monitoreddir, found_file.name)

                    if found_file.is_dir():
                        logger.info(
                            '%s is a directory... Skipping', fullpath)
                        continue

                    if found_file.is_symlink():
                        logger.info(
                            '%s is a symbolic link... Skipping', fullpath)
                        continue

                    logger.info(
                        'Testing Pattern Match: %s on file %s',
                        route_filenamepattern, fullpath)

                    match = re.search(route_filenamepattern, found_file.name)
                    if match is None:
                        match = re.match(route_filenamepattern, found_file.name)

                    if match is None:
                        logger.info(
                            'Pattern Not Matched: %s with file %s',
                            route_filenamepattern, fullpath)
                        continue

                    xfero_token = uuid.uuid4()  # Generate random uuid token
                    # Store the matched filename
                    original_filename = fullpath

                    logger.info(
                        'Pattern Matched: %s with file %s (XFERO_Token=%s)',
                        route_filenamepattern, fullpath, xfero_token)

                    logger_stats = logging.getLogger('ftstats')
                    logger_stats.info(
                        "File: %s - Last Modified: %s (XFERO_Token=%s)",
                        fullpath, \
                         time.ctime(os.path.getmtime(fullpath)), xfero_token)
                    logger_stats.info(
                        "File: %s - Created: %s (XFERO_Token=%s)",
                        fullpath, \
                         time.ctime(os.path.getctime(fullpath)), xfero_token)
                    logger_stats.info(
                        "File: %s - Size: %s (XFERO_Token=%s)",
                        fullpath, os.path.getsize(fullpath), xfero_token)

                    logger = logging.getLogger('monitor')
                    logger.info(
                        'move %s to %s (XFERO_Token=%s)',
                        fullpath, transient_directory, xfero_token)

                    try:
                        rename_func = Copy_File()
                        working_file = rename_func.rename_file(
                            fullpath,
                            transient_directory +
                            os.sep +
                            found_file.name)
                    except Exception as err:
                        logger.error(
                            'Rename File %s to %s. Will retry next time \
                            monitor fires. Error: %s (XFERO_Token=%s)',
                            working_file, transient_directory, err, xfero_token)
                        continue

                    # Inputs for workflow processing: route_id, file, & XFERO
                    # Token
                    work = (
                        route_priority,
                        route_id,
                        working_file,
                        original_filename,
                        xfero_token)
                    logger.debug(
                        'Work: %s - Work-Type: %s (XFERO_Token=%s)',
                        work, type(work), xfero_token)
                    inq.put(work)

        except Exception:
            logger.info('Unable to acquire a lock on %s', (route_monitoreddir))

    # When work is done put None to the queue for each worker
    for i in range(workers):
        print('None to inq worker')

        inq.put(done)
    inq.join()
    print('joined inq')
    outq.join()
    print('joined outq')

    logger.debug("Monitor process terminating")
    print('end')

if __name__ == '__main__':

    dirmon()
