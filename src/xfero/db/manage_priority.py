#!/usr/bin/env python

'''
**Purpose**

Module contains functions to manage the database table XFERO_Priority

**Unit Test Module:** test_crud_XFERO_Priority.py

**Process Flow**

.. figure::  ../process_flow/manage_priority.png
   :align:   center

   Process Flow: Manage Priority
   
*External dependencies*

    os (/xfero/.db.manage_priority)
    /xfero/ 
      get_conf (/xfero/.db.manage_priority)

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+
| 13/01/2014 | Chris Falck | Update error trapping, logging & refactored       |
+------------+-------------+---------------------------------------------------+
| 03/05/2014 | Chris Falck | Added new column to accommodate threading of      |
|            |             | monitor process.                                  |
+------------+-------------+---------------------------------------------------+
| 11/05/2014 | Chris Falck | Modified the function to ensure that database     |
|            |             | connections are opened and closed within the      |
|            |             | function call. This enables the function to be    |
|            |             | called in a multiprocessing environment.          |
+------------+-------------+---------------------------------------------------+
| 12/05/2014 | Chris Falck | New element passed on queue 'xfero_token'. Used in   |
|            |             | Logging.                                          |
+------------+-------------+---------------------------------------------------+
| 27/09/2014 | Chris Falck | modified call to get_conf                         |
+------------+-------------+---------------------------------------------------+
| 16/10/2014 | Chris Falck | Updated because XFERO_Priority table has changed to  |
|            |             | remove the column priority_worker_threads         |
+------------+-------------+---------------------------------------------------+

'''

import sqlite3 as lite
from /xfero/ import get_conf as get_conf
import logging.config

def create_XFERO_Priority(priority_level, priority_detail, xfero_token=False):
    '''

    **Purpose:**

    The function ```create_XFERO_Priority``` is a script to insert a row into the
    XFERO_Priority table.

    It performs the following SQL statement:

    ```'INSERT INTO XFERO_Priority VALUES(?, ?)',
    (priority_level, priority_detail)```

    **Usage Notes:**

    None

    *Example usage:*

    ```create_XFERO_Priority(priority_level, priority_detail)```

    :param priority_level: Degree of Priority
    :param priority_detail: Description of Priority e.g. High, Medium, Low
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

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute('INSERT INTO XFERO_Priority VALUES(?, ?)',
                    (priority_level, priority_detail))
        con.commit()
    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Inserting row into XFERO_Priority table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    # return cur
    cur.close()
    con.close()

    return 'Row Inserted'


def read_XFERO_Priority(priority_level, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_Priority``` is a script to retrieve a specific row
    from the XFERO_Priority table.

    It performs the following SQL statement:

    ```'SELECT priority_level, priority_detail FROM XFERO_Priority
    WHERE priority_level=?', (priority_level)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_XFERO_Priority(priority_level)```

    :param priority_level: Degree of Priority
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

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute(
            'SELECT priority_level, priority_detail \
            FROM XFERO_Priority \
            WHERE priority_level=?', (priority_level))
    except lite.Error as err:

        logger.error('Error Selecting row into XFERO_Partner table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def read_XFERO_Priority_level(priority_detail, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_Priority_level``` is a script to retrieve a specific
    row from the XFERO_Priority table by priority_detail.

    It performs the following SQL statement:

    ```'SELECT priority_level from XFERO_Priority WHERE priority_detail=?',
    [priority_detail]```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_XFERO_Priority_level(priority_detail)```

    :param priority_detail: Description of Priority e.g. High, Medium, Low
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

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute('SELECT priority_level from XFERO_Priority \
        WHERE priority_detail=?', [priority_detail])
    except lite.Error as err:

        logger.error('Error Selecting row into XFERO_Partner table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def update_XFERO_Priority(priority_level, priority_detail, xfero_token=False):
    '''

    **Purpose:**

    The function ```update_XFERO_Priority``` is a  SQL update script to update
    rows into the XFERO_Priority table.

    It performs the following SQL statement:

    ```'UPDATE XFERO_Priority SET priority_detail=?, priority_worker_threads=?
    WHERE priority_level=?', (priority_detail, priority_level)```

    **Usage Notes:**

    None

    *Example usage:*

    ```update_XFERO_Priority(priority_level, priority_worker_threads,
    priority_detail)```

    :param priority_level: Degree of Priority
    :param priority_detail: Description of Priority e.g. High, Medium, Low
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

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute('UPDATE XFERO_Priority SET priority_detail=?, \
        priority_worker_threads=? WHERE priority_level=?',
                    (priority_detail, priority_level))
        con.commit()
    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Updating row on XFERO_Priority table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def delete_XFERO_Priority(priority_level, xfero_token=False):
    '''

    **Purpose:**

    The function ```delete_XFERO_Priority``` is a script to delete a specific row
    from the XFERO_Priority table.

    It performs the following SQL statement:

    ```'DELETE FROM XFERO_Priority WHERE priority_level=?', (priority_level,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```delete_XFERO_Priority(priority_level)```

    :param priority_level: Primary Key ID which identifies the row to update
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

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute(
            'DELETE FROM XFERO_Priority WHERE priority_level=?', (priority_level,))
        con.commit()
    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error deleting row on XFERO_Priority table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def list_XFERO_Priority(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Priority``` is a script to retrieve all rows from
    the XFERO_Priority table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Priority'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Priority()```

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

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute('SELECT * FROM XFERO_Priority')
        con.commit()
    except lite.Error as err:

        logger.error('Error Selecting row on XFERO_Priority table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def list_XFERO_Priority_detail(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Priority_detail``` is a script to retrieve all rows
    from the XFERO_Partner table ordered BY priority_level ascending.

    It performs the following SQL statement:

    ```'SELECT priority_detail FROM XFERO_Priority ORDER BY priority_level ASC'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Priority_detail()```

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

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute(
            'SELECT priority_detail \
            FROM XFERO_Priority ORDER BY priority_level ASC')
        con.commit()
    except lite.Error as err:

        logger.error('Error Selecting row on XFERO_Priority table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def list_XFERO_Priority_Asc(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Priority_Asc``` is a script to retrieve all rows
    from the XFERO_Priority table by ascending Priority level.

    It performs the following SQL statement:

    ```'SELECT priority_level FROM XFERO_Priority ORDER BY priority_level ASC'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Priority()```

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

    db_location = xfero_database

    try:
        con = lite.connect(db_location)
        cur = con.cursor()
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute(
            'SELECT priority_level \
            FROM XFERO_Priority ORDER BY priority_level ASC')
        con.commit()
    except lite.Error as err:

        logger.error('Error Selecting row on XFERO_Priority table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows

if __name__ == "__main__":

    priority_level = '6'
    priority_detail = 'High'
    read_XFERO_Priority_level(priority_detail)
