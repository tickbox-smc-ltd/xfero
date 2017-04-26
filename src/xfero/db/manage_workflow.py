#!/usr/bin/env python

'''
**Purpose**

Module contains functions to manage the database table XFERO_Workflow

**Unit Test Module:** test_crud_XFERO_Workflow.py

**Process Flow**

.. figure::  ../process_flow/manage_workflow.png
   :align:   center

   Process Flow: Manage Workflow

*External dependencies*

    /xfero/
      get_conf (/xfero/.db.manage_workflow)

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+
| 09/01/2014 | Chris Falck | Update error trapping, logging & refactored       |
+------------+-------------+---------------------------------------------------+
| 04/05/2014 | Chris Falck | Added new column 'workflow_item_class' to hold    |
|            |             | class details - OO conversion                     |
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


def create_XFERO_Workflow_Item(workflow_item_route, workflow_item_class,
                            workflow_item_function_call, workflow_item_args,
                            workflow_item_running_order, xfero_token=False):
    '''

    **Purpose:**

    The function ```create_XFERO_Workflow_Item``` is a script to insert rows into
    the XFERO_Workflow_Item table.

    It performs the following SQL statement:

    ```'INSERT INTO XFERO_Workflow_Item VALUES(NULL, ?, ?, ?, ?)',
    (workflow_item_route, workflow_item_class, workflow_item_function_call,
    workflow_item_args, workflow_item_running_order)```

    **Usage Notes:**

    None

    *Example usage:*

    ```create_XFERO_Workflow_Item(workflow_item_route, workflow_item_class,
    workflow_item_function_call, workflow_item_args,
    workflow_item_running_order)```

    :param workflow_item_route: identifies the route relationship
    :param workflow_item_class: Class containing workflow method
    :param workflow_item_function_call: Identifying relationship with function
    :param workflow_item_args: arguments to be passed to the function
    :param workflow_item_running_order: Order of execution within the workflow
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
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('INSERT INTO XFERO_Workflow_Item \
        VALUES(NULL, ?, ?, ?, ?, ?)', (workflow_item_route, workflow_item_class,
                                       workflow_item_function_call,
                                       workflow_item_args,
                                       workflow_item_running_order))
        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Inserting row into XFERO_Workflow_Item table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    # return cur
    cur.close()
    con.close()

    return 'Row Inserted'


def read_XFERO_Workflow_Item(workflow_item_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_Workflow_Item``` is a script to retrieve a specific
    row from the XFERO_Workflow_Item table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Workflow_Item WHERE workflow_item_id=?',
    (workflow_item_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_XFERO_Workflow_Item(workflow_item_id)```

    :param workflow_item_id: Identifying ID of the row
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
        cur.execute(
            'SELECT * FROM XFERO_Workflow_Item \
            WHERE workflow_item_id=?', (workflow_item_id))
    except lite.Error as err:

        logger.error('Error Selecting row from XFERO_Workflow_Item table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def select_max_XFERO_Workflow_Item(workflow_item_route, xfero_token=False):
    '''

    **Purpose:**

    The function ```select_max_XFERO_Workflow_Item``` is a script to retrieve max
    running order from the XFERO_Workflow_Item table using the foreign key workflow
    item route.

    It performs the following SQL statement:

    ```'SELECT max(workflow_item_running_order) FROM XFERO_Workflow_Item
    WHERE workflow_item_route=?', (workflow_item_route)```

    **Usage Notes:**

    None

    *Example usage:*

    ```select_max_XFERO_Workflow_Item(workflow_item_route)```

    :param workflow_item_id: Identifying ID of the row
    :returns: row: A Tuple of the selected row.

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
        cur.execute(
            'SELECT max(workflow_item_running_order) \
            FROM XFERO_Workflow_Item WHERE workflow_item_route=?',
            (workflow_item_route))
    except lite.Error as err:
        logger.error('Error Selecting row from XFERO_Workflow_Item table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def update_XFERO_Workflow_Item(workflow_item_id, workflow_item_route,
                            workflow_item_class, workflow_item_function_call,
                            workflow_item_args, workflow_item_running_order,
                            xfero_token=False):
    '''

    **Purpose:**

    The function ```update_XFERO_Workflow_Item``` is a script to update
    rows into the XFERO_Workflow_Item table.

    It performs the following SQL statement:

    ```'UPDATE XFERO_Workflow_Item SET workflow_item_route=?,
    workflow_item_class=?, workflow_item_function_call=?, workflow_item_args=?,
    workflow_item_running_order=? WHERE workflow_item_id=?',
    (workflow_item_route, workflow_item_class, workflow_item_function_call,
    workflow_item_args, workflow_item_running_order, workflow_item_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```update_XFERO_Workflow_Item(workflow_item_id, workflow_item_route,
    workflow_item_class, workflow_item_function_call, workflow_item_args,
    workflow_item_running_order):```

    :param workflow_item_id: Identifying ID of the row
    :param workflow_item_route: references the route
    :param workflow_item_class: Class containing workflow method
    :param workflow_item_function_call: Filename pattern match
    :param workflow_item_args: Status of route. 0 = deactivated, 1 = active
    :param workflow_item_running_order: Priority of the route
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
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute('UPDATE XFERO_Workflow_Item SET workflow_item_route=?, \
        workflow_item_class=?, workflow_item_function_call=?, \
        workflow_item_args=?, workflow_item_running_order=? \
        WHERE workflow_item_id=?',
                    (workflow_item_route, workflow_item_class,
                     workflow_item_function_call, workflow_item_args,
                     workflow_item_running_order, workflow_item_id))
        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Updating row on XFERO_Workflow_Item table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def delete_XFERO_Workflow_Item(workflow_item_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```delete_XFERO_Workflow_Item``` is a script to delete a specific
    row from the XFERO_Workflow_Item table.

    It performs the following SQL statement:

    ```'DELETE FROM XFERO_Workflow_Item WHERE workflow_item_id=?',
    (workflow_item_id,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```delete_XFERO_Workflow_Item(workflow_item_id)```

    :param workflow_item_id: Identifying ID of the row
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
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute(
            'DELETE FROM XFERO_Workflow_Item \
            WHERE workflow_item_id=?', (workflow_item_id,))
        con.commit()
    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error deleting row from XFERO_Workflow_Item table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def list_XFERO_Workflow_Item(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Workflow_Item``` is a script to retrieve all rows
    from the XFERO_Workflow_Item table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Workflow_Item'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Workflow_Item()```

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
        cur.execute('SELECT * FROM XFERO_Workflow_Item')
        con.commit()
    except lite.Error as err:

        logger.error('Error selecting rows from XFERO_Workflow_Item table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def list_XFERO_Workflow_Item_OrderBy_Run_Order(workflow_item_route,
                                            xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Workflow_Item_OrderBy_Run_Order``` is a script to
    retrieve all rows from the XFERO_Workflow_Item table ordered by
    workflow_item_route.

    It performs the following SQL statement:

    ```'SELECT workflow_item_id, workflow_item_route, workflow_item_class,
    workflow_item_function_call, workflow_item_args, workflow_item_running_order
    FROM XFERO_Workflow_Item WHERE workflow_item_route=? ORDER BY
    workflow_item_running_order ASC',(workflow_item_route,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Workflow_Item_OrderBy_Run_Order(workflow_item_route)```

    :param workflow_item_route: references the route
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
        cur.execute(
            'SELECT workflow_item_id, workflow_item_route, \
            workflow_item_class, workflow_item_function_call, \
            workflow_item_args, workflow_item_running_order \
            FROM XFERO_Workflow_Item WHERE workflow_item_route=? \
            ORDER BY workflow_item_running_order ASC', (workflow_item_route,))
    except lite.Error as err:

        logger.error('Error selecting rows from XFERO_Workflow_Item table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def list_XFERO_Workflow_Item_OrderBy_Run_Order_monitor(workflow_item_route,
                                                    xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Workflow_Item_OrderBy_Run_Order``` is a script to
    retrieve all rows from the XFERO_Workflow_Item table ordered by
    workflow_item_route.

    It performs the following SQL statement:

    ```'SELECT workflow_item_id, workflow_item_route, workflow_item_class,
    workflow_item_function_call, workflow_item_args, workflow_item_running_order
    FROM XFERO_Workflow_Item WHERE workflow_item_route=? ORDER BY
    workflow_item_running_order ASC',(workflow_item_route,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Workflow_Item_OrderBy_Run_Order(workflow_item_route)```

    :param workflow_item_route: references the route
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
        # cur = con.execute("pragma foreign_keys=OFF")
        cur.execute(
            'SELECT workflow_item_id, workflow_item_route, \
            workflow_item_class, workflow_item_function_call, \
            workflow_item_args, workflow_item_running_order \
            FROM XFERO_Workflow_Item WHERE workflow_item_route=? \
            ORDER BY workflow_item_running_order ASC', (workflow_item_route,))

    except lite.Error as err:

        logger.error('Error selecting rows from XFERO_Workflow_Item table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows

if __name__ == '__main__':

    rows = list_XFERO_Workflow_Item_OrderBy_Run_Order('5')
    print(rows)
    for workflow in rows:
        wf_args = ''
        wf_id = workflow['workflow_item_id']
        wf_route = workflow['workflow_item_route']
        wf_function_call = workflow['workflow_item_function_call']
        if workflow['workflow_item_args'] != 'NULL':
            wf_args = workflow['workflow_item_args']
        wf_run_order = workflow['workflow_item_running_order']

        print(wf_id, wf_route, wf_function_call, wf_args, wf_run_order)
