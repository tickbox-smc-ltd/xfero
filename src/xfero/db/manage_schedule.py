#!/usr/bin/env python

'''
**Purpose**

Module contains functions to manage the database table XFERO_Schduled_Task

**Unit Test Module:** test_crud_XFERO_Scheduled_Task.py

**Process Flow**

.. figure::  ../process_flow/manage_schedule.png
   :align:   center

   Process Flow: Manage Schedule

*External dependencies*

    /xfero/
      get_conf (/xfero/.db.manage_schedule)

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+
| 13/01/2014 | Chris Falck | Update error trapping, logging & refactored       |
+------------+-------------+---------------------------------------------------+
| 11/05/2014 | Chris Falck | Modified the function to ensure that database     |
|            |             | connections are opened and closed within the      |
|            |             | function call. This enables the function to be    |
|            |             | called in a multiprocessing environment.          |
+------------+-------------+---------------------------------------------------+
| 12/05/2014 | Chris Falck | New element passed on queue 'xfero_token'. Used in   |
|            |             | Logging.                                          |
+------------+-------------+---------------------------------------------------+
| 27/10/2014 | Chris Falck | modified call to get_conf                         |
+------------+-------------+---------------------------------------------------+

'''

import sqlite3 as lite
from /xfero/ import get_conf as get_conf
import logging.config

def create_XFERO_Scheduled_Task(scheduled_task_name, scheduled_task_function,
                             scheduled_task_year, scheduled_task_month,
                             scheduled_task_day, scheduled_task_week,
                             scheduled_task_day_of_week, scheduled_task_hour,
                             scheduled_task_minute, scheduled_task_second,
                             scheduled_task_args, scheduled_task_active,
                             xfero_token=False):
    '''

    **Purpose:**

    The function ```create_XFERO_Scheduled_Task``` is a script to insert rows into
    the XFERO_Scheduled_Task table.

    It performs the following SQL statement:

    ```'INSERT INTO XFERO_Scheduled_Task
    VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
    (scheduled_task_name, scheduled_task_function, scheduled_task_year,
    scheduled_task_month, scheduled_task_day, scheduled_task_week,
    scheduled_task_day_of_week, scheduled_task_hour, scheduled_task_minute,
    scheduled_task_second, scheduled_task_args, scheduled_task_active)```

    **Usage Notes:**

    None

    *Example usage:*

    ```create_XFERO_Scheduled_Task(scheduled_task_function, scheduled_task_year,
    scheduled_task_week, scheduled_task_day_of_week, scheduled_task_hour,
    scheduled_task_minute, scheduled_task_month, scheduled_task_day,
    scheduled_task_second, scheduled_task_name, scheduled_task_args,
    scheduled_task_active):```

    :param scheduled_task_name: Name of task
    :param scheduled_task_function: Function to be called
    :param scheduled_task_year: Year
    :param scheduled_task_month: Month
    :param scheduled_task_day: Day
    :param scheduled_task_week: Week
    :param scheduled_task_day_of_week: Day of week
    :param scheduled_task_hour: Hour
    :param scheduled_task_minute: Minute
    :param scheduled_task_second: Second
    :param scheduled_task_args: Arguments for the function
    :param scheduled_task_active: 0 = deactivated, 1 = Active - status of task
    :returns: Row Inserted

    '''
    try:
        (xfero_logger,.xfero_database, outbound_directory, transient_directory,
         error_directory, xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s' % err)
        raise err

    logging.config.fileConfig(xfero_logger)
    # create logger
    logger = logging.getLogger('database')

    logger.info('Retrieving settings from ini file')

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute('INSERT INTO XFERO_Scheduled_Task \
        VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (scheduled_task_name, scheduled_task_function,
                     scheduled_task_year, scheduled_task_month,
                     scheduled_task_day, scheduled_task_week,
                     scheduled_task_day_of_week, scheduled_task_hour,
                     scheduled_task_minute, scheduled_task_second,
                     scheduled_task_args, scheduled_task_active))
        con.commit()
    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Inserting row into XFERO_Scheduled_Task table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    # return cur
    cur.close()
    con.close()

    return 'Row Inserted'


def read_XFERO_Scheduled_Task(scheduled_task_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_Scheduled_Task``` is a script to retrieve a specific
    row from the XFERO_Scheduled_Task table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Scheduled_Task WHERE scheduled_task_id=?',
    (scheduled_task_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_XFERO_Scheduled_Task(scheduled_task_id)```

    :param scheduled_task_id: Identifying ID of the row
    :returns: rows: A Tuple of the selected rows.

    '''
    try:
        (xfero_logger,.xfero_database, outbound_directory, transient_directory,
         error_directory, xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s' % err)
        raise err

    logging.config.fileConfig(xfero_logger)
    # create logger
    logger = logging.getLogger('database')

    logger.info('Retrieving settings from ini file')

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute(
            'SELECT * FROM XFERO_Scheduled_Task \
            WHERE scheduled_task_id=?', (scheduled_task_id))
    except lite.Error as err:
        logger.error('Error Selecting row from XFERO_Scheduled_Task table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def update_XFERO_Scheduled_Task(scheduled_task_id, scheduled_task_name,
                             scheduled_task_function, scheduled_task_year,
                             scheduled_task_month, scheduled_task_week,
                             scheduled_task_day, scheduled_task_day_of_week,
                             scheduled_task_hour, scheduled_task_minute,
                             scheduled_task_second, scheduled_task_args,
                             scheduled_task_active, xfero_token=False):
    '''

    **Purpose:**

    The function ```update_XFERO_Scheduled_Task``` is a  SQL update script to
    update rows into the XFERO_Scheduled_Task table.

    It performs the following SQL statement:

    ```'UPDATE XFERO_Scheduled_Task SET scheduled_task_name=?,
    scheduled_task_function=?, scheduled_task_year=?, scheduled_task_month=?,
    scheduled_task_week=?, scheduled_task_day=?, scheduled_task_day_of_week=?,
    scheduled_task_hour=?, scheduled_task_minute=?, scheduled_task_second=?,
    scheduled_task_args=?, scheduled_task_active=?
    WHERE scheduled_task_id=?', (scheduled_task_name, scheduled_task_function,
    scheduled_task_year, scheduled_task_month, scheduled_task_week,
    scheduled_task_day, scheduled_task_day_of_week, scheduled_task_hour,
    scheduled_task_minute, scheduled_task_second, scheduled_task_args,
    scheduled_task_active, scheduled_task_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```update_XFERO_Scheduled_Task(scheduled_task_id, scheduled_task_name,
    scheduled_task_function, scheduled_task_year, scheduled_task_month,
    scheduled_task_week, scheduled_task_day, scheduled_task_day_of_week,
    scheduled_task_hour, scheduled_task_minute, scheduled_task_second,
    scheduled_task_args, scheduled_task_active)```

    :param scheduled_task_id: Identifying ID of the row
    :param scheduled_task_name: Name of task
    :param scheduled_task_function: Function to be called
    :param scheduled_task_year: Year
    :param scheduled_task_month: Month
    :param scheduled_task_day: Day
    :param scheduled_task_week: Week
    :param scheduled_task_day_of_week: Day of week
    :param scheduled_task_hour: Hour
    :param scheduled_task_minute: Minute
    :param scheduled_task_second: Second
    :param scheduled_task_args: Arguments for the function
    :param scheduled_task_active: 0 = deactivated, 1 = Active - status of task
    :returns: Success.

    '''
    try:
        (xfero_logger,.xfero_database, outbound_directory, transient_directory,
         error_directory, xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s' % err)
        raise err

    logging.config.fileConfig(xfero_logger)
    # create logger
    logger = logging.getLogger('database')

    logger.info('Retrieving settings from ini file')

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute('UPDATE XFERO_Scheduled_Task \
        SET scheduled_task_name=?, scheduled_task_function=?, \
        scheduled_task_year=?, scheduled_task_month=?, scheduled_task_week=?, \
        scheduled_task_day=?, scheduled_task_day_of_week=?, \
        scheduled_task_hour=?, scheduled_task_minute=?, \
        scheduled_task_second=?, scheduled_task_args=?, \
        scheduled_task_active=? WHERE scheduled_task_id=?',
                    (scheduled_task_name, scheduled_task_function,
                     scheduled_task_year, scheduled_task_month,
                     scheduled_task_week, scheduled_task_day,
                     scheduled_task_day_of_week, scheduled_task_hour,
                     scheduled_task_minute, scheduled_task_second,
                     scheduled_task_args, scheduled_task_active,
                     scheduled_task_id))
        con.commit()
    except lite.Error as err:
        if con:
            con.rollback()

        logger.error('Error Updating row on XFERO_Scheduled_Task table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def delete_XFERO_Scheduled_Task(scheduled_task_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```delete_XFERO_Scheduled_Task``` s a script to delete a specific
    row from the XFERO_Scheduled_Task table.

    It performs the following SQL statement:

    ```'DELETE FROM XFERO_Scheduled_Task WHERE scheduled_task_id=?',
    (scheduled_task_id,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```delete_XFERO_Scheduled_Task(scheduled_task_id)```

    :param scheduled_task_id: Identifying ID of the row
    :returns: Success

    '''
    try:
        (xfero_logger,.xfero_database, outbound_directory, transient_directory,
         error_directory, xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s' % err)
        raise err

    logging.config.fileConfig(xfero_logger)
    # create logger
    logger = logging.getLogger('database')

    logger.info('Retrieving settings from ini file')

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute(
            'DELETE FROM XFERO_Scheduled_Task \
            WHERE scheduled_task_id=?', (scheduled_task_id,))
        con.commit()
    except lite.Error as err:
        if con:
            con.rollback()

        logger.error('Error Deleting row from XFERO_Scheduled_Task table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def list_XFERO_Scheduled_Task(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Scheduled_Task``` is a script to retrieve all rows
    from the XFERO_Scheduled_Task table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Scheduled_Task'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Scheduled_Task()```

    :param NONE: No parameters are passed to this function
    :returns: rows: A Tuple of the selected rows.

    '''
    try:
        (xfero_logger,.xfero_database, outbound_directory, transient_directory,
         error_directory, xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s' % err)
        raise err

    logging.config.fileConfig(xfero_logger)
    # create logger
    logger = logging.getLogger('database')

    logger.info('Retrieving settings from ini file')

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute('SELECT * FROM XFERO_Scheduled_Task')
        con.commit()
    except lite.Error as err:
        logger.error('Error Selecting rows from XFERO_Scheduled_Task table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def get_activated_XFERO_Scheduled_Task(xfero_token=False):
    '''

    **Purpose:**

    The function ```get_activated_XFERO_Scheduled_Task``` is a to retrieve all
    active rows from the XFERO_Scheduled_Task table.

    It performs the following SQL statement:

    ```'SELECT scheduled_task_id, scheduled_task_name, scheduled_task_function,
    scheduled_task_year, scheduled_task_month, scheduled_task_day,
    scheduled_task_week, scheduled_task_day_of_week,  scheduled_task_hour,
    scheduled_task_minute, scheduled_task_second, scheduled_task_args,
    scheduled_task_active
    FROM XFERO_Scheduled_Task WHERE scheduled_task_active=?', ('1')```

    **Usage Notes:**

    None

    *Example usage:*

    ```get_activated_XFERO_Scheduled_Task()```

    :param NONE: No parameters passed
    :returns: rows: A Tuple of the selected rows.

    '''
    try:
        (xfero_logger,.xfero_database, outbound_directory, transient_directory,
         error_directory, xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s' % err)
        raise err

    logging.config.fileConfig(xfero_logger)
    # create logger
    logger = logging.getLogger('database')

    logger.info('Retrieving settings from ini file')

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        con.row_factory = lite.Row
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute(
            'SELECT scheduled_task_id, scheduled_task_name, \
            scheduled_task_function, scheduled_task_year, \
            scheduled_task_month, scheduled_task_day, scheduled_task_week, \
            scheduled_task_day_of_week,  scheduled_task_hour, \
            scheduled_task_minute, scheduled_task_second, scheduled_task_args, \
            scheduled_task_active FROM XFERO_Scheduled_Task \
            WHERE scheduled_task_active=?', ('1'))
    except lite.Error as err:
        logger.error('Error Selecting row from XFERO_Scheduled_Task table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows

def get_deactivated_XFERO_Scheduled_Task(scheduled_task_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```get_deactivated_XFERO_Scheduled_Task``` is a to retrieve all
    active rows into the XFERO_Scheduled_Task table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Scheduled_Task WHERE scheduled_task_active=?', (1)```

    **Usage Notes:**

    None

    *Example usage:*

    ```get_activated_XFERO_Scheduled_Task()```

    :param NONE: No parameters passed
    :returns: rows: A Tuple of the selected rows.

    '''
    try:
        (xfero_logger,.xfero_database, outbound_directory, transient_directory,
         error_directory, xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s' % err)
        raise err

    logging.config.fileConfig(xfero_logger)
    # create logger
    logger = logging.getLogger('database')

    logger.info('Retrieving settings from ini file')

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute(
            'SELECT * FROM XFERO_Scheduled_Task \
            WHERE scheduled_task_active=?', (1))
    except lite.Error as err:
        logger.error('Error Selecting row from XFERO_Scheduled_Task table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows

if __name__ == "__main__":

    for t in [('High Priority Xfers', 'monitor.dirmon', '', '', '', '',
               'mon-sun', '*', '*/10', '', '1', '1'),]:

        (scheduled_task_name, scheduled_task_function, scheduled_task_year,
         scheduled_task_month, scheduled_task_day, scheduled_task_week,
         scheduled_task_day_of_week, scheduled_task_hour, scheduled_task_minute,
         scheduled_task_second, scheduled_task_args, scheduled_task_active) = t

        result = create_XFERO_Scheduled_Task(scheduled_task_name,
                                          scheduled_task_function,
                                          scheduled_task_year,
                                          scheduled_task_month,
                                          scheduled_task_day,
                                          scheduled_task_week,
                                          scheduled_task_day_of_week,
                                          scheduled_task_hour,
                                          scheduled_task_minute,
                                          scheduled_task_second,
                                          scheduled_task_args,
                                          scheduled_task_active)
    print(result)
