#!/usr/bin/env python
'''Test Manage Control'''
import unittest
import configparser
import os
import sqlite3 as lite
from /xfero/.db import manage_control as db_control
from /xfero/.db import create_XFERO_DB as db


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```crud_XFERO_Control```

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
        except configparser.Error as err:
            raise err

        xfero_db = config.get('database', 'db_location')

        # Delete the test DB
        os.remove(xfero_db)

    def test_create_XFERO_Control(self):
        '''

        **Purpose:**

        INSERT rows into the XFERO_Control table and confirm they have been
        successfully inserted

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+
        '''

        for tst in [('START', 'KEY', 'PASSPHRASE', 1),
                    ('STOP', 'KEY', 'PASSPHRASE', 1),]:

            (self.control_status, self.key, self.passphrase,
             self.control_num_threads) = tst
            result = db_control.create_XFERO_Control(
                self.control_status, self.key, self.passphrase,
                self.control_num_threads,)

        config = configparser.RawConfigParser()
        try:
            config.read('conf/XFERO_config.ini')
        except configparser.Error as err:
            raise err

        xfero_db = config.get('database', 'db_location')
        con = lite.connect(xfero_db)

        try:
            cur = con.cursor()
            cur = con.execute("pragma foreign_keys=ON")
            cur.execute('SELECT control_id FROM XFERO_Control')
        except lite.Error as err:

            print("Error %s:" % err.args[0])

        expected_tuple = ((1,), (2,))

        rows = cur.fetchall()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row retrieved')

    def test_read_XFERO_Control(self):
        '''

        **Purpose:**

        SELECT a specified row from the XFERO_Control table with control_id = 1 and
        confirm that the row returned is as expected

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('START', 'KEY', 'PASSPHRASE', 1),]:

            (self.control_status, self.key, self.passphrase,
             self.control_num_threads) = tst
            result = db_control.create_XFERO_Control(
                self.control_status, self.key, self.passphrase,
                self.control_num_threads,)

        # Perform the select
        self.control_id = '1'
        rows = db_control.read_XFERO_Control(self.control_id)

        expected_id = 1
        expected_status = 'START'
        expected_key = 'KEY'
        expected_pass = 'PASSPHRASE'

        for control in rows:
            control_id = control['control_id']
            control_status = control['control_status']
            control_key = control['control_pgp_priv_key']
            control_pass = control['control_pgp_passphrase']

            self.assertEqual(
                expected_id, control_id, 'Unexpected value returned')
            self.assertEqual(
                expected_status, control_status, 'Unexpected value returned')
            self.assertEqual(
                expected_key, control_key, 'Unexpected value returned')
            self.assertEqual(
                expected_pass, control_pass, 'Unexpected value returned')

    def test_read_XFERO_Control_monitor(self):
        '''

        **Purpose:**

        SELECT a specified row from the XFERO_Control table with control_id = 1 and
        confirm that the row returned is as expected

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('START', 'KEY', 'PASSPHRASE', 1),]:

            (self.control_status, self.key, self.passphrase,
             self.control_num_threads) = tst
            result = db_control.create_XFERO_Control(
                self.control_status, self.key, self.passphrase,
                self.control_num_threads,)

        # Perform the select
        self.control_id = '1'
        row = db_control.read_XFERO_Control_monitor(self.control_id)

        expected_tuple = (1, 'START', 'KEY', 'PASSPHRASE')

        self.assertTupleEqual(expected_tuple, row, 'Unexpected row returned')

    def test_update_XFERO_Control(self):
        '''

        **Purpose:**

        UPDATE row on the XFERO_Control table with control_id = 1 and confirm that
        the update has been applied to the table.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''

        # Create the row in the database
        for tst in [('START', 'KEY', 'PASSPHRASE', 1),]:

            (self.control_status, self.key, self.passphrase,
             self.control_num_threads) = tst
            result = db_control.create_XFERO_Control(
                self.control_status, self.key, self.passphrase,
                self.control_num_threads,)

        # Perform the test
        expected_control_id = 1
        expected_control_status = 'STOP'
        expected_control_key = 'ANOTHER_KEY'
        expected_control_passphrase = 'DIFFERENT_PASSPHRASE'

        rows = db_control.update_XFERO_Control(
            expected_control_id, expected_control_status, expected_control_key,
            expected_control_passphrase)

        # Check update
        rows = db_control.read_XFERO_Control(expected_control_id)

        for control in rows:
            control_id = control['control_id']
            control_status = control['control_status']
            control_key = control['control_pgp_priv_key']
            control_pass = control['control_pgp_passphrase']

            self.assertEqual(
                expected_control_id, control_id, 'Unexpected value returned')
            self.assertEqual(
                expected_control_status, control_status,
                'Unexpected value returned')
            self.assertEqual(
                expected_control_key, control_key, 'Unexpected value returned')
            self.assertEqual(
                expected_control_passphrase, control_pass,
                'Unexpected value returned')

    def test_delete_XFERO_Control(self):
        '''

        **Purpose:**

        DELETE row on the XFERO_Control table with control_id = 1 and confirm that
        the deletion has been successful.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('START', 'KEY', 'PASSPHRASE', 1),]:

            (self.control_status, self.key, self.passphrase,
             self.control_num_threads) = tst
            result = db_control.create_XFERO_Control(
                self.control_status, self.key, self.passphrase,
                self.control_num_threads,)

        # Perform the test
        self.control_id = '1'
        rows = db_control.delete_XFERO_Control(self.control_id)

        # Check update
        config = configparser.RawConfigParser()
        try:
            config.read('conf/XFERO_config.ini')
        except configparser.Error as err:
            raise err

        xfero_db = config.get('database', 'db_location')
        con = lite.connect(xfero_db)

        try:
            cur = con.cursor()
            cur = con.execute("pragma foreign_keys=ON")
            cur.execute('SELECT count(*) FROM XFERO_Control')

        except lite.Error as err:

            print("Error %s:" % err.args[0])

        data = cur.fetchone()[0]
        expected = 0
        self.assertEqual(expected == data, True, "Unexpected row selected")

    def test_list_XFERO_Control(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Control table and confirm that all rows have
        been returned successfully.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 08/01/2014 | Chris Falck | Added additional inputs to be tested      |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''

        expected_tuple = ((1, 'START1', 'KEY', 'PASSPHRASE', 1),
                          (2, 'START2', 'KEY', 'PASSPHRASE', 1),
                          (3, 'START3', 'KEY', 'PASSPHRASE', 1),
                          (4, 'START4', 'KEY', 'PASSPHRASE', 1))

        for tst in [('START1', 'KEY', 'PASSPHRASE', 1),
                    ('START2', 'KEY', 'PASSPHRASE', 1),
                    ('START3', 'KEY', 'PASSPHRASE', 1),
                    ('START4', 'KEY', 'PASSPHRASE', 1),]:

            (self.control_status, self.key, self.passphrase,
             self.control_num_threads) = tst
            result = db_control.create_XFERO_Control(
                self.control_status, self.key, self.passphrase,
                self.control_num_threads,)

        rows = db_control.list_XFERO_Control()
        for control in rows:
            # self.assertIn(row, expected_tuple, 'Unexpected row selected')
            control_id = control['control_id']
            control_status = control['control_status']
            control_key = control['control_pgp_priv_key']
            control_pass = control['control_pgp_passphrase']

            actual_tuple = (
                control_id, control_status, control_key, control_pass)
            self.assertIn(
                actual_tuple, expected_tuple, 'Unexpected row returned')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
