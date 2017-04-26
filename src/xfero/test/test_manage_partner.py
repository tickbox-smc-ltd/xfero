#!/usr/bin/env python
''' Test Manage Partner'''
import unittest
import configparser
import os
import sqlite3 as lite
from /xfero/.db import manage_partner as db_partner
from /xfero/.db import create_XFERO_DB as db


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```crud_XFERO_Partner```

    **Usage Notes:**

    XFERO stores the database location and database name in an ini file which is
    found in <INSTALL_DIR>/conf/XFERO_config.ini. Before proceeding with the test
    please ensure that the XFERO_config.ini file has been suitably modified for the
    purposes of this test.

    **Warning:**

    ALL DATABASE TABLE WILL BE DROPPED DURING THE EXECUTION OF THESE TESTS

    *External dependencies*

    os (/xfero/.test.test_manage_partner)
    /xfero/
      db
        create_XFERO_DB (/xfero/.test.test_manage_partner)
        manage_partner (/xfero/.test.test_manage_partner)

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

    def test_create_XFERO_Partner(self):
        '''

        **Purpose:**

        INSERT rows into the XFERO_Partner table and confirm they have been
        successfully inserted.

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

        for tst in [('WIN1', 'Win2008 Server 1', 'SFTPPlus', '192.168.0.65', '',
                     '', '', '', 'xfero', 'xferopassword', '', '', '10021', '', '',
                     'key1'),
                    ('WIN2', 'Win2008 Server 2', 'SFTPPlus', '192.168.0.66', '',
                     '', '', '', 'xfero', 'xferopassword', '', '', '10221', '', '',
                     'key2'),
                    ('CENT1', 'CentOS6 Server 1', 'SFTPPlus', '192.168.0.11',
                     '', '', '', '', 'xfero', 'xferopassword', '', '', '10121', '',
                     '', 'key3'),
                    ('CENT2', 'CentOS6 Server 2', 'SFTPPlus', '192.168.0.12',
                     '', '', '', '', 'xfero', 'xferopassword', '', '', '10321', '',
                     '', 'key4'),]:

            (partner_service_name, partner_service_description,
             partner_COTS_type, partner_remote_system_id, partner_code,
             partner_mode, partner_local_username, partner_local_password,
             partner_remote_user, partner_remote_password,
             partner_CA_certificate, partner_cert_bundle, partner_control_port,
             partner_IDF, partner_parm, partner_pub_key) = tst
            result = db_partner.create_XFERO_Partner(partner_service_name,
                                                  partner_service_description,
                                                  partner_COTS_type,
                                                  partner_remote_system_id,
                                                  partner_code, partner_mode,
                                                  partner_local_username,
                                                  partner_local_password,
                                                  partner_remote_user,
                                                  partner_remote_password,
                                                  partner_CA_certificate,
                                                  partner_cert_bundle,
                                                  partner_control_port,
                                                  partner_IDF, partner_parm,
                                                  partner_pub_key)

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
            cur.execute('SELECT partner_id FROM XFERO_Partner')

        except lite.Error as err:
            print("Error %s:" % err.args[0])

        expected_tuple = ((1,), (2,), (3,), (4,))

        rows = cur.fetchall()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row retrieved')

    def test_read_XFERO_Partner(self):
        '''

        **Purpose:**

        SELECT a specified row from the XFERO_Patner table with partner_id = 1 and
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
        for tst in [('WIN1', 'Win2008 Server 1', 'SFTPPlus', '192.168.0.65', '',
                     '', '', '', 'xfero', 'xferopassword', '', '', '10021', '', '',
                     'key1'),]:

            (partner_service_name, partner_service_description,
             partner_COTS_type, partner_remote_system_id, partner_code,
             partner_mode, partner_local_username, partner_local_password,
             partner_remote_user, partner_remote_password,
             partner_CA_certificate, partner_cert_bundle, partner_control_port,
             partner_IDF, partner_parm, partner_pub_key) = tst
            result = db_partner.create_XFERO_Partner(partner_service_name,
                                                  partner_service_description,
                                                  partner_COTS_type,
                                                  partner_remote_system_id,
                                                  partner_code,
                                                  partner_mode,
                                                  partner_local_username,
                                                  partner_local_password,
                                                  partner_remote_user,
                                                  partner_remote_password,
                                                  partner_CA_certificate,
                                                  partner_cert_bundle,
                                                  partner_control_port,
                                                  partner_IDF, partner_parm,
                                                  partner_pub_key)

        # Perform the select
        self.partner_id = '1'
        rows = db_partner.read_XFERO_Partner(self.partner_id)

        expected_tuple = (1, 'WIN1', 'Win2008 Server 1', 'SFTPPlus',
                          '192.168.0.65', '', '', '', '', 'xfero', 'xferopassword',
                          '', '', 10021, '', '', 'key1')

        self.assertTupleEqual(expected_tuple, rows, 'Unexpected row retrieved')

    def test_read_psn_XFERO_Partner(self):
        '''

        **Purpose:**

        SELECT a specified row from the XFERO_Patner table with
        partner_service_name and confirm that the row returned is as expected

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('WIN1', 'Win2008 Server 1', 'SFTPPlus', '192.168.0.65', '',
                     '', '', '', 'xfero', 'xferopassword', '', '', '10021', '', '',
                     'key1'),]:

            (partner_service_name, partner_service_description,
             partner_COTS_type, partner_remote_system_id, partner_code,
             partner_mode, partner_local_username, partner_local_password,
             partner_remote_user, partner_remote_password,
             partner_CA_certificate, partner_cert_bundle, partner_control_port,
             partner_IDF, partner_parm, partner_pub_key) = tst
            result = db_partner.create_XFERO_Partner(partner_service_name,
                                                  partner_service_description,
                                                  partner_COTS_type,
                                                  partner_remote_system_id,
                                                  partner_code, partner_mode,
                                                  partner_local_username,
                                                  partner_local_password,
                                                  partner_remote_user,
                                                  partner_remote_password,
                                                  partner_CA_certificate,
                                                  partner_cert_bundle,
                                                  partner_control_port,
                                                  partner_IDF, partner_parm,
                                                  partner_pub_key)

        # Perform the select
        self.partner_service_name = 'WIN1'
        rows = db_partner.read_psn_XFERO_Partner(self.partner_service_name)
        for row in rows:
            expected_tuple = (1, 'WIN1', 'Win2008 Server 1', 'SFTPPlus',
                              '192.168.0.65', '', '', '', '', 'xfero',
                              'xferopassword', '', '', 10021, '', '', 'key1')
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_update_XFERO_Partner(self):
        '''

        **Purpose:**

        UPDATE row on the XFERO_Partner table with partner_id = 1 and confirm that
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
        for tst in [('WIN1', 'Win2008 Server 1', 'SFTPPlus', '192.168.0.65', '',
                     '', '', '', 'xfero', 'xferopassword', '', '', '10021', '', '',
                     'key1'),]:

            (partner_service_name, partner_service_description,
             partner_COTS_type, partner_remote_system_id, partner_code,
             partner_mode, partner_local_username, partner_local_password,
             partner_remote_user, partner_remote_password,
             partner_CA_certificate, partner_cert_bundle, partner_control_port,
             partner_IDF, partner_parm, partner_pub_key) = tst
            result = db_partner.create_XFERO_Partner(partner_service_name,
                                                  partner_service_description,
                                                  partner_COTS_type,
                                                  partner_remote_system_id,
                                                  partner_code, partner_mode,
                                                  partner_local_username,
                                                  partner_local_password,
                                                  partner_remote_user,
                                                  partner_remote_password,
                                                  partner_CA_certificate,
                                                  partner_cert_bundle,
                                                  partner_control_port,
                                                  partner_IDF, partner_parm,
                                                  partner_pub_key)

        # Perform the select

        self.partner_id = '1'
        self.partner_service_name = 'Test'
        self.partner_service_description = 'TEST'
        self.partner_COTS_type = 'Testing'
        self.partner_remote_system_id = 'Falck'
        self.partner_code = 'b'
        self.partner_mode = 'w'
        self.partner_local_username = 'test'
        self.partner_local_password = 'test'
        self.partner_remote_user = 'test'
        self.partner_remote_password = 'test'
        self.partner_CA_certificate = 'CA_cert_bundle'
        self.partner_cert_bundle = 'cert_bundle'
        self.partner_control_port = '10121'
        self.partner_IDF = 'idf'
        self.partner_parm = 'parm'
        self.partner_pub_key = 'pub_key'

        result = db_partner.update_XFERO_Partner(self.partner_id,
                                              self.partner_service_name,
                                              self.partner_service_description,
                                              self.partner_COTS_type,
                                              self.partner_remote_system_id,
                                              self.partner_code,
                                              self.partner_mode,
                                              self.partner_local_username,
                                              self.partner_local_password,
                                              self.partner_remote_user,
                                              self.partner_remote_password,
                                              self.partner_CA_certificate,
                                              self.partner_cert_bundle,
                                              self.partner_control_port,
                                              self.partner_IDF,
                                              self.partner_parm,
                                              self.partner_pub_key)

        # Check update
        rows = db_partner.read_XFERO_Partner(self.partner_id)

        expected_tuple = (1, 'Test', 'TEST', 'Testing', 'Falck', 'b', 'w',
                          'test', 'test', 'test', 'test', 'CA_cert_bundle',
                          'cert_bundle', 10121, 'idf', 'parm', 'pub_key')

        # for row in rows:
        self.assertTupleEqual(expected_tuple, rows, 'Unexpected row retrieved')

    def test_delete_XFERO_Partner(self):
        '''

        **Purpose:**

        DELETE row on the XFERO_Partner table with Partner ID = 1 and confirm that
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
        for tst in [('WIN1', 'Win2008 Server 1', 'SFTPPlus', '192.168.0.65', '',
                     '', '', '', 'xfero', 'xferopassword', '', '', '10021', '', '',
                     'key1'),]:

            (partner_service_name, partner_service_description,
             partner_COTS_type, partner_remote_system_id, partner_code,
             partner_mode, partner_local_username, partner_local_password,
             partner_remote_user, partner_remote_password,
             partner_CA_certificate, partner_cert_bundle, partner_control_port,
             partner_IDF, partner_parm, partner_pub_key) = tst
            result = db_partner.create_XFERO_Partner(partner_service_name,
                                                  partner_service_description,
                                                  partner_COTS_type,
                                                  partner_remote_system_id,
                                                  partner_code, partner_mode,
                                                  partner_local_username,
                                                  partner_local_password,
                                                  partner_remote_user,
                                                  partner_remote_password,
                                                  partner_CA_certificate,
                                                  partner_cert_bundle,
                                                  partner_control_port,
                                                  partner_IDF,
                                                  partner_parm,
                                                  partner_pub_key)

        # Perform the test
        self.partner_id = '1'
        rows = db_partner.delete_XFERO_Partner(self.partner_id)

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
            cur.execute('SELECT count(*) FROM XFERO_Partner')

        except lite.Error as e:
            print("Error %s:" % e.args[0])

        data = cur.fetchone()[0]
        expected = 0
        self.assertEqual(expected == data, True, "Unexpected row selected")

    def test_list_XFERO_Partner(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_Partner table and confirm that all rows have
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
        expected_tuple = ((1, 'WIN1', 'Win2008 Server 1', 'SFTPPlus',
                           '192.168.0.65', '', '', '', '', 'xfero', 'xferopassword',
                           '', '', 10021, '', '', 'key1'),
                          (2, 'WIN2', 'Win2008 Server 2', 'SFTPPlus',
                           '192.168.0.66', '', '', '', '', 'xfero', 'xferopassword',
                           '', '', 10221, '', '', 'key2'),
                          (3, 'CENT1', 'CentOS6 Server 1', 'SFTPPlus',
                           '192.168.0.11', '', '', '', '', 'xfero', 'xferopassword',
                           '', '', 10121, '', '', 'key3'),
                          (4, 'CENT2', 'CentOS6 Server 2', 'SFTPPlus',
                           '192.168.0.12', '', '', '', '', 'xfero', 'xferopassword',
                           '', '', 10321, '', '', 'key4'))

        for tst in [('WIN1', 'Win2008 Server 1', 'SFTPPlus', '192.168.0.65', '',
                     '', '', '', 'xfero', 'xferopassword', '', '', '10021', '', '',
                     'key1'),
                    ('WIN2', 'Win2008 Server 2', 'SFTPPlus', '192.168.0.66', '',
                     '', '', '', 'xfero', 'xferopassword', '', '', '10221', '', '',
                     'key2'),
                    ('CENT1', 'CentOS6 Server 1', 'SFTPPlus', '192.168.0.11',
                     '', '', '', '', 'xfero', 'xferopassword', '', '', '10121', '',
                     '', 'key3'),
                    ('CENT2', 'CentOS6 Server 2', 'SFTPPlus', '192.168.0.12',
                     '', '', '', '', 'xfero', 'xferopassword', '', '', '10321', '',
                     '', 'key4'),
                   ]:

            (partner_service_name, partner_service_description,
             partner_COTS_type, partner_remote_system_id, partner_code,
             partner_mode, partner_local_username, partner_local_password,
             partner_remote_user, partner_remote_password,
             partner_CA_certificate, partner_cert_bundle, partner_control_port,
             partner_IDF, partner_parm, partner_pub_key) = tst
            result = db_partner.create_XFERO_Partner(partner_service_name,
                                                  partner_service_description,
                                                  partner_COTS_type,
                                                  partner_remote_system_id,
                                                  partner_code, partner_mode,
                                                  partner_local_username,
                                                  partner_local_password,
                                                  partner_remote_user,
                                                  partner_remote_password,
                                                  partner_CA_certificate,
                                                  partner_cert_bundle,
                                                  partner_control_port,
                                                  partner_IDF, partner_parm,
                                                  partner_pub_key)

        rows = db_partner.list_XFERO_Partner()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')

    def test_list_service_name_XFERO_Partner(self):
        '''

        **Purpose:**

        SELECT ALL rows from the XFERO_Partner table returning only the service
        name and confirm that all rows have been returned successfully.

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
        expected_tuple = (('WIN1',), ('WIN2',), ('CENT1',), ('CENT2',))

        for tst in [('WIN1', 'Win2008 Server 1', 'SFTPPlus', '192.168.0.65', '',
                     '', '', '', 'xfero', 'xferopassword', '', '', '10021', '', '',
                     'key1'),
                    ('WIN2', 'Win2008 Server 2', 'SFTPPlus', '192.168.0.66', '',
                     '', '', '', 'xfero', 'xferopassword', '', '', '10221', '', '',
                     'key2'),
                    ('CENT1', 'CentOS6 Server 1', 'SFTPPlus', '192.168.0.11',
                     '', '', '', '', 'xfero', 'xferopassword', '', '', '10121', '',
                     '', 'key3'),
                    ('CENT2', 'CentOS6 Server 2', 'SFTPPlus', '192.168.0.12',
                     '', '', '', '', 'xfero', 'xferopassword', '', '', '10321', '',
                     '', 'key4'),
                   ]:

            (partner_service_name, partner_service_description,
             partner_COTS_type, partner_remote_system_id, partner_code,
             partner_mode, partner_local_username, partner_local_password,
             partner_remote_user, partner_remote_password,
             partner_CA_certificate, partner_cert_bundle, partner_control_port,
             partner_IDF, partner_parm, partner_pub_key) = tst
            result = db_partner.create_XFERO_Partner(partner_service_name,
                                                  partner_service_description,
                                                  partner_COTS_type,
                                                  partner_remote_system_id,
                                                  partner_code, partner_mode,
                                                  partner_local_username,
                                                  partner_local_password,
                                                  partner_remote_user,
                                                  partner_remote_password,
                                                  partner_CA_certificate,
                                                  partner_cert_bundle,
                                                  partner_control_port,
                                                  partner_IDF, partner_parm,
                                                  partner_pub_key)

        rows = db_partner.list_service_name_XFERO_Partner()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
