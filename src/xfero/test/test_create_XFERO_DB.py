#!/usr/bin/env python
'''Test Create XFERO DB'''
import unittest
import configparser
import os
import sqlite3 as lite
from /xfero/.db import create_XFERO_DB as db


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```create_XFERO_DB```

    **Usage Notes:**

    XFERO stores the database location and database name in an ini file which is
    found in <INSTALL_DIR>/conf/XFERO_config.ini. Before proceeding with the test
    please ensure that the XFERO_config.ini file has been suitably modified for the
    purposes of this test.

    **Warning:**

    ALL DATABASE TABLE WILL BE DROPPED DURING THE EXECUTION OF THESE TESTS

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/06/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 08/01/2014 | Chris Falck | Tested to confirm changes to DB               |
    +------------+-------------+-----------------------------------------------+

    '''

    def setUp(self):
        '''
        **Purpose:**

        Create a test /Xfero/ Database

        '''
        # Create the database
        db.create_db()

    def tearDown(self):
        '''
        **Purpose:**

        Delete the test /Xfero/ Database.

        **Usage Notes:**

        XFERO stores the database location and database name in an ini file which
        is found in <INTALL_DIR>/conf/XFERO_config.ini.

        '''

        config = configparser.RawConfigParser()
        try:
            config.read('conf/XFERO_config.ini')
        except configparser.Error as e:
            raise e

        xfero_db = config.get('database', 'db_location')

        # Delete the test DB
        os.remove(xfero_db)

    def test_XFERO_Tables(self):
        '''

        **Purpose:**

        This Test confirms that the /Xfero/ tables have been created.
        This is achieved with the following select statement:

        ```SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        config = configparser.RawConfigParser()
        try:
            config.read('conf/XFERO_config.ini')
        except configparser.Error as e:
            raise e

        xfero_db = config.get('database', 'db_location')

        con = lite.connect(xfero_db)

        try:

            cur = con.cursor()
            cur = con.execute("pragma foreign_keys=ON")
            s = 'table'
            cur.execute('SELECT name FROM sqlite_master WHERE type=?', (s,))

        except lite.Error as e:

            print("Error %s:" % e.args[0])

        rows = cur.fetchall()

        expected_table_list = {'XFERO_AV_Pattern', 'XFERO_COTS_Pattern', ''XFERO_Control',
                               'XFERO_Function', 'XFERO_Partner', ''XFERO_Priority',
                               'XFERO_Route', 'XFERO_Scheduled_Task',
                               'XFERO_Workflow_Item', 'XFERO_Xfer', 'sqlite_sequence'}
        expected_num_tables = 11
        c = 0
        unexpected_tables = 0

        for table_name in rows:
            # print(''.join(table_name))
            c += 1

            if ''.join(table_name) not in expected_table_list:
                unexpected_tables += 1

        # print(unexpected_tables)

        # Ensure expected number of tables
        self.assertEqual(
            expected_num_tables == c, True, "Incorrect Number of tables have \
            been created")
        # Ensure no unexpected tables
        self.assertEqual(
            unexpected_tables == 0, True, "Unexpected tables exist in DB")

    def test_XFERO_Indices(self):
        '''

        **Purpose:**

        This Test confirms that the /Xfero/ indices have been created.
        This is achieved with the following select statement:

        ```SELECT name FROM sqlite_master WHERE type='index' ORDER BY name;```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        config = configparser.RawConfigParser()
        try:
            config.read('conf/XFERO_config.ini')
        except configparser.Error as e:
            raise e

        xfero_db = config.get('database', 'db_location')

        con = lite.connect(xfero_db)

        try:

            cur = con.cursor()
            cur = con.execute("pragma foreign_keys=ON")

            s = 'index'

            cur.execute('SELECT name FROM sqlite_master WHERE type=?', (s,))

        except lite.Error as e:

            print("Error %s:" % e.args[0])

        rows = cur.fetchall()

        expected_index_list = {
            'routeindex', 'workflowindex', 'xfercotspatternindex', 'xferindex',
            'xferpartner'}
        expected_num_indices = 5
        c = 0
        unexpected_index = 0

        for index_name in rows:
            # print(''.join(index_name))
            c += 1

            if ''.join(index_name) not in expected_index_list:
                unexpected_index += 1

        # Ensure expected number of tables
        self.assertEqual(expected_num_indices == c, True,
                         "Incorrect Number of indices have been created")
        # Ensure no unexpected tables
        self.assertEqual(
            unexpected_index == 0, True, "Unexpected indices exist in DB")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
