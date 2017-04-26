#!/usr/bin/env python
'''
**Purpose**

Module contains functions to manage the database table XFERO_Workflow

**Unit Test Module:** test_crud_XFERO_Xfer.py

**Process Flow**

.. figure::  ../process_flow/manage_xfer.png
   :align:   center

   Process Flow: Manage Xfer

*External dependencies*

    /xfero/
      get_conf (/xfero/.db.manage_xfer)

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+
| 14/01/2014 | Chris Falck | Update error trapping, logging & refactored       |
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
import logging.config
from /xfero/ import get_conf as get_conf

def create_XFERO_Xfer(xfer_route, xfer_cotspattern, xfer_partner, xfer_cmd,
                   xfer_params, xfer_delsrc='No', xfero_token=False):
    '''

    **Purpose:**

    The function ```create_XFERO_Xfer``` is a script to insert rows into the
    XFERO_Xfer table.

    It performs the following SQL statement:

    ```'INSERT INTO XFERO_Xfer VALUES(NULL, ?, ?, ?, ?, ?, ?)', (xfer_route,
    xfer_cotspattern, xfer_partner, xfer_cmd, xfer_params, xfer_delsrc)```

    **Usage Notes:**

    None

    *Example usage:*

    ```create_XFERO_Xfer(xfer_route, xfer_cotspattern, xfer_partner, xfer_cmd,
    xfer_params, xfer_delsrc )```

    :param xfer_route: identifies the route relationship
    :param xfer_cotspattern: Identifies the relationship with COTS_Pattern
    :param xfer_partner: Patner ID
    :param xfer_cmd: File Transfer command to be executed
    :param xfer_params: Parameters to be supplied to the transfer command
    :param xfer_delsrc: Value can be 'Yes' or 'No' and indicates if the source
    file is to be deleted post successful transfer
    :returns: Row Inserted.

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
        # cur = con.execute("pragma foreign_keys=ON")
        cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('INSERT INTO XFERO_Xfer VALUES(NULL, ?, ?, ?, ?, ?, ?)',
                    (xfer_route, xfer_cotspattern, xfer_partner, xfer_cmd,
                     xfer_params, xfer_delsrc))
        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Inserting row into XFERO_Xfer table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    # return cur
    cur.close()
    con.close()

    return 'Row Inserted'


def read_XFERO_Xfer(xfer_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_Xfer``` is a script to retrieve a specific row from
    the XFERO_Xfer table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Xfer WHERE xfer_id=?', (xfer_id,)```

    **Usage Notes:**

    *Example usage:*

    ```read_XFERO_Xfer(xfer_id)```

    :param xfer_id: Identifying ID of the row
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
        # cur = con.execute("pragma foreign_keys=ON")
        cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('SELECT * FROM XFERO_Xfer WHERE xfer_id=?', (xfer_id,))
    except lite.Error as err:
        logger.error('Error Selecting row from XFERO_Xfer table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def update_XFERO_Xfer(xfer_id, xfer_route, xfer_cotspattern, xfer_partner,
                   xfer_cmd, xfer_params, xfer_delsrc, xfero_token=False):
    '''

    **Purpose:**

    The function ```update_XFERO_Xfer``` is a script to retrieve a specific row
    from the XFERO_Xfer table.

    It performs the following SQL statement:

    ```'UPDATE XFERO_Xfer SET xfer_cmd=?, xfer_cotspattern=?, xfer_route=?,
    xfer_partner=?, xfer_params=? WHERE xfer_id=?', (xfer_cmd, xfer_cotspattern,
    xfer_route, xfer_partner, xfer_params, xfer_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```update_XFERO_Xfer(xfer_id, xfer_route, xfer_cotspattern, xfer_partner,
    xfer_cmd, xfer_params)```

    :param xfer_id: Identifying ID of the row
    :param xfer_route: references the route
    :param xfer_cotspattern: Filname pattern match
    :param xfer_partner: Status of route. 0 = deactivated, 1 = active
    :param xfer_cmd: Priority of the route
    :param xfer_delsrc: Value can be 'Yes' or 'No' and indicates if the source
    file is to be deleted post successful transfer
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
        # cur = con.execute("pragma foreign_keys=ON")
        cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('UPDATE XFERO_Xfer SET xfer_cmd=?, xfer_cotspattern=?, \
        xfer_route=?, xfer_partner=?, xfer_params=?, xfer_delsrc=? \
        WHERE xfer_id=?',
                    (xfer_cmd, xfer_cotspattern, xfer_route, xfer_partner,
                     xfer_params, xfer_delsrc, xfer_id))
        con.commit()
    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Updating row in XFERO_Xfer table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'

def delete_XFERO_Xfer(xfer_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```delete_XFERO_Xfer``` is a script to delete a specific row
    from the XFERO_Xfer table.

    It performs the following SQL statement:

    ```'DELETE FROM XFERO_Xfer WHERE xfer_id=?', (xfer_id,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```delete_XFERO_Xfer(xfer_id)```

    :param xfer_id: Identifying ID of the row
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
        # cur = con.execute("pragma foreign_keys=ON")
        cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('DELETE FROM XFERO_Xfer WHERE xfer_id=?', (xfer_id,))
        con.commit()
    except lite.Error as err:
        if con:
            con.rollback()

        logger.error('Error deleting row from XFERO_Xfer table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def list_XFERO_Xfer(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Xfer``` is a script to retrieve all rows from
    the XFERO_Xfer table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Xfer'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Xfer()```

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
        # cur = con.execute("pragma foreign_keys=ON")
        cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('SELECT * FROM XFERO_Xfer')
        con.commit()
    except lite.Error as err:
        logger.error('Error selecting row from XFERO_Xfer table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows

def list_XFERO_Xfer_Route(xfer_route, xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Xfer_Route``` is a script to retrieve all rows from
    the XFERO_Xfer table using the foreign key xfer_route.

    It performs the following SQL statement:

    ```'SELECT xfer_id, xfer_route, xfer_cotspattern, xfer_partner, xfer_cmd,
    xfer_params, xfer_delsrc
    FROM XFERO_Xfer WHERE xfer_route=?',(xfer_route,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Xfer_Route(xfer_route)```

    :param xfer_route: references the route
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
        # cur = con.execute("pragma foreign_keys=ON")
        cur = con.execute("pragma foreign_keys=OFF")
        cur.execute(
            'SELECT xfer_id, xfer_route, xfer_cotspattern, xfer_partner, \
            xfer_cmd, xfer_params, xfer_delsrc \
            FROM XFERO_Xfer WHERE xfer_route=?', (xfer_route,))
    except lite.Error as err:
        logger.error('Error selecting row from XFERO_Xfer table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def list_all_XFERO_Xfer_Route(xfer_route, xfero_token=False):
    '''

    **Purpose:**

    The function ```list_all_XFERO_Xfer_Route``` is a script to retrieve all rows
    from the XFERO_Xfer table using the foreign key xfer_route.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Xfer WHERE xfer_route=?',(xfer_route)```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_all_XFERO_Xfer_Route(xfer_route)```

    :param xfer_route: references the route
    :returns: rows: All rows selected.

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
        # cur = con.execute("pragma foreign_keys=ON")
        cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('SELECT * FROM XFERO_Xfer WHERE xfer_route=?', (xfer_route))
    except lite.Error as err:
        logger.error('Error selecting row from XFERO_Xfer table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def count_XFERO_Xfer_Route(xfer_route, xfero_token=False):
    '''

    **Purpose:**

    The function ```count_XFERO_Xfer_Route``` is a script to count all rows on the
    XFERO_Xfer table that matched the supplied foreign key xfer_route.

    It performs the following SQL statement:

    ```'SELECT count(*) FROM XFERO_Xfer WHERE xfer_route=?',(xfer_route)```

    **Usage Notes:**

    None

    *Example usage:*

    ```count_XFERO_Xfer_Route(xfer_route)```

    :param xfer_route: references the route
    :returns: count: Number of rows selected.

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
        # cur = con.execute("pragma foreign_keys=ON")
        cur = con.execute("pragma foreign_keys=OFF")
        cur.execute(
            'SELECT count(*) FROM XFERO_Xfer WHERE xfer_route=?', (xfer_route))
    except lite.Error as err:
        logger.error('Error selecting row from XFERO_Xfer table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    count = cur.fetchone()[0]

    cur.close()
    con.close()

    return count


def join_xfer_partner(xfer_route, xfero_token=False):
    '''

    **Purpose:**

    The function ```join_xfer_partner``` is a script which selects items from a
    2 table join of the XFERO_Xfer and XFERO_Partner table.

    It performs the following SQL statement:

    ```'SELECT xfer_id, xfer_route, xfer_cotspattern, xfer_partner, xfer_cmd,
    xfer_params, xfer_delsrc partner_service_name FROM XFERO_Xfer, XFERO_Partner
    WHERE xfer_route=? AND xfer_partner = partner_id', (xfer_route,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```join_xfer_partner(xfer_route)```

    :param xfer_route: references the route
    :returns: rows: Rows selected

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
        # cur = con.execute("pragma foreign_keys=ON")
        cur = con.execute("pragma foreign_keys=OFF")
        cur.execute(
            'SELECT xfer_id, xfer_route, xfer_cotspattern, xfer_partner, \
            xfer_cmd, xfer_params, xfer_delsrc, partner_service_name \
            FROM XFERO_Xfer, XFERO_Partner WHERE xfer_route=? \
            AND xfer_partner = partner_id', (xfer_route,))
    except lite.Error as err:
        logger.error('Error selecting row from table join between XFERO_Xfer & \
        XFERO_Partner table: %s. (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows

if __name__ == '__main__':

    rows = join_xfer_partner('1')

    for xfers in rows:
        xfer_id = xfers[0]
        xfer_route = xfers[1]
        xfer_cotspattern = xfers[2]
        xfer_partner = xfers[3]
        xfer_cmd = xfers[4]
        xfer_params = xfers[5]
        xfer_delsrc = xfers[6]
        partner_service_name = xfers[7]

        print(xfer_id, xfer_route, xfer_cotspattern, xfer_partner,
              xfer_cmd, xfer_params, xfer_delsrc, partner_service_name)
