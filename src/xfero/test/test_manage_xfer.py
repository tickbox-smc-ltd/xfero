#!/usr/bin/env python

import unittest
import configparser
import os
import sqlite3 as lite
from /xfero/.db import manage_xfer as db_xfer
from /xfero/.db import manage_partner as db_partner
from /xfero/.db import create_XFERO_DB as db


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```crud_XFERO_Xfer```
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

    def test_create_XFERO_Xfer(self):
        '''

        **Purpose:**

        INSERT rows into the XFERO_Xfer table and confirm they have been successfully
        inserted

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 08/01/2014 | Chris Falck | Added additional inputs to be tested               |
        +------------+-------------+----------------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+
        '''

        for t in [('2', '2', 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'params'),
                  ('2', '2',
                   'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'params'),
                  ('2', '2',
                   'send part=PART003, idf=SEND2GSI, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'params'),
                  ]:

            self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params = t

            result = db_xfer.create_XFERO_Xfer(
                self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params)

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
            cur.execute('SELECT xfer_id FROM XFERO_Xfer')

        except lite.Error as e:
            print("Error %s:" % e.args[0])

        expected_tuple = ((1,), (2,), (3,))

        rows = cur.fetchall()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row retrieved')

    def test_read_XFERO_Xfer(self):
        '''

        **Purpose:**

        SELECT rows from the XFERO_Xfer table with xfer_id = 1 and confirm that
        the rows returned are as expected

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        # Create the row in the database
        for t in [('2', '2', 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'params'),
                  ]:

            self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params = t

            result = db_xfer.create_XFERO_Xfer(
                self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params)

        self.xfer_id = '1'
        rows = db_xfer.read_XFERO_Xfer(self.xfer_id)

        expected_tuple = (
            1, 2, 2, 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'params')

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_update_XFERO_Xfer(self):
        '''

        **Purpose:**

        UPDATE rows on the XFERO_Xfer table with xfer_id = 1 and confirm that the
        update has been applied to the table.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        # Create the row in the database
        for t in [('2', '2', 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'params'),
                  ]:

            self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params = t

            result = db_xfer.create_XFERO_Xfer(
                self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params)

        self.xfer_id = '1'
        self.xfer_route = '3'
        self.xfer_call = 'send part=PART069, idf=SEND2ME, fname=FTSOUT, nfname={Remote_File_Name}'
        self.xfer_cotspattern = '3'
        self.xfer_cmd = 'cftutil'
        self.xfer_params = 'parmeters'

        rows = db_xfer.update_XFERO_Xfer(
            self.xfer_id, self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params)

        # Check update
        rows = db_xfer.read_XFERO_Xfer(self.xfer_id)

        expected_tuple = (
            1, 3, 3, 'send part=PART069, idf=SEND2ME, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters')

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_delete_XFERO_Xfer(self):
        '''

        **Purpose:**

        DELETE rows on the XFERO_Xfer table with xfer_id = 1 and confirm that the
        deletion has been successful.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        # Create the row in the database
        for t in [('2', '2', 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ]:

            self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params = t

            result = db_xfer.create_XFERO_Xfer(
                self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params)

        self.xfer_id = '1'
        rows = db_xfer.delete_XFERO_Xfer(self.xfer_id)

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
            cur.execute('SELECT count(*) FROM XFERO_Xfer')

        except lite.Error as e:
            print("Error %s:" % e.args[0])

        data = cur.fetchone()[0]
        expected = 0
        self.assertEqual(expected == data, True, "Unexpected row selected")

    def test_list_XFERO_Xfer(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Xfer table and confirm that all rows have been
        returned successfully.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        expected_tuple = ((1, 2, 2, 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                          (2, 2, 2,
                           'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'parmeters'),
                          (3, 2, 2, 'send part=PART003, idf=SEND2GSI, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'))

        for t in [('2', '2', 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ('2', '2',
                   'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'parmeters'),
                  ('2', '2',
                   'send part=PART003, idf=SEND2GSI, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ]:

            self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params = t
            result = db_xfer.create_XFERO_Xfer(
                self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params)

        rows = db_xfer.list_XFERO_Xfer()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')

    def test_list_XFERO_Xfer_Route(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Xfer table where xfer_route = 3 and confirm that
        all rows have been returned successfully.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 16/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        expected_tuple = ((1, 2, 2, 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                          (2, 2, 2, 'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'parmeters'))

        for t in [('2', '2', 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ('2', '2',
                   'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'parmeters'),
                  ('3', '2',
                   'send part=PART003, idf=SEND2GSI, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ]:

            self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params = t
            result = db_xfer.create_XFERO_Xfer(
                self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params)

        rows = db_xfer.list_XFERO_Xfer_Route(2)
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')

    def test_list_all_XFERO_Xfer_Route(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Xfer table where xfer_route = 2 and confirm that
        all rows have been returned successfully.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 16/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        expected_tuple = ((1, 2, 2, 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                          (2, 2, 2, 'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'parmeters'))

        for t in [('2', '2', 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ('2', '2',
                   'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'parmeters'),
                  ('3', '2',
                   'send part=PART003, idf=SEND2GSI, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ]:

            self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params = t
            result = db_xfer.create_XFERO_Xfer(
                self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params)

        rows = db_xfer.list_XFERO_Xfer_Route(2)
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')

    def test_count_XFERO_Xfer_Route(self):
        '''

        **Purpose:**

        COUNT ALL rows on the XFERO_Xfer table where xfer_route = 2 and confirm that
        all rows have been returned successfully.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 16/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''
        expected_tuple = ((1, 2, 2, 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                          (2, 2, 2, 'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'parmeters'))

        for t in [('2', '2', 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ('2', '2',
                   'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'parmeters'),
                  ('3', '2',
                   'send part=PART003, idf=SEND2GSI, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ]:

            self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params = t
            result = db_xfer.create_XFERO_Xfer(
                self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params)

        count = db_xfer.count_XFERO_Xfer_Route('2')

        self.assertEqual(count, 2, 'Incorrect row count returned')

    def test_join_xfer_partner(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Xfer table where xfer_route = 2 and confirm that
        all rows have been returned successfully.

        +------------+-------------+----------------------------------------------------+
        | Date       | Author      | Change Details                                     |
        +============+=============+====================================================+
        | 02/06/2013 | Chris Falck | Created                                            |
        +------------+-------------+----------------------------------------------------+
        | 16/01/2014 | Chris Falck | Tested to confirm changes to DB                    |
        +------------+-------------+----------------------------------------------------+

        '''

        expected_tuple = ((1, 2, 2, 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                          (2, 2, 2, 'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'parmeters'))
        for t in [
            ('WIN1', 'Win2008 Server 1', 'SFTPPlus', '192.168.0.65', '', '',
             '', '', 'xfero', 'xferopassword', '', '', '10021', '', '', 'key1'),
            ('WIN2', 'Win2008 Server 2', 'SFTPPlus', '192.168.0.66', '', '',
             '', '', 'xfero', 'xferopassword', '', '', '10221', '', '', 'key2'),
        ]:

            partner_service_name, partner_service_description, partner_COTS_type, partner_remote_system_id, partner_code, partner_mode, partner_local_username, partner_local_password, partner_remote_user, partner_remote_password, partner_CA_certificate, partner_cert_bundle, partner_control_port, partner_IDF, partner_parm, partner_pub_key = t
            result = db_partner.create_XFERO_Partner(partner_service_name, partner_service_description, partner_COTS_type, partner_remote_system_id, partner_code, partner_mode, partner_local_username,
                                                  partner_local_password, partner_remote_user, partner_remote_password, partner_CA_certificate, partner_cert_bundle, partner_control_port, partner_IDF, partner_parm, partner_pub_key)

        for t in [('2', '2', 'send part=PART001, idf=SEND2CPS, parm=0001, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ('2', '2',
                   'send part=PART002, idf=SEND2DRS, parm=0002, fname={Path_to_File_to_Send}', 'cftutil', 'parmeters'),
                  ('3', '2',
                   'send part=PART003, idf=SEND2GSI, fname=FTSOUT, nfname={Remote_File_Name}', 'cftutil', 'parmeters'),
                  ]:

            self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params = t
            result = db_xfer.create_XFERO_Xfer(
                self.xfer_route, self.xfer_cotspattern, self.xfer_call, self.xfer_cmd, self.xfer_params)

        rows = db_xfer.join_xfer_partner(2)
        for row in rows:
            print(row)
            # self.assertIn(row, expected_tuple, 'Unexpected row selected')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
