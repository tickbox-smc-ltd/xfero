#!/usr/bin/env python
'''
**Purpose**

Module contains functions to manage the database table XFERO_COTS_Pattern

**Unit Test Module:** test_crud_XFERO_COTS_Pattern.py

**Process Flow**

.. figure::  ../process_flow/manage_cots_patterns.png
   :align:   center

   Process Flow: Manage COTS Pattern

*External dependencies*

    /xfero/
      get_conf (/xfero/.db.manage_cots_pattern)

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

'''

import sqlite3 as lite
from /xfero/ import get_conf as get_conf
import logging.config

def create_XFERO_COTS_Pattern(cotspattern_product, cotspattern_pattern_name,
                           cotspattern_prototype, xfero_token=False):
    '''

    **Purpose:**

    The function ```create_XFERO_COTS_Pattern``` is a script to insert a row into
    the XFERO_COTS_Pattern table.

    It performs the following SQL statement:

    ```'INSERT INTO XFERO_COTS_Pattern VALUES(NULL, ?, ?, ?)',
    (cotspattern_product,cotspattern_pattern_name, cotspattern_prototype)```

    **Usage Notes:**

    None

    *Example usage:*

    ```create_XFERO_COTS_Pattern(cotspattern_product, cotspattern_pattern_name,
    cotspattern_prototype)```

    :param cotspattern_product: Name of COTS Product
    :param cotspattern_pattern_name: Pattern name
    :param cotspattern_prototype: Contains the command line prototype to the
    COTS product
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
        cur.execute('INSERT INTO XFERO_COTS_Pattern VALUES(NULL, ?, ?, ?)',
                    (cotspattern_product, cotspattern_pattern_name,
                     cotspattern_prototype))
        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Inserting row into XFERO_COTS_Pattern table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    # return cur
    cur.close()
    con.close()

    return 'Row Inserted'


def read_XFERO_COTS_Pattern(cotspattern_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_COTS_Pattern``` is a script to retrieve a specific
    row from the XFERO_COTS_Pattern table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_COTS_Pattern
    WHERE cotspattern_id=?', (cotspattern_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_XFERO_COTS_Pattern(cotspattern_id)```

    :param cotspattern_id: Primary Key ID which identifies the row to retrieve
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
            'SELECT * FROM XFERO_COTS_Pattern \
            WHERE cotspattern_id=?', (cotspattern_id))

    except lite.Error as err:

        logger.error('Error Selecting row from XFERO_COTS_Pattern table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def read_cpn_XFERO_COTS_Pattern(cotspattern_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_cpn_XFERO_COTS_Pattern``` is a script to retrieve a
    specificrow from the XFERO_COTS_Pattern table. It is based on
    read_XFERO_COTS_Pattern but only returns the cotspattern_prototype

    It performs the following SQL statement:

    ```'SELECT cotspattern_prototype FROM XFERO_COTS_Pattern
    WHERE cotspattern_id=?', (cotspattern_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_cpn_XFERO_COTS_Pattern(cotspattern_id)```

    :param cotspattern_id: Primary Key ID which identifies the row to retrieve
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
            'SELECT cotspattern_prototype FROM \
            XFERO_COTS_Pattern WHERE cotspattern_id=?', (cotspattern_id))

    except lite.Error as err:
        logger.error('Error Selecting row from XFERO_COTS_Pattern table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def read_with_name_XFERO_COTS_Pattern(cotspattern_pattern_name, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_with_name_XFERO_COTS_Pattern``` is a script to retrieve a
    specific row from the XFERO_COTS_Pattern table that matched the COTS Pattern
    Name supplied.

    It performs the following SQL statement:

    ```'SELECT cotspattern_id, cotspattern_product, cotspattern_pattern_name,
    cotspattern_prototype  FROM XFERO_COTS_Pattern
    WHERE cotspattern_pattern_name=?', (cotspattern_pattern_name,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_XFERO_COTS_Pattern(cotspattern_pattern_name)```

    :param cotspattern_pattern_name: which identifies the row to retrieve
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
            'SELECT cotspattern_id, \
            cotspattern_product, \
            cotspattern_pattern_name, \
            cotspattern_prototype  \
            FROM XFERO_COTS_Pattern \
            WHERE cotspattern_pattern_name=?', (cotspattern_pattern_name,))

    except lite.Error as err:

        logger.error('Error Selecting row from XFERO_COTS_Pattern table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def update_XFERO_COTS_Pattern(cotspattern_id, cotspattern_product,
                           cotspattern_pattern_name,
                           cotspattern_prototype, xfero_token=False):
    '''

    **Purpose:**

    The function ```update_XFERO_COTS_Pattern``` is a script to update a specific
    row on the XFERO_COTS_Pattern table.

    It performs the following SQL statement:

    ```cur.execute('UPDATE XFERO_COTS_Pattern SET cotspattern_product=?,
    cotspattern_pattern_name=?, cotspattern_prototype=? WHERE cotspattern_id=?',
    (cotspattern_product, cotspattern_pattern_name, cotspattern_prototype,
    cotspattern_id))```

    **Usage Notes:**

    *Example usage:*

    ```'UPDATE XFERO_COTS_Pattern SET cotspattern_product=?,
    cotspattern_pattern_name=?, cotspattern_prototype=?
    WHERE cotspattern_id=?', (cotspattern_product, cotspattern_pattern_name,
    cotspattern_prototype, cotspattern_id)```

    :param cotspattern_id: Primary Key ID which identifies the row to retrieve
    :param cotspattern_product: Name of COTS Product
    :param cotspattern_pattern_name: Pattern name
    :param cotspattern_prototype: Contains the command line prototype to the
    COTS product
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
        cur.execute('UPDATE XFERO_COTS_Pattern \
        SET cotspattern_product=?, \
        cotspattern_pattern_name=?, \
        cotspattern_prototype=? \
        WHERE cotspattern_id=?', (cotspattern_product, cotspattern_pattern_name,
                                  cotspattern_prototype, cotspattern_id))

        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Selecting row from XFERO_COTS_Pattern table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def delete_XFERO_COTS_Pattern(cotspattern_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```delete_XFERO_COTS_Pattern``` is a script to delete a specific
    row from the XFERO_COTS_Pattern table.

    It performs the following SQL statement:

    ```cur.execute('DELETE FROM XFERO_COTS_Pattern
    WHERE cotspattern_id=?', (cotspattern_id,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```delete_XFERO_COTS_Pattern(cotspattern_id)```

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
        cur.execute(
            'DELETE FROM XFERO_COTS_Pattern \
            WHERE cotspattern_id=?', (cotspattern_id,))

        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()
        logger.error('Error selecting all rows from XFERO_COTSPattern table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def list_XFERO_COTS_Pattern(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_COTS_Pattern``` is a script to retrieve all rows
    from the XFERO_COTS_Pattern table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_COTS_Pattern'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_COTS_Pattern()```

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
        cur.execute('SELECT * FROM XFERO_COTS_Pattern')
        con.commit()

    except lite.Error as err:

        logger.error('Error selecting all rows from XFERO_COTS_Pattern table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def list_all_patterns_XFERO_COTS_Pattern(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_all_patterns_XFERO_COTS_Pattern``` is a script to retrieve
    the pattern names from all rows in the XFERO_COTS_Pattern table.

    It performs the following SQL statement:

    ```'SELECT cotspattern_pattern_name FROM XFERO_COTS_Pattern'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_all_patterns_XFERO_COTS_Pattern()```

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
        cur.execute('SELECT cotspattern_pattern_name FROM XFERO_COTS_Pattern')
        con.commit()

    except lite.Error as err:

        logger.error('Error selecting all rows from XFERO_COTSPattern table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows

if __name__ == "__main__":

    rows = read_XFERO_COTS_Pattern('1',)
    for row in rows:
        print(row)

    rows = read_with_name_XFERO_COTS_Pattern('SFTPPlus',)
    for row in rows:
        print(row)
    print(rows[0])
