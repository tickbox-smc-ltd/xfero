#!/usr/bin/env python
'''Test Manage Route'''
import unittest
import configparser
import os
import sqlite3 as lite
from /xfero/.db import manage_route as db_route
from /xfero/.db import create_XFERO_DB as db


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```crud_XFERO_Route```

    **Usage Notes:**

    XFERO stores the database location and database name in an ini file which is
    found in <INSTALL_DIR>/conf/XFERO_config.ini. Before proceeding with the test
    please ensure that the XFERO_config.ini file has been suitably modified for the
    purposes of this test.

    To aid unit testing on this table it is necessary to modify the
    crud_XFERO_Route.py script as follows:

    #cur = con.execute("pragma foreign_keys=ON")
    cur = con.execute("pragma foreign_keys=OFF")

    The above must be reset to the following post unit testing:

    cur = con.execute("pragma foreign_keys=ON")
    #cur = con.execute("pragma foreign_keys=OFF")


    **Warning:**

    ALL DATABASE TABLE WILL BE DROPPED DURING THE EXECUTION OF THESE TESTS

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/06/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 13/01/2014 | Chris Falck | Tested to confirm changes to DB               |
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

    def test_create_XFERO_Route(self):
        '''

        **Purpose:**

        INSERT rows into the XFERO_Route table and confirm they have been
        successfully inserted

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''

        for tst in [('/ftran/CIS/ISCS', '^cis_123_XYZ', '1', '1'),
                    ('/ftran/UC/HMRC', '^UC_PYT_20120113', '2', '1'),
                    ('/ftran/DRS/XEROX', '_DRS_to_XEROX$', '3', '1'),
                    ('/ftran/CIS/FCO', '^FCO_123_XYZ', '2', '1'),
                    ('/ftran/CPS/CITIBANK', '^CITC_PYT_20120113', '1', '1'),
                    ('/ftran/CPS/ETSE', '_PAYT_TO_CITI$', '3', '1')
                   ]:

            (self.route_monitoreddir, self.route_filenamepattern,
             self.route_active, self.route_priority) = tst
            result = db_route.create_XFERO_Route(
                self.route_monitoreddir, self.route_filenamepattern,
                self.route_active, self.route_priority)

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
            cur.execute('SELECT route_id FROM XFERO_Route')

        except lite.Error as err:
            print("Error %s:" % err.args[0])

        expected_tuple = ((1,), (2,), (3,), (4,), (5,), (6,))

        rows = cur.fetchall()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row retrieved')

    def test_read_XFERO_Route(self):
        '''

        **Purpose:**

        SELECT rows from the XFERO_Route table with route_id = 1 and confirm that
        the rows returned are as expected

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        for tst in [('/ftran/CIS/ISCS', '^cis_123_XYZ', '1', '1'),
                   ]:

            (self.route_monitoreddir, self.route_filenamepattern,
             self.route_active, self.route_priority) = tst
            result = db_route.create_XFERO_Route(
                self.route_monitoreddir, self.route_filenamepattern,
                self.route_active, self.route_priority)

        self.route_id = '1'
        rows = db_route.read_XFERO_Route(self.route_id)

        expected_tuple = (1, '/ftran/CIS/ISCS', '^cis_123_XYZ', 1, 1)

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_update_XFERO_Route(self):
        '''

        **Purpose:**

        UPDATE rows on the XFERO_Route table with route_id = 3 and confirm that the
        update has been applied to the table.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        for tst in [('/ftran/CIS/ISCS', '^cis_123_XYZ', '1', '1'),
                   ]:

            (self.route_monitoreddir, self.route_filenamepattern,
             self.route_active, self.route_priority) = tst
            result = db_route.create_XFERO_Route(
                self.route_monitoreddir, self.route_filenamepattern,
                self.route_active, self.route_priority)

        self.route_id = '1'
        self.route_monitoreddir = '/ftran/test/chris'
        self.route_filenamepattern = '^Chris'
        self.route_active = '1'
        self.route_priority = '2'
        rows = db_route.update_XFERO_Route(
            self.route_monitoreddir, self.route_filenamepattern,
            self.route_active, self.route_priority, self.route_id)

        # Check update
        rows = db_route.read_XFERO_Route(self.route_id)

        expected_tuple = (1, '/ftran/test/chris', '^Chris', 1, 2)

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_delete_XFERO_Route(self):
        '''

        **Purpose:**

        DELETE rows on the XFERO_Route table with route_id = 1 and confirm that the
        deletion has been successful.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        for tst in [('/ftran/CIS/ISCS', '^cis_123_XYZ', '1', '1'),]:

            (self.route_monitoreddir, self.route_filenamepattern,
             self.route_active, self.route_priority) = tst
            result = db_route.create_XFERO_Route(
                self.route_monitoreddir, self.route_filenamepattern,
                self.route_active, self.route_priority)

        self.route_id = '1'
        rows = db_route.delete_XFERO_Route(self.route_id)

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
            cur.execute('SELECT count(*) FROM XFERO_Route')

        except lite.Error as err:
            print("Error %s:" % err.args[0])

        data = cur.fetchone()[0]
        expected = 0
        self.assertEqual(expected == data, True, "Unexpected row selected")

    def test_list_XFERO_Route(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Route table and confirm that all rows have
        been returned successfully.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        expected_tuple = ((1, '/ftran/CIS/ISCS', '^cis_123_XYZ', 1, 1),
                          (2, '/ftran/UC/HMRC', '^UC_PYT_20120113', 2, 1),
                          (3, '/ftran/DRS/XEROX', '_DRS_to_XEROX$', 3, 1),
                          (4, '/ftran/CIS/FCO', '^FCO_123_XYZ', 2, 1),
                          (5, '/ftran/CPS/CITIBANK',
                           '^CITC_PYT_20120113', 1, 1),
                          (6, '/ftran/CPS/ETSE', '_PAYT_TO_CITI$', 3, 1)
                         )

        for tst in [('/ftran/CIS/ISCS', '^cis_123_XYZ', '1', '1'),
                    ('/ftran/UC/HMRC', '^UC_PYT_20120113', '2', '1'),
                    ('/ftran/DRS/XEROX', '_DRS_to_XEROX$', '3', '1'),
                    ('/ftran/CIS/FCO', '^FCO_123_XYZ', '2', '1'),
                    ('/ftran/CPS/CITIBANK', '^CITC_PYT_20120113', '1', '1'),
                    ('/ftran/CPS/ETSE', '_PAYT_TO_CITI$', '3', '1')
                   ]:

            (self.route_monitoreddir, self.route_filenamepattern,
             self.route_active, self.route_priority) = tst
            result = db_route.create_XFERO_Route(
                self.route_monitoreddir, self.route_filenamepattern,
                self.route_active, self.route_priority)

        rows = db_route.list_XFERO_Route()

        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')

    def test_list_XFERO_Route_Priority(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Route table where the Priority assigned to the
        routes is set to 3 and confirm that all rows have been returned
        successfully.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 13/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        expected_tuple = ((3, '/ftran/DRS/XEROX', '_DRS_to_XEROX$', 1, 3),
                          (6, '/ftran/CPS/ETSE', '_PAYT_TO_CITI$', 1, 3)
                         )

        for tst in [('/ftran/CIS/ISCS', '^cis_123_XYZ', '1', '1'),
                    ('/ftran/UC/HMRC', '^UC_PYT_20120113', '1', '2'),
                    ('/ftran/DRS/XEROX', '_DRS_to_XEROX$', '1', '3'),
                    ('/ftran/CIS/FCO', '^FCO_123_XYZ', '1', '2'),
                    ('/ftran/CPS/CITIBANK', '^CITC_PYT_20120113', '1', '1'),
                    ('/ftran/CPS/ETSE', '_PAYT_TO_CITI$', '1', '3')
                   ]:

            (self.route_monitoreddir, self.route_filenamepattern,
             self.route_active, self.route_priority) = tst
            result = db_route.create_XFERO_Route(
                self.route_monitoreddir, self.route_filenamepattern,
                self.route_active, self.route_priority)

        priority = '3'
        rows = db_route.list_XFERO_Route_Priority_Route(priority)

        for route in rows:
            route_id = route['route_id']
            route_monitoreddir = route['route_monitoreddir']
            route_filenamepattern = route['route_filenamepattern']
            route_active = route['route_active']
            route_priority = route['route_priority']

            actual_tuple = (
                (route_id, route_monitoreddir, route_filenamepattern,
                 route_active, route_priority))

            self.assertIn(
                actual_tuple, expected_tuple, 'Unexpected row selected')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
