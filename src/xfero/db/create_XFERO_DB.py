#!/usr/bin/env python
'''
'XFERO Database creation
'''
import sqlite3 as lite
import sys
from /xfero/ import get_conf as get_conf


def create_db():
    '''

    **Purpose:**

    This script has been developed for System Administrators to create the
    Database and associated tables for /Xfero/.

    **Usage Notes:**

    This script will DROP any pre-existing tables prior to creation. So, beware
    when using.

    This script will report "/Xfero/ Database created!" when the
    database has been successfully created.

    Any errors that occur during the creation of the database will be reported
    to the command line.

    *Example usage:*

    ```create_db()``

    :param none: This script takes no parameters
    :returns: This script does not return any values

    **Unit Test Module:** test_create_db.py

    *External dependencies*

    /xfero/
      get_conf (/xfero/.db.create_XFERO_DB)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/07/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 08/01/2014 | Chris Falck | Added error trapping                          |
    +------------+-------------+-----------------------------------------------+
    | 04/05/2014 | Chris Falck | Added new column 'priority_worker_threads' to |
    |            |             | create Priority table.                        |
    |            |             | Added new column 'workflow_item_class' to hold|
    |            |             | class details - OO conversion                 |
    +------------+-------------+-----------------------------------------------+
    | 12/05/2014 | Chris Falck | Added new column 'xfer_delsrc' to             |
    |            |             | create_XFERO_Xfer table.                         |
    +------------+-------------+-----------------------------------------------+
    | 16/10/2014 | Chris Falck | Modified the creation of Priority and Control |
    |            |             | table                                         |
    +------------+-------------+-----------------------------------------------+
    | 28/04/2015 | Chris Falck | Added support for eNDI and UTM to the Partner |
    |            |             | table                                         |
    +------------+-------------+-----------------------------------------------+
    

    '''
    try:
        (xfero_logger,.xfero_database, outbound_directory, transient_directory,
         error_directory, xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s', err)
        sys.exit(err)

    dbase = xfero_database

    try:

        con = lite.connect(dbase)

        with con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS XFERO_Function")
            cur.execute("DROP TABLE IF EXISTS XFERO_COTS_Pattern")
            cur.execute("DROP TABLE IF EXISTS XFERO_AV_Pattern")
            cur.execute("DROP TABLE IF EXISTS XFERO_Priority")
            cur.execute("DROP TABLE IF EXISTS XFERO_Route")
            cur.execute("DROP TABLE IF EXISTS XFERO_Xfer")
            cur.execute("DROP TABLE IF EXISTS XFERO_Workflow_Item")
            cur.execute("DROP TABLE IF EXISTS XFERO_Scheduled_Task")
            cur.execute("DROP TABLE IF EXISTS XFERO_Control")
            cur.execute("DROP TABLE IF EXISTS XFERO_Partner")

            cur.execute("DROP INDEX IF EXISTS routeindex")
            cur.execute("DROP INDEX IF EXISTS xferindex")
            cur.execute("DROP INDEX IF EXISTS workflowindex")
            cur.execute("DROP INDEX IF EXISTS xfercotspatternindex")

            cur.execute(
                "CREATE TABLE XFERO_Function \
                (function_id INTEGER NOT NULL PRIMARY KEY, \
                function_name TEXT NOT NULL, \
                function_class TEXT NULL, \
                function_description TEXT NULL, \
                function_prototype TEXT NOT NULL);")
            cur.execute(
                "CREATE TABLE XFERO_Partner \
                (partner_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                partner_service_name TEXT NOT NULL, \
                partner_service_description TEXT NULL, \
                partner_COTS_type TEXT NOT NULL, \
                partner_remote_system_id TEXT NOT NULL, \
                partner_code TEXT NULL, \
                partner_mode TEXT NULL, \
                partner_local_username TEXT NULL, \
                partner_local_password TEXT NULL, \
                partner_remote_user TEXT NULL, \
                partner_remote_password TEXT NULL, \
                partner_CA_certificate TEXT NULL, \
                partner_cert_bundle TEXT NULL, \
                partner_control_port INTEGER NULL, \
                partner_IDF TEXT NULL, \
                partner_parm TEXT NULL, \
                partner_pgp_pub_key TEXT NULL, \
                partner_lqm TEXT NULL, \
                partner_dqm TEXT NULL, \
                partner_oqm TEXT NULL, \
                partner_cq TEXT NULL, \
                partner_exit TEXT NULL, \
                partner_exitdll TEXT NULL, \
                partner_exitentry TEXT NULL, \
                partner_exitdata TEXT NULL, \
                partner_ofile TEXT NULL, \
                partner_receiving_app TEXT NULL, \
                partner_target_app TEXT NULL, \
                partner_action TEXT NULL, \
                partner_post_xfer_hook TEXT NULL, \
                partner_post_xfer_comp_hook TEXT NULL, \
                partner_retain_file TEXT NULL, \
                partner_priority TEXT NULL);")
            cur.execute(
                "CREATE TABLE XFERO_COTS_Pattern \
                (cotspattern_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                cotspattern_product TEXT NOT NULL, \
                cotspattern_pattern_name TEXT NOT NULL, \
                cotspattern_prototype TEXT NOT NULL);")
            cur.execute(
                "CREATE TABLE XFERO_AV_Pattern \
                (avpattern_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                avpattern_product TEXT NOT NULL, \
                avpattern_pattern_name TEXT NOT NULL, \
                avpattern_params TEXT NULL);")
            cur.execute(
                "CREATE TABLE XFERO_Priority \
                (priority_level INTEGER NOT NULL PRIMARY KEY, \
                priority_detail TEXT NOT NULL);")
            cur.execute(
                "CREATE TABLE XFERO_Scheduled_Task \
                (scheduled_task_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                scheduled_task_name TEXT NOT NULL, \
                scheduled_task_function TEXT NOT NULL, \
                scheduled_task_year TEXT NULL, \
                scheduled_task_month TEXT NULL, \
                scheduled_task_day TEXT NULL, \
                scheduled_task_week TEXT NULL, \
                scheduled_task_day_of_week TEXT NULL, \
                scheduled_task_hour TEXT NULL, \
                scheduled_task_minute TEXT NULL, \
                scheduled_task_second TEXT NULL, \
                scheduled_task_args TEXT NOT NULL, \
                scheduled_task_active TEXT NOT NULL);")
            cur.execute(
                "CREATE TABLE XFERO_Control \
                (control_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                control_status TEXT NOT NULL, \
                control_pgp_priv_key TEXT NULL, \
                control_pgp_passphrase TEXT NULL, \
                control_num_threads INTEGER NOT NULL);")

            cur.execute(
                "CREATE TABLE XFERO_Route \
                (route_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                route_monitoreddir TEXT NOT NULL, \
                route_filenamepattern TEXT NOT NULL, \
                route_active INTEGER NOT NULL, \
                route_priority INTEGER NOT NULL REFERENCES \
                XFERO_Priority(priority_level) ON \
                DELETE RESTRICT ON UPDATE CASCADE);")
            cur.execute("CREATE INDEX routeindex ON XFERO_Route(route_priority);")
            cur.execute(
                "CREATE TABLE XFERO_Xfer \
                (xfer_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                xfer_route INTEGER NOT NULL, \
                xfer_cotspattern INTEGER NOT NULL, \
                xfer_partner INTEGER NOT NULL, \
                xfer_cmd TEXT NOT NULL, \
                xfer_params TEXT NOT NULL, \
                xfer_delsrc TEXT NOT NULL, \
                FOREIGN KEY(xfer_route) REFERENCES XFERO_Route(route_id) ON \
                DELETE CASCADE ON UPDATE CASCADE, \
                FOREIGN KEY(xfer_cotspattern) REFERENCES \
                XFERO_COTS_Pattern(cotspattern_id) ON DELETE CASCADE ON UPDATE \
                CASCADE, \
                FOREIGN KEY(xfer_partner) REFERENCES XFERO_Partner(partner_id) ON \
                DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("CREATE INDEX xferindex ON XFERO_Xfer(xfer_route);")
            cur.execute(
                "CREATE INDEX xfercotspatternindex ON \
                XFERO_Xfer(xfer_cotspattern);")
            cur.execute("CREATE INDEX xferpartner ON XFERO_Xfer(xfer_partner);")
            cur.execute(
                "CREATE TABLE XFERO_Workflow_Item \
                (workflow_item_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                workflow_item_route INTEGER NOT NULL REFERENCES \
                XFERO_Route(route_id) ON DELETE CASCADE ON UPDATE CASCADE, \
                workflow_item_class TEXT NOT NULL, \
                workflow_item_function_call TEXT NOT NULL, \
                workflow_item_args TEXT NULL, \
                workflow_item_running_order INTEGER NOT NULL);")
            cur.execute(
                "CREATE INDEX workflowindex ON \
                XFERO_Workflow_Item(workflow_item_route);")

    except lite.Error as err:
        print("Error %s:" % err.args[0])
        sys.exit(err)

    # Commit
    con.commit()
    con.close()
    print("/Xfero/ Database created!")

if __name__ == "__main__":
    create_db()
