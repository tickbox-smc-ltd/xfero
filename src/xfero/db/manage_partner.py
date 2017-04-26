#!/usr/bin/env python

'''
**Purpose**

Module contains functions to manage the database table XFERO_Partner

**Unit Test Module:** test_crud_XFERO_Partner.py

**Process Flow**

.. figure::  ../process_flow/manage_partner.png
   :align:   center

   Process Flow: Manage Partner

*External dependencies*

    os (/xfero/.db.manage_partner)
    /xfero/
      get_conf (/xfero/.db.manage_partner)

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
| 27/10/2014 | Chris Falck | modified call to get_conf                         |
+------------+-------------+---------------------------------------------------+
| 28/04/2015 | Chris Falck | Added support for eNDI and UTM functionality      |
+------------+-------------+---------------------------------------------------+

'''

import sqlite3 as lite
from /xfero/ import get_conf as get_conf
import logging.config

def create_XFERO_Partner(partner_service_name, partner_service_description,
                      partner_COTS_type, partner_remote_system_id, partner_code,
                      partner_mode, partner_local_username,
                      partner_local_password, partner_remote_user,
                      partner_remote_password, partner_CA_certificate,
                      partner_cert_bundle, partner_control_port,
                      partner_IDF, partner_parm, partner_pgp_pub_key,
                      partner_lqm, partner_dqm, partner_oqm, partner_cq,
                      partner_exit, partner_exitdll, partner_exitentry,
                      partner_exitdata, partner_ofile, partner_receiving_app,
                      partner_target_app, partner_action,
                      partner_post_xfer_hook, partner_post_xfer_comp_hook,
                      partner_retain_file, partner_priority, xfero_token=False):
    '''

    **Purpose:**

    The function ```create_XFERO_Partner``` is a script to insert rows into the
    XFERO_Partner table.

    It performs the following SQL statement:

    ```'INSERT INTO XFERO_Partner
    VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
    (partner_service_name, partner_service_description, partner_COTS_type,
    partner_remote_system_id, partner_code, partner_mode,
    partner_local_username, partner_local_password, partner_remote_user,
    partner_remote_password, partner_CA_certificate, partner_cert_bundle,
    partner_control_port, partner_IDF, partner_parm, partner_pgp_pub_key,
    partner_lqm, partner_dqm, partner_oqm, partner_cq, partner_exit,
    partner_exitdll, partner_exitentry, partner_exitdata, partner_ofile,
    partner_receiving_app, partner_target_app, partner_action, 
    partner_post_xfer_hook, partner_post_xfer_comp_hook, partner_retain_file,
    partner_priority)```

    **Usage Notes:**

    None

    *Example usage:*

    ```create_XFERO_Partner(partner_service_name, partner_service_description,
    partner_COTS_type, partner_remote_system_id, partner_code, partner_mode,
    partner_local_username, partner_local_password, partner_remote_user,
    partner_remote_password, partner_CA_certificate, partner_cert_bundle,
    partner_control_port, partner_IDF, partner_parm, partner_pgp_pub_key)```

    :param partner_service_name: Name of Partner Service
    :param partner_service_description: Description of Service
    :param partner_COTS_type: COTS Product type used by partner
    :param partner_remote_system_id: ID of remote system
    :param partner_code: Codeset for file transfer ((B)inary/(A)scii)
    :param partner_mode: Mode of transfer ((R)ead/(W)rite)
    :param partner_local_username: Local username used for transfer
    :param partner_local_password: Local users password used for transfer
    :param partner_remote_user: Remote Username used for transfer receive
    :param partner_remote_password: Remote User password for transfer receive
    :param partner_CA_certificate: Location of CA Certificate
    :param partner_cert_bundle: Location of User Certificate bundle
    :param partner_control_port: Port used for transfer
    :param partner_IDF, partner_parm: IDF of CFT Transfer
    :param partner_pgp_pub_key: Public Key provided by partner
    :returns: Row Inserted

    **Unit Test Module:** test_crud_XFERO_Partner.py

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/07/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 09/01/2014 | Chris Falck | Update error trapping, logging & refactored   |
    +------------+-------------+-----------------------------------------------+
    | 11/05/2014 | Chris Falck | Modified the function to ensure that database |
    |            |             | connections are opened and closed within the  |
    |            |             | function call. This enables the function to be|
    |            |             | called in a multiprocessing environment.      |
    +------------+-------------+-----------------------------------------------+
    | 12/05/2014 | Chris Falck | New element passed on queue 'xfero_token'. Used  |
    |            |             | in Logging.                                   |
    +------------+-------------+-----------------------------------------------+
    | 28/04/2015 | Chris Falck | Added support for eNDI and UTM                |
    +------------+-------------+-----------------------------------------------+
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
        cur.execute('INSERT INTO XFERO_Partner \
        VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (partner_service_name, partner_service_description,
                     partner_COTS_type, partner_remote_system_id, partner_code,
                     partner_mode, partner_local_username,
                     partner_local_password, partner_remote_user,
                     partner_remote_password, partner_CA_certificate,
                     partner_cert_bundle, partner_control_port, partner_IDF,
                     partner_parm, partner_pgp_pub_key, partner_lqm,
                     partner_dqm, partner_oqm, partner_cq, partner_exit,
                     partner_exitdll, partner_exitentry, partner_exitdata,
                     partner_ofile, partner_receiving_app, partner_target_app,
                     partner_action, partner_post_xfer_hook,
                     partner_post_xfer_comp_hook, partner_retain_file,
                     partner_priority))
        con.commit()
        inserted_id = cur.lastrowid

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Inserting row into XFERO_Partner table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    # return cur
    cur.close()
    con.close()

    return inserted_id


def read_XFERO_Partner(partner_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_XFERO_Partner``` is a script to retrieve a specific row
    from the XFERO_Partner table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Partner WHERE partner_id=?', (partner_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_XFERO_Partner(partner_id)```

    :param partner_service_name: Name of Partner Service
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
            'SELECT * FROM XFERO_Partner WHERE partner_id=?', (partner_id))
    except lite.Error as err:
        logger.error('Error Selecting row into XFERO_Partner table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def read_psn_XFERO_Partner(partner_service_name, xfero_token=False):
    '''

    **Purpose:**

    The function ```read_psn_XFERO_Partner``` is a script to retrieve a specific
    row from the XFERO_Partner table by Partner Service Name.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Partner WHERE partner_service_name=?',
    (partner_service_name,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```read_psn_XFERO_Partner(partner_service_name)```

    :param partner_service_name: Name of Partner Service
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
            'SELECT * FROM XFERO_Partner WHERE partner_service_name=?',
            (partner_service_name,))

    except lite.Error as err:
        logger.error('Error Selecting row into XFERO_Partner table: %s. \
        (XFERO_Token=%s)' % (err.args[0], xfero_token))
        raise err

    rows = cur.fetchone()

    cur.close()
    con.close()

    return rows


def update_XFERO_Partner(partner_id, partner_service_name,
                      partner_service_description, partner_COTS_type,
                      partner_remote_system_id, partner_code, partner_mode,
                      partner_local_username, partner_local_password,
                      partner_remote_user, partner_remote_password,
                      partner_CA_certificate, partner_cert_bundle,
                      partner_control_port, partner_IDF, partner_parm,
                      partner_pgp_pub_key, partner_lqm, partner_dqm,
                      partner_oqm, partner_cq, partner_exit, partner_exitdll,
                      partner_exitentry, partner_exitdata, partner_ofile,
                      partner_receiving_app, partner_target_app, partner_action,
                      partner_post_xfer_hook, partner_post_xfer_comp_hook,
                      partner_retain_file, partner_priority, xfero_token=False):
    
    '''

    **Purpose:**

    The function ```update_XFERO_Partner``` is a  SQL update script to update
    rows into the XFERO_Partner table.

    It performs the following SQL statement:

    ```'UPDATE XFERO_Partner SET partner_service_name=?,
    partner_service_description=?, partner_COTS_type=?,
    partner_remote_system_id=?, partner_code=?, partner_mode=?,
    partner_local_username=?, partner_local_password=?, partner_remote_user=?,
    partner_remote_password=?, partner_CA_certificate=?, partner_cert_bundle=?,
    partner_control_port=?, partner_IDF=?, partner_parm=?, partner_pgp_pub_key=?
    WHERE partner_id=?', (partner_service_name, partner_service_description,
    partner_COTS_type, partner_remote_system_id, partner_code, partner_mode,
    partner_local_username, partner_local_password, partner_remote_user,
    partner_remote_password, partner_CA_certificate, partner_cert_bundle,
    partner_control_port, partner_IDF, partner_parm, partner_pgp_pub_key,
    partner_id)```

    **Usage Notes:**

    None

    *Example usage:*

    ```update_XFERO_Partner(partner_id, partner_service_name,
    partner_service_description, partner_COTS_type, partner_remote_system_id,
    partner_code, partner_mode, partner_local_username, partner_local_password,
    partner_remote_user, partner_remote_password, partner_CA_certificate,
    partner_cert_bundle, partner_control_port, partner_IDF, partner_parm,
    partner_pgp_pub_key)```

    :param partner_id: Primary Key ID which identifies the row to update
    :param partner_service_name: Name of Partner Service
    :param partner_service_description: Description of Service
    :param partner_COTS_type: COTS Product type used by partner
    :param partner_remote_system_id: ID of remote system
    :param partner_code: Codeset for file transfer ((B)inary/(A)scii)
    :param partner_mode: Mode of transfer ((R)ead/(W)rite)
    :param partner_local_username: Local username used for transfer
    :param partner_local_password: Local users password used for transfer
    :param partner_remote_user: Remote Username used for transfer receive
    :param partner_remote_password: Remote User password for transfer receive
    :param partner_CA_certificate: Location of CA Certificate
    :param partner_cert_bundle: Location of User Certificate bundle
    :param partner_control_port: Port used for transfer
    :param partner_IDF, partner_parm: IDF of CFT Transfer
    :param partner_pgp_pub_key: Public Key supplied by partner
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
        cur.execute('UPDATE XFERO_Partner \
        SET partner_service_name=?, partner_service_description=?, \
        partner_COTS_type=?, partner_remote_system_id=?, partner_code=?, \
        partner_mode=?, partner_local_username=?, partner_local_password=?, \
        partner_remote_user=?, partner_remote_password=?, \
        partner_CA_certificate=?, partner_cert_bundle=?, \
        partner_control_port=?, partner_IDF=?, partner_parm=?, \
        partner_pgp_pub_key=?, partner_lqm=?, partner_dqm=?, partner_oqm=?, \
        partner_cq=?, partner_exit=?, partner_exitdll=?, partner_exitentry=?, \
        partner_exitdata=?, partner_ofile=?, partner_receiving_app=?, \
        partner_target_app=?, partner_action=?, partner_post_xfer_hook=?, \
        partner_post_xfer_comp_hook=?, partner_retain_file=?, \
        partner_priority=? WHERE partner_id=?',
                    (partner_service_name, partner_service_description,
                     partner_COTS_type, partner_remote_system_id, partner_code,
                     partner_mode, partner_local_username,
                     partner_local_password, partner_remote_user,
                     partner_remote_password, partner_CA_certificate,
                     partner_cert_bundle, partner_control_port, partner_IDF,
                     partner_parm, partner_pgp_pub_key, partner_lqm,
                     partner_dqm, partner_oqm, partner_cq, partner_exit,
                     partner_exitdll, partner_exitentry, partner_exitdata,
                     partner_ofile, partner_receiving_app, partner_target_app,
                     partner_action, partner_post_xfer_hook,
                     partner_post_xfer_comp_hook, partner_retain_file,
                     partner_priority, partner_id))
        con.commit()

    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error Updating row on XFERO_Partner table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def delete_XFERO_Partner(partner_id, xfero_token=False):
    '''

    **Purpose:**

    The function ```delete_XFERO_Partner``` is a script to delete a specific row
    from the XFERO_Partner table.

    It performs the following SQL statement:

    ```'DELETE FROM XFERO_Partner WHERE partner_id=?', (partner_id,)```

    **Usage Notes:**

    None

    *Example usage:*

    ```delete_XFERO_Partner(partner_id)```

    :param partner_id: Primary Key ID which identifies the row to update
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
        cur.execute('DELETE FROM XFERO_Partner WHERE partner_id=?', (partner_id,))
        con.commit()
    except lite.Error as err:

        if con:
            con.rollback()

        logger.error('Error deleting row on XFERO_Partner table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    cur.close()
    con.close()

    return 'Success'


def list_XFERO_Partner(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_XFERO_Partner``` is a script to retrieve all rows from
    the XFERO_Partner table.

    It performs the following SQL statement:

    ```'SELECT * FROM XFERO_Partner'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_XFERO_Partner()```

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
        cur.execute('SELECT * FROM XFERO_Partner')
        con.commit()

    except lite.Error as err:

        logger.error('Error Selecting row on XFERO_Partner table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


def list_service_name_XFERO_Partner(xfero_token=False):
    '''

    **Purpose:**

    The function ```list_service_name_XFERO_Partner``` is a script to retrieve all
    rows from the XFERO_Partner table.

    It performs the following SQL statement:

    ```'SELECT partner_service_name FROM XFERO_Partner'```

    **Usage Notes:**

    None

    *Example usage:*

    ```list_service_name_XFERO_Partner()```

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
        cur.execute('SELECT partner_service_name FROM XFERO_Partner')
        con.commit()

    except lite.Error as err:
        logger.error('Error Selecting row on XFERO_Partner table: %s. \
        (XFERO_Token=%s)', err.args[0], xfero_token)
        raise err

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows

if __name__ == "__main__":

    rows = read_psn_XFERO_Partner('OSI_PART')
    if rows is None:
        print('No record')
    else:
        print(rows)
        print(rows[1])
