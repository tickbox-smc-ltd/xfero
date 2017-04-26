#!/usr/bin/env python
'''Test Manage Function'''
import unittest
import configparser
import os
import sqlite3 as lite
from /xfero/.db import manage_function as db_function
from /xfero/.db import create_XFERO_DB as db


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```crud_XFERO_Function```

    **Usage Notes:**

    XFERO stores the database location and database name in an ini file which is
    found in <INSTALL_DIR>/conf/XFERO_config.ini. Before proceeding with the test
    please ensure that the XFERO_config.ini file has been suitably modified for the
    purposes of this test.

    **Warning:**

    ALL DATABASE TABLE WILL BE DROPPED DURING THE EXECUTION OF THESE TESTS

    External dependencies

    os (/xfero/.test.test_manage_function)
    /xfero/
      db
        create_XFERO_DB (/xfero/.test.test_manage_function)
        manage_function (/xfero/.test.test_manage_function)

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

    def test_create_XFERO_Function(self):
        '''

        **Purpose:**

        INSERT rows into the XFERO_Function table and confirm they have been
        successfully inserted

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

        for tst in [('move_file', 'Copy_File',
                     'Function to Move a file to a specified directory',
                     'target_directory={Enter_value}'),
                    ('compress_entities', 'Manage_Archives',
                     'Function to tar.gz or zip files',
                     'entities={Enter_value} archive_name={Enter_value} \
                     subdir={Enter_value}'),
                   ]:

            (self.function_name, self.function_class, self.function_description,
             self.function_prototype) = tst

            result = db_function.create_XFERO_Function(
                self.function_name, self.function_class,
                self.function_description, self.function_prototype)

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
            cur.execute('SELECT function_id FROM XFERO_Function')

        except lite.Error as err:

            print("Error %s:" % err.args[0])

        expected_tuple = (
            (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,))

        rows = cur.fetchall()
        for row in rows:

            self.assertIn(row, expected_tuple, 'Unexpected row retrieved')

    def test_read_XFERO_Function(self):
        '''

        **Purpose:**

        SELECT rows from the XFERO_Function table with function_id = 1 and confirm
        that the rows returned are as expected

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('avcheck', 'Anti_Virus',
                     'Function to Anti-Virus check a file', 'NULL'),
                   ]:

            (self.function_name,
             self.function_class,
             self.function_description,
             self.function_prototype) = tst
            result = db_function.create_XFERO_Function(self.function_name,
                                                    self.function_class,
                                                    self.function_description,
                                                    self.function_prototype)

        # Perform the select
        self.function_id = '1'
        rows = db_function.read_XFERO_Function(self.function_id)
        expected_tuple = (
            1, 'avcheck', 'Function to Anti-Virus check a file', 'NULL')

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_read_with_name_XFERO_Function(self):
        '''

        **Purpose:**

        SELECT rows from the XFERO_Function table with function_name and confirm
        that the rows returned are as expected

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('avcheck', 'Anti_Virus',
                     'Function to Anti-Virus check a file', 'NULL'),
                   ]:

            (self.function_name, self.function_class, self.function_description,
             self.function_prototype) = tst
            result = db_function.create_XFERO_Function(
                self.function_name, self.function_class,
                self.function_description, self.function_prototype)

        # Perform the select
        self.function_name = 'avcheck'
        rows = db_function.read_with_name_XFERO_Function(self.function_name)
        expected_tuple = (
            1, 'avcheck', 'Function to Anti-Virus check a file', 'NULL')

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_update_XFERO_Function(self):
        '''

        **Purpose:**

        UPDATE rows on the XFERO_Function table with function_id = 1 and confirm
        that the update has been applied to the table.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('avcheck', 'Anti_Virus',
                     'Function to Anti-Virus check a file', 'NULL'),
                   ]:

            (self.function_name, self.function_class, self.function_description,
             self.function_prototype) = tst
            result = db_function.create_XFERO_Function(
                self.function_name, self.function_class,
                self.function_description, self.function_prototype)

        # Perform the select
        self.function_id = '1'
        self.function_name = 'new_func'
        self.function_description = 'Function to Anti-Virus check a file'
        self.function_prototype = 'NULL'
        rows = db_function.update_XFERO_Function(
            self.function_id, self.function_name, self.function_class,
            self.function_description, self.function_prototype)

        expected_tuple = (
            1, 'new_func', 'Anti_Virus', 'Function to Anti-Virus check a file',
            'NULL')

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_delete_XFERO_Function(self):
        '''

        **Purpose:**

        DELETE rows on the XFERO_Function table with function_id = 1 and confirm
        that the deletion has been successful.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('avcheck', 'Function to Anti-Virus check a file', 'NULL'),
                   ]:

            (self.function_name, self.function_description,
             self.function_prototype) = tst
            result = db_function.create_XFERO_Function(
                self.function_name, self.function_description,
                self.function_prototype)

        # Perform the select
        self.function_id = '1'
        rows = db_function.delete_XFERO_Function(self.function_id)

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
            cur.execute('SELECT count(*) FROM XFERO_Function')
        except lite.Error as err:
            print("Error %s:" % err.args[0])

        data = cur.fetchone()[0]
        expected = 0
        self.assertEqual(expected == data, True, "Unexpected row selected")

    def test_list_XFERO_Function(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Function table and confirm that all rows have
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
        expected_tuple = ((1, 'move_file',
                           'Function to Move a file to a specified directory',
                           'target_directory={Enter_value}'),
                          (2, 'xfer_file',
                           'Function to transfer a file', 'NULL'),
                          (3, 'XFERO_exit', 'Function to enable the execution of \
                           external programs',
                           'exit_script={Enter_value}'),
                          (4, 'compress_entities', 'Function to tar.gz or \
                           zip files',
                           'entities={Enter_value} archive_name={Enter_value} \
                           subdir={Enter_value}'),
                          (5, 'xform',
                           'Function to transform a file name', 'NULL'),
                          (6, 'encrypt', 'Function to encrypt a file', 'NULL'),
                          (7, 'decrypt', 'Function to decrypt a file', 'NULL'),
                          (8, 'cksum',
                           'Function to produce a Checksum of a file', 'NULL'),
                          (9, 'split_file',
                           'Function to split a large file into smaller files',
                           'NULL'),
                          (10, 'merge_file',
                           'Function to merge split file', 'NULL'),
                          (11, 'avcheck', 'Function to Anti-Virus check a file',
                           'NULL'))

        for tst in [('move_file',
                     'Function to Move a file to a specified directory',
                     'target_directory={Enter_value}'),
                    ('xfer_file', 'Function to transfer a file', 'NULL'),
                    ('XFERO_exit', 'Function to enable the execution of external \
                     programs',
                     'exit_script={Enter_value}'),
                    ('compress_entities', 'Function to tar.gz or zip files',
                     'entities={Enter_value} archive_name={Enter_value} \
                     subdir={Enter_value}'),
                    ('xform', 'Function to transform a file name', 'NULL'),
                    ('encrypt', 'Function to encrypt a file', 'NULL'),
                    ('decrypt', 'Function to decrypt a file', 'NULL'),
                    ('cksum',
                     'Function to produce a Checksum of a file', 'NULL'),
                    ('split_file',
                     'Function to split a large file into smaller files',
                     'NULL'),
                    ('merge_file', 'Function to merge split file', 'NULL'),
                    ('avcheck', 'Function to Anti-Virus check a file', 'NULL'),
                   ]:

            (self.function_name, self.function_description,
             self.function_prototype) = tst
            result = db_function.create_XFERO_Function(
                self.function_name, self.function_description,
                self.function_prototype)

        rows = db_function.list_XFERO_Function()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
