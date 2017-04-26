#!/usr/bin/env python

import unittest
import configparser
import os
import sqlite3 as lite
from /xfero/.db import manage_workflow as db_workflow
from /xfero/.db import create_XFERO_DB as db


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```crud_XFERO_Workflow_Item```

    **Usage Notes:**

    XFERO stores the database location and database name in an ini file which is
    found in <INSTALL_DIR>/conf/XFERO_config.ini. Before proceeding with the test
    please ensure that the XFERO_config.ini file has been suitably modified for the
    purposes of this test.

    To aid unit testing on this table it is necessary to modify the crud_XFERO_Workflow_Item.py
    script as follows:

    #cur = con.execute("pragma foreign_keys=ON")
    cur = con.execute("pragma foreign_keys=OFF")

    The above must be reset to the following post unit testing:

    cur = con.execute("pragma foreign_keys=ON")
    #cur = con.execute("pragma foreign_keys=OFF")

    **Warning:**

    ALL DATABASE TABLE WILL BE DROPPED DURING THE EXECUTION OF THESE TESTS

    +------------+-------------+----------------------------------------------------+
    | Date       | Author      | Change Details                                     |
    +============+=============+====================================================+
    | 02/06/2013 | Chris Falck | Created                                            |
    +------------+-------------+----------------------------------------------------+
    | 14/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
    +------------+-------------+----------------------------------------------------+

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

        XFERO stores the database location and database name in an ini file which is
        found in <INTALL_DIR>/conf/XFERO_config.ini.

        '''

        config = configparser.RawConfigParser()
        try:
            config.read('conf/XFERO_config.ini')
        except configparser.Error as e:
            raise e

        xfero_db = config.get('database', 'db_location')

        # Delete the test DB
        os.remove(xfero_db)

    def test_create_XFERO_Workflow_Item(self):
        '''

        **Purpose:**

        INSERT rows into the XFERO_Workflow_Item table and confirm they have been successfully
        inserted

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 14/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        for t in [('3', 'move_file target_dir=/move/to/here', 'Move file to a specified directory', '1'),
                  ('3', 'move_file target_dir=/move/to/there',
                   'Move file to a specified directory', '2'),
                  ]:
            self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order = t

            result = db_workflow.create_XFERO_Workflow_Item(
                self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order)

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
            cur.execute('SELECT workflow_item_id FROM XFERO_Workflow_Item')

        except lite.Error as e:
            print("Error %s:" % e.args[0])

        expected_tuple = ((1,), (2,))

        rows = cur.fetchall()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row retrieved')

    def test_read_XFERO_Workflow_Item(self):
        '''

        **Purpose:**

        SELECT rows from the XFERO_Workflow_Item table with workflow_item_id = 1 and confirm that
        the rows returned are as expected

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 14/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        # Create the row in the database
        for t in [('3', 'move_file target_dir=/move/to/here', 'Move file to a specified directory', '1'),
                  ]:
            self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order = t
            result = db_workflow.create_XFERO_Workflow_Item(
                self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order)

        # Perform the select
        self.workflow_item_id = '1'
        rows = db_workflow.read_XFERO_Workflow_Item(self.workflow_item_id)

        expected_tuple = (
            1, 3, 'move_file target_dir=/move/to/here', 'Move file to a specified directory', 1)
        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_select_max_XFERO_Workflow_Item(self):
        '''

        **Purpose:**

        SELECT max row from the XFERO_Workflow_Item table with workflow_item_route and confirm that
        the rows returned are as expected

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 14/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        # Create the row in the database
        for t in [('3', 'move_file target_dir=/move/to/here', 'Move file to a specified directory', '1'),
                  ]:
            self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order = t
            result = db_workflow.create_XFERO_Workflow_Item(
                self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order)

        # Perform the select
        self.workflow_item_route = '3'
        rows = db_workflow.select_max_XFERO_Workflow_Item(
            self.workflow_item_route)

        expected_tuple = (1,)

        self.assertTupleEqual(expected_tuple, rows, 'Unexpected row retrieved')

    def test_update_XFERO_Workflow_Item(self):
        '''

        **Purpose:**

        UPDATE rows on the XFERO_Workflow_Item table with workflow_item_id = 1 and confirm that the
        update has been applied to the table.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 14/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        # Create the row in the database
        for t in [('3', 'move_file target_dir=/move/to/here', 'Move file to a specified directory', '1'),
                  ]:
            self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order = t
            result = db_workflow.create_XFERO_Workflow_Item(
                self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order)

        # Perform the select
        self.workflow_item_id = '1'
        self.workflow_item_route = '3'
        self.workflow_item_function_call = 'move_file target_dir=/not/there/here'
        self.workflow_item_description = 'Silly Function call'
        self.workflow_item_running_order = '2'

        rows = db_workflow.update_XFERO_Workflow_Item(
            self.workflow_item_id, self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order)

        # Check update
        rows = db_workflow.read_XFERO_Workflow_Item(self.workflow_item_id)

        expected_tuple = (
            1, 3, 'move_file target_dir=/not/there/here', 'Silly Function call', 2)

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_delete_XFERO_Workflow_Item(self):
        '''

        **Purpose:**

        DELETE rows on the XFERO_Workflow_Item table with workflow_item_id = 1 and confirm that the
        deletion has been successful.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 14/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        # Create the row in the database
        for t in [('3', 'move_file target_dir=/move/to/here', 'Move file to a specified directory', '1'),
                  ]:
            self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order = t
            result = db_workflow.create_XFERO_Workflow_Item(
                self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order)

        # Perform the select
        self.workflow_item_id = '1'
        rows = db_workflow.delete_XFERO_Workflow_Item(self.workflow_item_id)

        # Check update
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
            cur.execute('SELECT count(*) FROM XFERO_Workflow_Item')

        except lite.Error as e:
            print("Error %s:" % e.args[0])

        data = cur.fetchone()[0]
        expected = 0
        self.assertEqual(expected == data, True, "Unexpected row selected")

    def test_list_XFERO_Workflow_Item(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Workflow_Item table and confirm that all rows have been
        returned successfully.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 14/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        expected_tuple = ((1, 3, 'move_file target_dir=/move/to/here', 'Move file to a specified directory', 1),
                          (2, 3, 'move_file target_dir=/move/to/there', 'Move file to a specified directory', 2),)

        for t in [('3', 'move_file target_dir=/move/to/here', 'Move file to a specified directory', '1'),
                  ('3', 'move_file target_dir=/move/to/there',
                   'Move file to a specified directory', '2'),
                  ]:
            self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order = t
            result = db_workflow.create_XFERO_Workflow_Item(
                self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order)

        rows = db_workflow.list_XFERO_Workflow_Item()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')

    def test_list_XFERO_Workflow_Item_OrderBy_Run_Order(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Workflow_Item table WHERE workflow_item_route = 3
        ORDER_BY workflow run order and confirm that all rows have been returned successfully.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 14/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        expected_tuple = ((1, 3, 'move_file target_dir=/move/to/here', 'Move file to a specified directory', 1),
                          (2, 2, 'move_file target_dir=/move/to/there', 'Move file to a specified directory', 2),)

        for t in [('3', 'move_file target_dir=/move/to/here', 'Move file to a specified directory', '1'),
                  ('2', 'move_file target_dir=/move/to/there',
                   'Move file to a specified directory', '2'),
                  ]:
            self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order = t
            result = db_workflow.create_XFERO_Workflow_Item(
                self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order)

        self.workflow_item_route = str(3)
        rows = db_workflow.list_XFERO_Workflow_Item_OrderBy_Run_Order(
            self.workflow_item_route)
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')

    def test_list_XFERO_Workflow_Item_OrderBy_Run_Order_monitor(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Workflow_Item table WHERE workflow_item_route = 3
        ORDER_BY workflow run order and confirm that all rows have been returned successfully.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 14/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        expected_tuple = ((1, 3, 'move_file target_dir=/move/to/here', 'Move file to a specified directory', 1),
                          (2, 2, 'move_file target_dir=/move/to/there', 'Move file to a specified directory', 2),)

        for t in [('3', 'move_file target_dir=/move/to/here', 'Move file to a specified directory', '1'),
                  ('2', 'move_file target_dir=/move/to/there',
                   'Move file to a specified directory', '2'),
                  ]:
            self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order = t
            result = db_workflow.create_XFERO_Workflow_Item(
                self.workflow_item_route, self.workflow_item_function_call, self.workflow_item_description, self.workflow_item_running_order)

        self.workflow_item_route = str(3)
        rows = db_workflow.list_XFERO_Workflow_Item_OrderBy_Run_Order_monitor(
            self.workflow_item_route)

        for workflow in rows:
            wf_id = workflow['workflow_item_id']
            wf_route = workflow['workflow_item_route']
            wf_function_call = workflow['workflow_item_function_call']
            wf_args = workflow['workflow_item_args']
            wf_run_order = workflow['workflow_item_running_order']

            actual_tuple = (
                (wf_id, wf_route, wf_function_call, wf_args, wf_run_order))

            self.assertIn(
                actual_tuple, expected_tuple, 'Unexpected row selected')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
