#!/usr/bin/env python

'''
**Purpose**

Module contains functions to manage the database table XFERO_Route

**Unit Test Module:** test_crud_XFERO_Route.py

**Process Flow**

.. figure::  ../process_flow/manage_route.png
   :align:   center

   Process Flow: Manage Route

*External dependencies*

    /xfero/
      get_conf (/xfero/.db.manage_route)

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
| 27/09/2014 | Chris Falck | modified call to get_conf                         |
+------------+-------------+---------------------------------------------------+
| 16/10/2014 | Chris Falck | Created a new function called count_XFERO_Route      |
+------------+-------------+---------------------------------------------------+

'''

import sqlite3 as lite
from /xfero/ import get_conf as get_conf
import logging.config

def create_XFERO_Route(route_monitoreddir, route_filenamepattern, route_active,
                    route_priority, xfero_token=False):
    '''

    **Purpose:**

    The function ```create_XFERO_Route``` is a script to retrieve a specific row
    from the XFERO_Route table.

    It performs the following SQL statement:

    ```'INSERT INTO XFERO_Route VALUES(NULL, ?, ?, ?, ?)', (route_monitoreddir,
    route_filenamepattern, route_active, route_priority)```

    **Usage Notes:**

    None

    *Example usage:*

    ```create_XFERO_Route(route_monitoreddir, route_filenamepattern, route_active,
    route_priority)```

    :param route_monitoreddir: Directory to be monitored
    :param route_filenamepattern: Filname pattern match
    :param route_active: Status of route. 0 = deactivated, 1 = active
    :param route_priority: Priority of the route
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
        con.row_factory = lite.Row
        cur = con.execute("pragma foreign_keys=ON")
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('INSERT INTO XFERO_Route VALUES(NULL, ?, ?, ?, ?)',
                    (route_monitoreddir, route_filenamepattern, route_active,
                     route_priority))
        con.commit()
        inserted_id = cur.lastrowid

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Inserting row into XFERO_Route table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    # return cur
    cur.close()
    con.close()

    return inserted_id


def read_XFERO_Route(route_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_Route``` is a script to retrieve a specific row from
    the XFERO_Route table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Route WHERE route_id=?', (route_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_XFERO_Route(route_id)```

    :param route_id: Identifying ID of the row
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
        # con.row_factory = lite.Row
        cur = con.execute("pragma foreign_keys=ON")
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('SELECT * FROM XFERO_Route WHERE route_id=?', (route_id))
    except lite.Error as err:
        logger.error('Error Selecting row into XFERO_Route table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows

def update_XFERO_Route(route_monitoreddir, route_filenamepattern, route_active,
                    route_priority, route_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```update_XFERO_Route``` is a  SQL update script to update
    rows into the XFERO_Route table.

    It performs the following SQL statement:

    ```'UPDATE XFERO_Route SET route_monitoreddir=?, route_filenamepattern=?,
    route_active = ?, route_priority=?  WHERE route_id=?', (route_monitoreddir,
    route_filenamepattern, route_active, route_priority, route_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```update_XFERO_Route(route_monitoreddir, route_filenamepattern, route_active,
    route_priority, route_id)```

    :param route_id: Identifying ID of the row
    :param route_monitoreddir: Directory to be monitored
    :param route_filenamepattern: Filname pattern match
    :param route_active: Status of route. 0 = deactivated, 1 = active
    :param route_priority: Priority of the route
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
        con.row_factory = lite.Row
        cur = con.execute("pragma foreign_keys=ON")
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('UPDATE XFERO_Route SET route_monitoreddir=?, \
        route_filenamepattern=?, route_active = ?, route_priority=? \
        WHERE route_id=?',
                    (route_monitoreddir, route_filenamepattern, route_active,
                     route_priority, route_id))
        con.commit()
    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Updating row on XFERO_Route table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def delete_XFERO_Route(route_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```delete_XFERO_Route``` is a script to delete a specific row
    from the XFERO_Route table.

    It performs the following SQL statement:

    ```'DELETE FROM XFERO_Route WHERE route_id=?', (route_id,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```delete_XFERO_Route(route_id)```

    :param route_id: Identifying ID of the row
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
        con.row_factory = lite.Row
        cur = con.execute("pragma foreign_keys=ON")
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('DELETE FROM XFERO_Route WHERE route_id=?', (route_id,))
        con.commit()
    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error deleting row on XFERO_Route table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def list_XFERO_Route(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Route``` is a script to retrieve all rows from
    the XFERO_Route table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Route'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Route()```

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
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('SELECT * FROM XFERO_Route')
    except lite.Error as err:
        logger.error('Error Selecting row on XFERO_Route table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def list_XFERO_Route_Priority_Route(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Route_Priority_Route``` is a script to retrieve all
    rows from the XFERO_Route table returning the route priority values.

    It performs the following SQL statement:

    ```'SELECT route_priority FROM XFERO_Route'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Route()```

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
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('SELECT route_priority FROM XFERO_Route')
    except lite.Error as err:
        logger.error('Error Selecting row on XFERO_Route table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows

def list_XFERO_Route_Active(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Route_Active``` is a script to retrieve all rows
    from the XFERO_Route table that are 'Active'.

    It performs the following SQL statement:

    ```'SELECT route_id, route_monitoreddir, route_filenamepattern,
    route_active, route_priority FROM XFERO_Route WHERE route_active=?',(1)```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Route_Priority_Active(priority)```

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
        con.row_factory = lite.Row
        cur = con.execute("pragma foreign_keys=ON")
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute(
            'SELECT route_id, route_monitoreddir, route_filenamepattern, \
            route_active, route_priority FROM XFERO_Route \
            WHERE route_active=?', (1,))

    except lite.Error as err:
        logger.error('Error Selecting row on XFERO_Route table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def count_XFERO_Route_Priority(priority, xfero_token=False):
    '''

    **Purpose:**

    The function ```count_XFERO_Route_Priority``` is a script to count all rows in
    the XFERO_Route table given the priority and status is Active.

    It performs the following SQL statement:

    ```'SELECT count(*) FROM XFERO_Route WHERE route_priority=? \
    AND route_active=?',(priority, 1)```

    **Usage Notes:**

    None

    *Example usage:*

    ```count_XFERO_Route_Priority(priority)```

    :param route_priority: Priority of the route
    :returns: count: Number of rows.

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
        con.row_factory = lite.Row
        cur = con.execute("pragma foreign_keys=ON")
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute(
            'SELECT count(*) FROM XFERO_Route \
            WHERE route_priority=? AND route_active=?', (priority, 1))
    except lite.Error as err:
        logger.error('Error Selecting count on XFERO_Route table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    count = cur.fetchone()[0]

    cur.close()
    con.close()
    return count


def count_XFERO_Route(xfero_token=False):
    '''

    **Purpose:**

    The function ```count_XFERO_Route``` is a script to count all rows in
    the XFERO_Route tablethat has a status of Active.

    It performs the following SQL statement:

    ```'SELECT count(*) FROM XFERO_Route WHERE route_active=?',(1)```

    **Usage Notes:**

    None

    *Example usage:*

    ```count_XFERO_Route(1)```

    :param route_priority: Priority of the route
    :returns: count: Number of rows.

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
        con.row_factory = lite.Row
        cur = con.execute("pragma foreign_keys=ON")
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('SELECT count(*) FROM XFERO_Route WHERE route_active=?', (1,))
    except lite.Error as err:
        logger.error('Error Selecting count on XFERO_Route table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    count = cur.fetchone()[0]

    cur.close()
    con.close()
    return count

if __name__ == '__main__':

    rows = list_XFERO_Route_Active('1')
    print(rows)

    for row in rows:
        r_id = row['route_id']
        r_mondir = row['route_monitoreddir']
        r_pattern = row['route_filenamepattern']
        r_active = row['route_active']
        r_priority = row['route_priority']

        print(r_id, r_mondir, r_pattern, r_active, r_priority)

    count = count_XFERO_Route()
    print('number of routes = %s' % count)
