#!/usr/bin/env python
'''
CRON Like Scheduler module
'''

from apscheduler.scheduler import Scheduler
from time import sleep
import logging.config
import signal
import sys
from xfero import monitor as monitor
from xfero import get_conf as get_conf
from xfero.hk import housekeeping as housekeeping
from xfero.stats import xfero_stats as.xfero_stats
from xfero.db import manage_schedule as db_schedule
from xfero.db import manage_control as db_control


def schedule():
    '''

    **Purpose:**

    This function is an in-process task scheduler that lets you schedule
    functions (or any other python callables) to be executed at times of your
    choosing.

    It replaces the reliance on externally run cron scripts for long-running
    applications such as XFERO.

    **Features:**

    * No (hard) external dependencies, except for setuptools/distribute
    * Cron-like scheduling

    **Cron-style Scheduling**

    You can specify a variety of different expressions on each field, and when
    determining the next execution time, it finds the earliest possible time
    that satisfies the conditions in every  field. This behavior resembles the
    Cron utility found in most UNIX-like operating systems.

    You can also specify the starting date for the cron-style schedule through
    the start_date parameter, which can be given as a date or datetime object
    or text.

    Unlike with crontab expressions, you can omit fields that you don't need.
    Fields greater than the least significant explicitly defined field default
    to * while lesser fields default to their minimum values except for week
    and day_of_week which default to *.

    For example, if you specify only day=1, minute=20, then the job will execute
    on the first day of every month on every year at 20 minutes of every hour.

    +------------------------+-------------------------------------------------+
    | Available Fields       | Description                                     |
    +========================+=================================================+
    | year                   | 4-digit year number                             |
    +------------------------+-------------------------------------------------+
    | month                  | month number (1-12)                             |
    +------------------------+-------------------------------------------------+
    | day                    | day of the month (1-31)                         |
    +------------------------+-------------------------------------------------+
    | week                   | ISO week number (1-53)                          |
    +------------------------+-------------------------------------------------+
    | day_of_week            | number or name of weekday (0-6 or mon-sun)      |
    +------------------------+-------------------------------------------------+
    | hour                   | hour (0-23)                                     |
    +------------------------+-------------------------------------------------+
    | minute                 | minute (0-59)                                   |
    +------------------------+-------------------------------------------------+
    | second                 | second (0-59)                                   |
    +------------------------+-------------------------------------------------+

    The following table lists all the available expressions applicable in cron-
    style schedules.

    +-----------------+------+-------------------------------------------------+
    | Expression types|Field | Description                                     |
    +=================+======+=================================================+
    | \\*              | any  | Fire on every value                            |
    +-----------------+------+-------------------------------------------------+
    | \\*/a            | any  | Fire every a values, starting from the minimum |
    +-----------------+------+-------------------------------------------------+
    | a-b             | any  | Fire on any value within the a-b range          |
    +-----------------+------+-------------------------------------------------+
    | a-b/c           | any  | Fire every c values within the a-b range        |
    +-----------------+------+-------------------------------------------------+
    | xth y           | day  | Fire on the x -th occurrence of weekday y within|
    |                 |      | the month                                       |
    +-----------------+------+-------------------------------------------------+
    | last x          | day  | Fire on the last occurrence of weekday x within |
    |                 |      | the month                                       |
    +-----------------+------+-------------------------------------------------+
    | last            | day  | Fire on the last day within the month           |
    +-----------------+------+-------------------------------------------------+
    | x,y,z           | any  | Fire on any matching expression; can combine any|
    |                 |      | number of any of the above expressions          |
    +-----------------+------+-------------------------------------------------+

    *Example Uses*

    Scheduled pull transfers from partner site.
    Scheduled outbond transfer (Part of a transfer workflow)
    Scheduled Housekeeping

    :returns: retval: Details of return

    **Unit Test Module:** None

    **Process Flow**

    .. figure::  ../process_flow/scheduler.png
       :align:   center

       Process Flow: Scheduler

    *External dependencies*

    os (xfero.scheduler)
    time (xfero.scheduler)
    xfero
      db
        manage_control (xfero.scheduler)
        manage_schedule (xfero.scheduler)
      get_conf (xfero.scheduler)
      hk
        housekeeping (xfero.scheduler)
      monitor (xfero.scheduler)
      stats
        xfero_stats (xfero.scheduler)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/07/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 27/09/2014 | Chris Falck | Added ability to call xfero_stats                |
    +------------+-------------+-----------------------------------------------+
    | 27/10/2014 | Chris Falck | modified call to get_conf                     |
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

    logging.config.fileConfig(xfero_logger)

    # create logger
    logger = logging.getLogger('scheduler')

    logger.info('Running XFERO Scheduler...')

    # Check status of XFERO_Control.control_status = 'STOPPED'. If it is 'RUNNING'
    # Advise that it is already running

    try:
        rows = db_control.read_XFERO_Control('1')
    except Exception as err:
        logger.error(
            'Unable to read XFERO_Control from DB: Error %s',
            (err),
            exc_info=True)
        sys.exit(err)

    control_id = rows[0]
    control_status = rows[1]
    # print('control_id = %s' % control_id)
    # print('control_status = %s' % control_status)

    # Advise that it is closing down as request they wait
    if control_status == 'STARTED':
        logger.warning('The XFERO Scheduler is already running! Exiting')
        print('Scheduler is running... exiting')
        sys.exit('Scheduler is running')

    # If it is 'STOPPING'
    # Advise that it is closing down as request they wait
    if control_status == 'STOPPING':
        logger.warning(
            'The XFERO Scheduler is currently stopping... Please wait! Exiting')
        print('Scheduler is stopping... wait')
        control_id = '1'
        control_status = 'STOPPED'
        try:
            rows = db_control.update_XFERO_Control(control_id, control_status)
        except Exception as err:
            logger.error(
                'Unable to update XFERO_Control from DB: Error %s',
                (err),
                exc_info=True)
            sys.exit(err)
    # If it is 'STOPPED'
    # Advise it is about to startup
    if control_status == 'STOPPED':
        logger.warning('The XFERO Scheduler is starting!')
        print('Starting scheduler')

    # Get rows from table
    logger.info('Retrieving Scheduled Tasks...')
    try:
        rows = db_schedule.get_activated_XFERO_Scheduled_Task()
    except Exception as err:
        logger.info(
            'Unable to get active Scheduled Task from DB: Error %s',
            (err),
            exc_info=True)
        sys.exit(err)

    counter = 1
    jobs = []

    sched = Scheduler(coalesce=True, daemonic=False)
    sched.add_listener(listener, sched.shutdown )

    # scheduled_task_id, scheduled_task_name, scheduled_task_function,
    # scheduled_task_year, scheduled_task_month, scheduled_task_day,
    # scheduled_task_week, scheduled_task_day_of_week,  scheduled_task_hour,
    # scheduled_task_minute, scheduled_task_second, scheduled_task_args,
    # scheduled_task_active FROM XFERO_Scheduled_Task WHERE
    # scheduled_task_active=?', ('1'))

    for task in rows:
        print('In for loop task')
        scheduled_task_id = task['scheduled_task_id']
        scheduled_task_name = task['scheduled_task_name']
        scheduled_task_function = task['scheduled_task_function']
        scheduled_task_year = task['scheduled_task_year']
        scheduled_task_month = task['scheduled_task_month']
        scheduled_task_day = task['scheduled_task_day']
        scheduled_task_week = task['scheduled_task_week']
        scheduled_task_day_of_week = task['scheduled_task_day_of_week']
        scheduled_task_hour = task['scheduled_task_hour']
        scheduled_task_minute = task['scheduled_task_minute']
        scheduled_task_second = task['scheduled_task_second']
        scheduled_task_args = task['scheduled_task_args']
        scheduled_task_active = task['scheduled_task_active']

        # job1 = sched.add_cron_job (job_function, day_of_week = 'mon-fri',
        # hour = '*', minute = '0-59 ', second ='*/20 ', args = ['hello'],
        # name="Hiya")
        f_module, f_func = scheduled_task_function.split('.')
        # print(f_module + '.' + f_func)

        if f_module == 'monitor':
            func = getattr(monitor, f_func)
        elif f_module == 'housekeeping':
            f_module = 'hk.housekeeping'
            func = getattr(housekeeping, f_func)
        elif f_module == 'xfero_stats':
            f_module = 'stats.xfero_stats'
            func = getattr(xfero_stats, f_func)

        print('Func = %s' % func)

        if scheduled_task_year == 'NULL':
            scheduled_task_year = None
        if scheduled_task_month == 'NULL':
            scheduled_task_month = None
        if scheduled_task_day == 'NULL':
            scheduled_task_day = None
        if scheduled_task_week == 'NULL':
            scheduled_task_week = None
        if scheduled_task_day_of_week == 'NULL':
            scheduled_task_day_of_week = None
        if scheduled_task_hour == 'NULL':
            scheduled_task_hour = None
        if scheduled_task_minute == 'NULL':
            scheduled_task_minute = None
        if scheduled_task_second == 'NULL':
            scheduled_task_second = None

        if scheduled_task_args == 'NULL':
            list_args = ''
        else:
            list_args = scheduled_task_args.split(',')

        job = 'Job_' + str(counter)
        jobs.append(job)

        # NOTE using __import__ returns the top-level name of the package
        # Using sys.modules allows us to make the function call

        __import__(f_module)
        mod = sys.modules[f_module]

        job = sched.add_cron_job(
            getattr(mod, f_func),
            year=scheduled_task_year,
            month=scheduled_task_month,
            day=scheduled_task_day,
            week=scheduled_task_week,
            day_of_week=scheduled_task_day_of_week,
            hour=scheduled_task_hour,
            minute=scheduled_task_minute,
            second=scheduled_task_second,
            args=list_args,
            name=scheduled_task_name)

        counter += 1
    sched.start()

    # Set XFERO_Control.control_status = 'STARTED'
    try:
        rows = db_control.update_XFERO_Control('1', 'STARTED')
    except Exception:
        logger.error('Unable to update Control Status from DB')

    # IN A LOOP
    # Now that scheduled tasks are running, we need to watch for requests to
    # shutdown.
    # Retrieve status from XFERO_Control where control_status = 'STOPPING'

    while True:
        print('Going to sleepies!!!')
        sleep(30)

        for job in jobs:
            logger.info('Running Job: %s', job)

        logger.info('Checking Control Status')
        try:
            rows = db_control.read_XFERO_Control('1')
        except Exception:
            logger.error('Unable to retrieve Control Status from DB')

        control_id = rows[0]
        control_status = rows[1]
        logger.info('Status = %s', control_status)
        # If XFERO_Control.control_status = 'STOPPING'
        if control_status == 'STOPPING':
            logger.info('Scheduler is shutting down')
            sched.shutdown(0)

            # Set XFERO_Control.control_status = 'STOPPED'
            try:
                rows = db_control.update_XFERO_Control('1', 'STOPPED')
            except Exception:
                logger.error('Unable to retrieve Control Status from DB')
            break


def f_dirmon(priority):
    '''
    dirmon function
    '''
    print('priority = ', priority)


def f_delete_old_files(purge_dir, fn_pattern, num_days, subdir=False):
    '''
    delete old files
    '''
    print(
        'purge_dir = %s : fn_pattern = %s : num_days = %s : subdir = %s',
        purge_dir,
        fn_pattern,
        num_days,
        subdir)


def listener(event):
    '''
    event listener
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

    logging.config.fileConfig(xfero_logger)
    # create logger
    logger = logging.getLogger('scheduler')
    if event.exception:
        logging.error('The job crashed')
    else:
        logging.info('The job worked')


def set_exit_handler(func):
    '''
    exit handler
    '''
    signal.signal(signal.SIGTERM, func)


def on_exit(sig, func=None):
    '''
    on exit function
    '''
    logging.info('exit handler triggered: %s : %s', sig, func)
    sys.exit(1)

if __name__ == '__main__':
    schedule()
