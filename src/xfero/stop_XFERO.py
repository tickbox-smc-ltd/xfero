#!/usr/bin/env python
'''

**Purpose:**

This script initiates the process of closing down XFERO in a tidy manner which
allows the scheduler to ensure all running threads are completed. Be prepared to
wait for tidy close down to complete.

**Usage Notes:**

This script should be performed from the command line or if there is a
requirement to stop the scheduler on a specific date or time, it can be added as
a Scheduled Task from within the XFERO Scheduler.

*Example usage:*

```python stop_XFERO.py```

:param NONE: This script takes no parameters
:returns: NONE: Nothing is returned from this script

**Process Flow**

.. figure::  ../process_flow/xfero_stop.png
   :align:   center

   Process Flow: Stop XFERO

*External dependencies*

    os (xfero.stop_XFERO)
    psutil (xfero.stop_XFERO)
    time (xfero.stop_XFERO)
    xfero
      db
         manage_control (xfero.stop_XFERO)
      get_conf (xfero.stop_XFERO)
+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+
| 05/05/2014 | Chris Falck | Modified to be called from init.d or win service  |
+------------+-------------+---------------------------------------------------+

'''

from time import sleep
import psutil
import logging.config
from xfero import get_conf as get_conf
from xfero.db import manage_control as db_control

try:
    (xfero_logger,.xfero_database, outbound_directory, transient_directory,
     error_directory, xfero_pid) = get_conf.get.xfero_config()
except Exception as err:
    print('Cannot get XFERO Config: %s' % err)
    raise err

logging.config.fileConfig(xfero_logger)
# create logger
logger = logging.getLogger('stop_xfero')
logger.info('XFERO Scheduler is shutting down...')

control_id = '1'
control_status = 'STOPPING'
try:
    rows = db_control.update_XFERO_Control(control_id, control_status)
except Exception as err:
    logger.error('Error updating XFERO_Control table: Error %s',
                 (err), exc_info=True)

sched_running = True

while sched_running:

    # sleep(10)
    try:
        rows = db_control.list_XFERO_Control()
    except Exception as err:
        logger.error('Error listing XFERO_Control table: Error %s',
                     (err), exc_info=True)

    for row in rows:
        c_id = row['control_id']
        c_status = row['control_status']

    if c_status == 'STOPPED':
        logger.info('XFERO Scheduler is Shut Down!')
        sched_running = False
    else:
        logger.info('XFERO Scheduler is waiting to stop...')

    # mon_running = True
    # while mon_running == True:
    #    logger.info('XFERO Monitor & Workers are shutting down...')

        # Open PID file to get PID
        with open(xfero_pid) as f:
            for line in f:
                for s in line.split(' '):
                    p = int(s)

        if psutil.pid_exists(p) is False:
            logger.info('XFERO Scheduler process closed...')
        else:
            logger.info('XFERO Scheduler process closing...')
            sleep(10)
