#!/usr/bin/env python

'''
**Purpose**

Module contains functions to manage the database table XFERO_Function

**Unit Test Module:** test_crud_XFERO_Function.py

External dependencies

    os (/xfero/.db.manage_function)
    /xfero/
      get_conf (/xfero/.db.manage_function)

**Process Flow**

.. figure::  ../process_flow/manage_function.png
   :align:   center

   Process Flow: Manage Function

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+
| 09/01/2014 | Chris Falck | Update error trapping, logging & refactored       |
+------------+-------------+---------------------------------------------------+
| 10/05/2014 | Chris Falck | Modified the function to ensure that database     |
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
import os
import sys


def create_XFERO_Function(function_name, function_class, function_description,
                       function_prototype, xfero_token=False):
    '''

    **Purpose:**

    The function ```create_XFERO_Function``` is a script to insert rows into the
    XFERO_Function table.

    It performs the following SQL statement:

    ```'INSERT INTO XFERO_Function VALUES(NULL, ?, ?, ?)', (function_name,
    function_class, function_description, function_prototype)```

    **Usage Notes:**

    None

    *Example usage:*

    ```create_XFERO_Function(function_name, function_class, function_description,
    function_prototype)```

    :param function_name: Name of function call
    :param function_class: Name of class
    :param function_description: Description of function
    :param function_prototype: Contains the argument prototype to the function
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
        cur.execute('INSERT INTO XFERO_Function VALUES(NULL, ?, ?, ?, ?)',
                    (function_name, function_class,
                     function_description, function_prototype))
        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Inserting row into XFERO_Function table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    # return cur
    cur.close()
    con.close()

    return 'Row Inserted'


def read_XFERO_Function(function_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_Function```  is a script to retrieve a specific row
    from the XFERO_Function table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Function WHERE function_id=?', (function_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_XFERO_Function(function_id)```

    :param function_id: Identifying ID of the row
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
            'SELECT * FROM XFERO_Function WHERE function_id=?', (function_id))
    except lite.Error as err:
        logger.error('Error Selecting row into XFERO_Function table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def read_with_name_XFERO_Function(function_name, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_with_name_XFERO_Function``` is a script to retrieve a
    specific row from
    the XFERO_Function table by the function_name.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Function WHERE function_name=?', (function_name,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_with_name_XFERO_Function(function_name)```

    :param function_name: Name of the function
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
            'SELECT * FROM XFERO_Function WHERE function_name=?', (function_name,))
    except lite.Error as err:
        logger.error('Error Selecting row into XFERO_Function table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def update_XFERO_Function(function_id, function_class, function_name,
                       function_description, function_prototype,
                       xfero_token=False):
    '''

    **Purpose:**

    The function ```update_XFERO_Function``` is a script to update a specific row
    on the XFERO_Function table.

    It performs the following SQL statement:

    ```'UPDATE XFERO_Function SET function_name=?, function_class=?,
    function_description=?, function_prototype=?
    WHERE function_id=?', (function_name, function_class, function_description,
    function_prototype, function_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```update_XFERO_Function(function_id, function_name, function_class,
    function_description, function_prototype)```

    :param function_id: Primary Key ID which identifies the row to retrieve
    :param function_name: Name of function call
    :param function_class: Name of class
    :param function_description: Description of function
    :param function_prototype: Contains the argument prototype to the function
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
        cur.execute('UPDATE XFERO_Function \
        SET function_name=?, \
        function_class=?, \
        function_description=?, \
        function_prototype=? \
        WHERE function_id=?',
                    (function_name, function_class, function_description,
                     function_prototype, function_id))
        con.commit()
    except lite.Error as err:
        if con:
            con.rollback()

        logger.error('Error updating row into XFERO_Function table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def delete_XFERO_Function(function_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```delete_XFERO_Function``` is a script to delete a specific row
    from the XFERO_Function table.

    It performs the following SQL statement:

    ```cur.execute('DELETE FROM XFERO_Function WHERE function_id=?',
    (function_id,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```delete_XFERO_Function(function_id)```

    :param function_id: Primary Key ID which identifies the row to retrieve
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
            'DELETE FROM XFERO_Function WHERE function_id=?', (function_id,))
        con.commit()
    except lite.Error as err:
        if con:
            con.rollback()

        logger.error('Error deleting row into XFERO_Function table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def list_XFERO_Function(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Function``` is a script to retrieve all rows from
    the XFERO_Function table.

    It performs the following SQL statement:

    ```cur.execute('SELECT * FROM XFERO_Function')```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Function()```

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
        cur.execute('SELECT * FROM XFERO_Function')
        con.commit()
    except lite.Error as err:
        logger.error('Error selecting row from XFERO_Function table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()
    return rows


def list_fname_XFERO_Function(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_fname_XFERO_Function``` is a script to retrieve all rows
    from the XFERO_Function table. It retrieves the function names and their class
    from the table

    It performs the following SQL statement:

    ```'SELECT function_name, function_class FROM XFERO_Function'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_fname_XFERO_Function()```

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
        cur.execute('SELECT function_name, function_class FROM XFERO_Function')
        con.commit()
    except lite.Error as err:
        logger.error('Error selecting row from XFERO_Function table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()
    return rows
