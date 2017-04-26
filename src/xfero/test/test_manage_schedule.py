#!/usr/bin/env python

import unittest
import configparser
import os
import sqlite3 as lite
from /xfero/.db import manage_schedule as db_schedule
from /xfero/.db import create_XFERO_DB as db


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```crud_XFERO_Scheduled_Task```

    **Usage Notes:**

    XFERO stores the database location and database name in an ini file which is
    found in <INSTALL_DIR>/conf/XFERO_config.ini. Before proceeding with the test
    please ensure that the XFERO_config.ini file has been suitably modified for the
    purposes of this test.

    **Warning:**

    ALL DATABASE TABLE WILL BE DROPPED DURING THE EXECUTION OF THESE TESTS

    +------------+-------------+----------------------------------------------------+
    | Date       | Author      | Change Details                                     |
    +============+=============+====================================================+
    | 02/06/2013 | Chris Falck | Created                                            |
    +------------+-------------+----------------------------------------------------+
    | 13/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
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

    def test_create_XFERO_Scheduled_Task(self):
        '''

        **Purpose:**

        INSERT rows into the XFERO_Scheduled_Task table and confirm they have been successfully
        inserted

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''

        for t in [('FTH Housekeeping1', 'housekeeping1', 'NULL', 'NULL', 'NULL', 'NULL', 'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping2', 'housekeeping2', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping3', 'housekeeping3', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping4', 'housekeeping4', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping5', 'housekeeping5', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping6', 'housekeeping6', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping7', 'housekeeping7', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping8', 'housekeeping8', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping9', 'housekeeping9', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping10', 'housekeeping10', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ]:

            self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day, self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active = t
            result = db_schedule.create_XFERO_Scheduled_Task(self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day,
                                                          self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active)

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
            cur.execute('SELECT scheduled_task_id FROM XFERO_Scheduled_Task')

        except lite.Error as e:
            print("Error %s:" % e.args[0])

        expected_tuple = (
            (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,))

        rows = cur.fetchall()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row retrieved')

    def test_read_XFERO_Scheduled_Task(self):
        '''

        **Purpose:**

        SELECT rows from the XFERO_Scheduled_Task table with scheduled_task_id = 1 and confirm that
        the rows returned are as expected

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        # Create the row in the database
        for t in [('FTH Housekeeping1', 'housekeeping1', 'NULL', 'NULL', 'NULL', 'NULL', 'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ]:

            self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day, self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active = t
            result = db_schedule.create_XFERO_Scheduled_Task(self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day,
                                                          self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active)

        self.scheduled_task_id = '1'
        rows = db_schedule.read_XFERO_Scheduled_Task(self.scheduled_task_id,)

        expected_tuple = (1, 'FTH Housekeeping1', 'housekeeping1', 'NULL', 'NULL', 'NULL',
                          'NULL', 'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1')

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_update_XFERO_Scheduled_Task(self):
        '''

        **Purpose:**

        UPDATE rows on the XFERO_Scheduled_Task table with scheduled_task_id = 2 and confirm that the
        update has been applied to the table.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        # Create the row in the database
        for t in [('FTH Housekeeping1', 'housekeeping1', 'NULL', 'NULL', 'NULL', 'NULL', 'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', 1),
                  ]:

            self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day, self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active = t
            result = db_schedule.create_XFERO_Scheduled_Task(self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day,
                                                          self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active)

        self.scheduled_task_id = '1'
        self.scheduled_task_name = 'FTH HK'
        self.scheduled_task_function = 'housekeeping'
        self.scheduled_task_year = 'NULL'
        self.scheduled_task_month = 'NULL'
        self.scheduled_task_day = 'NULL'
        self.scheduled_task_week = 'NULL'
        self.scheduled_task_day_of_week = 'mon-sun'
        self.scheduled_task_hour = '*'
        self.scheduled_task_minute = '0-59'
        self.scheduled_task_second = '*/25'
        self.scheduled_task_args = '[`\/FTH/logs\', \'^FTH\', 7, False]'
        self.scheduled_task_active = '1'

        rows = db_schedule.update_XFERO_Scheduled_Task(self.scheduled_task_id, self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day,
                                                    self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active)

        # Check update
        rows = db_schedule.read_XFERO_Scheduled_Task(self.scheduled_task_id)

        expected_tuple = (1, 'FTH HK', 'housekeeping', 'NULL', 'NULL', 'NULL', 'NULL',
                          'mon-sun', '*', '0-59', '*/25', "[`\\/FTH/logs', '^FTH', 7, False]", '1')

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_delete_XFERO_Scheduled_Task(self):
        '''

        **Purpose:**

        DELETE rows on the XFERO_Scheduled_Task table with scheduled_task_id = 1 and confirm that the
        deletion has been successful.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        # Create the row in the database
        for t in [('FTH Housekeeping1', 'housekeeping1', 'NULL', 'NULL', 'NULL', 'NULL', 'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ]:

            self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day, self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active = t
            result = db_schedule.create_XFERO_Scheduled_Task(self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day,
                                                          self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active)

        self.scheduled_task_id = '1'
        rows = db_schedule.delete_XFERO_Scheduled_Task(self.scheduled_task_id)

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
            cur.execute('SELECT count(*) FROM XFERO_Scheduled_Task')

        except lite.Error as e:
            print("Error %s:" % e.args[0])

        data = cur.fetchone()[0]
        expected = 0
        self.assertEqual(expected == data, True, "Unexpected row selected")

    def test_list_XFERO_Scheduled_Task(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Scheduled_Task table and confirm that all rows have been
        returned successfully.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        expected_tuple = ((1, 'FTH Housekeeping1', 'housekeeping1', 'NULL', 'NULL', 'NULL', 'NULL', 'mon-sun', '*', '0-59', '*/25', "['/FTH/logs', '^FTH', 7, False]", '1'),
                          (2, 'FTH Housekeeping2', 'housekeeping2', 'NULL', 'NULL', 'NULL', 'NULL',
                           'mon-sun', '*', '0-59', '*/25', "['/FTH/logs', '^FTH', 7, False]", '1'),
                          (3, 'FTH Housekeeping3', 'housekeeping3', 'NULL', 'NULL', 'NULL', 'NULL',
                           'mon-sun', '*', '0-59', '*/25', "['/FTH/logs', '^FTH', 7, False]", '1'),
                          (4, 'FTH Housekeeping4', 'housekeeping4', 'NULL', 'NULL', 'NULL', 'NULL',
                           'mon-sun', '*', '0-59', '*/25', "['/FTH/logs', '^FTH', 7, False]", '1'),
                          (5, 'FTH Housekeeping5', 'housekeeping5', 'NULL', 'NULL', 'NULL', 'NULL',
                           'mon-sun', '*', '0-59', '*/25', "['/FTH/logs', '^FTH', 7, False]", '1'),
                          (6, 'FTH Housekeeping6', 'housekeeping6', 'NULL', 'NULL', 'NULL', 'NULL',
                           'mon-sun', '*', '0-59', '*/25', "['/FTH/logs', '^FTH', 7, False]", '1'),
                          (7, 'FTH Housekeeping7', 'housekeeping7', 'NULL', 'NULL', 'NULL', 'NULL',
                           'mon-sun', '*', '0-59', '*/25', "['/FTH/logs', '^FTH', 7, False]", '1'),
                          (8, 'FTH Housekeeping8', 'housekeeping8', 'NULL', 'NULL', 'NULL', 'NULL',
                           'mon-sun', '*', '0-59', '*/25', "['/FTH/logs', '^FTH', 7, False]", '1'),
                          (9, 'FTH Housekeeping9', 'housekeeping9', 'NULL', 'NULL', 'NULL', 'NULL',
                           'mon-sun', '*', '0-59', '*/25', "['/FTH/logs', '^FTH', 7, False]", '1'),
                          (10, 'FTH Housekeeping10', 'housekeeping10', 'NULL', 'NULL', 'NULL', 'NULL', 'mon-sun', '*', '0-59', '*/25', "['/FTH/logs', '^FTH', 7, False]", '1'))

        for t in [('FTH Housekeeping1', 'housekeeping1', 'NULL', 'NULL', 'NULL', 'NULL', 'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping2', 'housekeeping2', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping3', 'housekeeping3', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping4', 'housekeeping4', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping5', 'housekeeping5', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping6', 'housekeeping6', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping7', 'housekeeping7', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping8', 'housekeeping8', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping9', 'housekeeping9', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ('FTH Housekeeping10', 'housekeeping10', 'NULL', 'NULL', 'NULL', 'NULL',
                   'mon-sun', '*', '0-59', '*/25', '[\'/FTH/logs\', \'^FTH\', 7, False]', '1'),
                  ]:

            self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day, self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active = t
            result = db_schedule.create_XFERO_Scheduled_Task(self.scheduled_task_name, self.scheduled_task_function, self.scheduled_task_year, self.scheduled_task_month, self.scheduled_task_day,
                                                          self.scheduled_task_week, self.scheduled_task_day_of_week, self.scheduled_task_hour, self.scheduled_task_minute, self.scheduled_task_second, self.scheduled_task_args, self.scheduled_task_active)

        rows = db_schedule.list_XFERO_Scheduled_Task()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
