#!/usr/bin/env python

'''
**Purpose**

Module contains functions to manage the database table XFERO_Control

**Unit Test Module:** test_crud_XFERO_Control.py

**Process Flow**

.. figure::  ../process_flow/manage_control.png
   :align:   center

   Process Flow: Manage Control

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+
| 09/01/2014 | Chris Falck | Update error trapping, logging & refactored       |
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
| 16/10/2014 | Chris Falck | Updated because XFERO_Control table has changed to   |
|            |             | add the column control_num_threads                |
+------------+-------------+---------------------------------------------------+

'''

import sqlite3 as lite
from /xfero/ import get_conf as get_conf
import logging.config
import os
import sys


def create_XFERO_Control(control_status, control_key, control_passphrase,
                      control_num_threads, xfero_token=False):
    '''

    **Purpose:**

    The function ```create_XFERO_Control``` is a script to insert rows into the
    XFERO_Control table.

    It performs the following SQL statement:

    ```'INSERT INTO XFERO_Control VALUES(NULL, ?, ?, ?, ?)', (control_status,
    control_key, control_passphrase, control_num_threads,))```

    **Usage Notes:**

    None

    *Example usage:*

    ```create_XFERO_Control(control_status, control_key, control_passphrase)```

    :param control_status: Status. Accepted values = Running, Stopped, Starting
    :param control_key: Private Key of XFERO Server
    :param control_passphrase: Passphrase for Private Key
    :param control_num_threads: Number of worker threads for this priority
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
        cur.execute('INSERT INTO XFERO_Control VALUES(NULL, ?, ?, ?, ?)',
                    (control_status, control_key, control_passphrase,
                     control_num_threads,))
        con.commit()

    except lite.Error as err:
        if con:
            con.rollback()

        logger.error('Error Inserting row into XFERO_Control table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    # return cur
    cur.close()
    con.close()

    return 'Row Inserted'


def read_XFERO_Control(control_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_Control``` is a script to retrieve a specific row
    from the XFERO_Control table. It uses a connection row factory to enable column
    names to be returned

    It performs the following SQL statement:

    ```SELECT control_id, control_status, control_pgp_priv_key,
    control_pgp_passphrase FROM XFERO_Control WHERE control_id=?', (control_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_XFERO_Control(control_id)```

    :param control_id: Primary Key ID which identifies the row to retrieve
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
        con.row_factory = lite.Row
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute(
            'SELECT control_id, \
            control_status, \
            control_pgp_priv_key, \
            control_pgp_passphrase, \
            control_num_threads \
            FROM XFERO_Control WHERE control_id=?', (control_id,))

    except lite.Error as err:

        logger.error('Error selecting row from XFERO_Control table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def read_XFERO_Control_monitor(control_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_Control_monitor``` is a script based on
    ```read_XFERO_Control_monitor``` but does not return column names. Its purpose
    is to retrieve a specific row from the XFERO_Control table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Control WHERE control_id=?', (control_id,))```

    **Usage Notes:**

    NONE

    *Example usage:*

    ```read_XFERO_Control(control_id)```

    :param control_id: Primary Key ID which identifies the row to retrieve
    :returns: rows: A Tuple of the selected rows.

    *External dependencies*

    os (/xfero/.db.manage_control)
    /xfero/
      get_conf (/xfero/.db.manage_control)

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
            'SELECT * FROM XFERO_Control WHERE control_id=?', (control_id,))

    except lite.Error as err:

        logger.error('Error selecting row from XFERO_Control table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()
    cur.close()
    con.close()

    return rows


def update_XFERO_Control(control_id, control_status, xfero_token=False):
    '''

    **Purpose:**

    The function ```update_XFERO_Control``` is a script to update a specific row on
    the XFERO_Control table.

    It performs the following SQL statement:

    ```'UPDATE XFERO_Control SET control_status=? WHERE control_id=?',
    (control_status, control_id)```

    **Usage Notes:**

    NONE

    *Example usage:*

    ```update_XFERO_Control(control_id, control_status)```

    :param control_id: Primary Key ID which identifies the row to retrieve
    :param control_status: Status. Accepted values = Running, Stopped, Starting
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
            'UPDATE XFERO_Control SET control_status=? WHERE control_id=?',
            (control_status, control_id))
        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error updating row in XFERO_Control table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def update_pgp_XFERO_Control(control_id, control_status, control_pgp_priv_key,
                          control_pgp_passphrase, control_num_threads,
                          xfero_token=False):
    '''

    **Purpose:**

    The function ```update_XFERO_Control``` is a script to update a specific row on
    the XFERO_Control table.

    It performs the following SQL statement:

    ```'UPDATE XFERO_Control SET control_status=?, control_pgp_priv_key=?,
    control_pgp_passphrase=?, control_num_threads=? WHERE control_id=?',
    (control_status, control_pgp_priv_key, control_pgp_passphrase,
    control_num_threads, control_id)```

    **Usage Notes:**

    NONE

    *Example usage:*

    ```update_XFERO_Control(control_id, control_status, control_pgp_priv_key,
    control_pgp_passphrase)```

    :param control_id: Primary Key ID which identifies the row to retrieve
    :param control_status: Status. Accepted values = Running, Stopped, Starting
    :param control_pgp_priv_key: Private Key of XFERO Installation
    :param control_pgp_passphrase: Passphrase of Private Key
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
        cur.execute('UPDATE XFERO_Control \
                    SET \
                    control_status=?, \
                    control_pgp_priv_key=?, \
                    control_pgp_passphrase=?, \
                    control_num_threads=? \
                    WHERE control_id=?',
                    (control_status,
                     control_pgp_priv_key,
                     control_pgp_passphrase,
                     control_num_threads,
                     control_id))
        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error updating row in XFERO_Control table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def delete_XFERO_Control(control_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```delete_XFERO_Control``` is a script to delete a specific row
    from the XFERO_Control table.

    It performs the following SQL statement:

    ```'DELETE FROM XFERO_Control WHERE control_id=?', (control_id,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```delete_XFERO_Control(control_id)```

    :param control_id: Primary Key ID which identifies the row to retrieve
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
        cur.execute('DELETE FROM XFERO_Control WHERE control_id=?', (control_id,))
        con.commit()

    except lite.Error as e:

        if con:
            con.rollback()

        logger.error('Error deleting row from XFERO_Control table: %s. \
        (XFERO_Token=%s)', e.args[0], xfero_token)
        raise e

    cur.close()
    con.close()

    return 'Success'


def list_XFERO_Control(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Control``` is a script to retrieve all rows from
    the XFERO_Control table. It uses a connection row factory to enable column
    names to be returned.

    It performs the following SQL statement:

    ```'SELECT control_id, control_status FROM XFERO_Control'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Control()```

    :param NONE: No parameters are passed to this function
    :returns: rows: Tuple containing the rows returned.

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
        con.row_factory = lite.Row
        cur = con.execute("pragma foreign_keys=ON")
        cur.execute(
            'SELECT control_id, \
            control_status, \
            control_pgp_priv_key, \
            control_pgp_passphrase, \
            control_num_threads \
            FROM XFERO_Control')
        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error selecting all rows from XFERO_Control table: %s. \
        (XFERO_Token=%s)' % (err.args[0], xfero_token))
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def list_XFERO_All_Control(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_All_Control``` is a script to retrieve all rows from
    the XFERO_Control table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_AV_Pattern'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_All_Control()```

    :param NONE: No parameters are passed to this function
    :returns: rows: Tuple containing the rows returned.

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
        cur.execute('SELECT * FROM XFERO_Control')
        con.commit()

    except lite.Error as err:
        if con:
            con.rollback()

        logger.error('Error selecting all rows from XFERO_Control table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


if __name__ == "__main__":

    # for t in [('START',), ('STOP',),
    #              ]:

            # control_status = t

            # create_XFERO_Control(control_status)

    rows = read_XFERO_Control('1')

    print(rows[0])
    print(rows[1])
    print(rows[2])
    print(rows[3])
