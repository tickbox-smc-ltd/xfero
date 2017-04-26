#!/usr/bin/env python
''' Manage COTS Pttern'''
import unittest
import configparser
import os
import sqlite3 as lite
from /xfero/.db import manage_cots_pattern as db_cots_pattern
from /xfero/.db import create_XFERO_DB as db


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```crud_XFERO_COTS_Pattern```

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

    def test_create_XFERO_COTS_Pattern(self):
        '''

        **Purpose:**

        INSERT rows into the XFERO_COTS_Pattern table and confirm they have been
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

        for tst in [('Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                       parm={PARM_ID}, fname={Path_to_File_to_Send}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                       fname={Path_to_File_to_Send}, \
                       nfname={Remote_File_Name}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME_PARM',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('Boldon James Impart', 'XFERO_BJI_PATTERN',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_NO_TLS',
                     'curl -v -T {Path_to_File_to_Send} --user \
                      {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_WITH_TLS',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_IGNORE_TLS',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME1',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      fname={Path_to_File_to_Send}, nfname={Remote_File_Name}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME_PARM1',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('Boldon James Impart', 'XFERO_BJI_PATTERN1',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_NO_TLS1',
                     'curl -v -T {Path_to_File_to_Send} --user \
                      {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_WITH_TLS1',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_IGNORE_TLS1',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                   ]:

            (self.cotspattern_product, self.cotspattern_pattern_name,
             self.cotspattern_params) = tst

            result = db_cots_pattern.create_XFERO_COTS_Pattern(
                self.cotspattern_product, self.cotspattern_pattern_name,
                self.cotspattern_params)

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
            cur.execute('SELECT cotspattern_id FROM XFERO_COTS_Pattern')

        except lite.Error as err:
            print("Error %s:" % err.args[0])

        expected_tuple = ((1,), (2,), (3,), (4,), (5,), (6,),
                          (7,), (8,), (9,), (10,), (11,), (12,), (13,))

        rows = cur.fetchall()
        for row in rows:

            self.assertIn(row, expected_tuple, 'Unexpected row retrieved')

    def test_read_XFERO_COTS_Pattern(self):
        '''

        **Purpose:**

        SELECT a specified row from the XFERO_COTS_Pattern table with
        cotspattern_id = 1 and confirm that the rows returned are as expected

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      parm={PARM_ID}, fname={Path_to_File_to_Send}'),]:

            (self.cotspattern_product, self.cotspattern_pattern_name,
             self.cotspattern_params) = tst
            result = db_cots_pattern.create_XFERO_COTS_Pattern(
                self.cotspattern_product, self.cotspattern_pattern_name,
                self.cotspattern_params)

        # Perform the select
        self.cotspattern_id = '1'
        rows = db_cots_pattern.read_XFERO_COTS_Pattern(self.cotspattern_id)

        expected_tuple = (1, 'Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                          'cftutil send part={Send_to_Partner}, \
                          idf={IDF_Name}, parm={PARM_ID}, \
                          fname={Path_to_File_to_Send}')

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_read_cpn_XFERO_COTS_Pattern(self):
        '''

        **Purpose:**

        SELECT a specified row from the XFERO_COTS_Pattern table with
        cotspattern_id = 1 and confirm that the rows returned are as expected.
        This query will only return cots pattern name

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      parm={PARM_ID}, fname={Path_to_File_to_Send}'),]:

            (self.cotspattern_product, self.cotspattern_pattern_name,
             self.cotspattern_params) = tst
            result = db_cots_pattern.create_XFERO_COTS_Pattern(
                self.cotspattern_product, self.cotspattern_pattern_name,
                self.cotspattern_params)

        # Perform the select
        self.cotspattern_id = '1'
        rows = db_cots_pattern.read_cpn_XFERO_COTS_Pattern(self.cotspattern_id)

        expected_tuple = (
            'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
            parm={PARM_ID}, fname={Path_to_File_to_Send}',)

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_read_with_name_XFERO_COTS_Pattern(self):
        '''

        **Purpose:**

        SELECT a specified row from the XFERO_COTS_Pattern table using the COTS
        Pattern Name and confirm that the rows returned are as expected. This
        query will only return cots pattern name

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      parm={PARM_ID}, fname={Path_to_File_to_Send}'),]:

            (self.cotspattern_product, self.cotspattern_pattern_name,
             self.cotspattern_params) = tst
            result = db_cots_pattern.create_XFERO_COTS_Pattern(
                self.cotspattern_product, self.cotspattern_pattern_name,
                self.cotspattern_params)

        # Perform the select
        self.cotspattern_name = 'XFERO_CFT_PATTERN_WITH_PARM'
        rows = db_cots_pattern.read_with_name_XFERO_COTS_Pattern(
            self.cotspattern_name)

        expected_tuple = (1, 'Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                          'cftutil send part={Send_to_Partner}, \
                          idf={IDF_Name}, parm={PARM_ID}, \
                          fname={Path_to_File_to_Send}')

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_update_XFERO_COTS_Pattern(self):
        '''

        **Purpose:**

        UPDATE row on the XFERO_COTS_Pattern table with cotspattern_id = 1 and
        confirm that the update has been applied to the table.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        # Create the row in the database
        for tst in [('Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      parm={PARM_ID}, fname={Path_to_File_to_Send}'),]:

            (self.cotspattern_product, self.cotspattern_pattern_name,
             self.cotspattern_params) = tst
            result = db_cots_pattern.create_XFERO_COTS_Pattern(
                self.cotspattern_product, self.cotspattern_pattern_name,
                self.cotspattern_params)

        # Perform the select
        self.cotspattern_id = '1'
        self.cotspattern_product = 'FALCK_FTP'
        self.cotspattern_pattern_name = 'SEND_WITH_FALCK'
        self.cotspattern_params = 'falcksend={send_me}, id={xfer_id}'
        rows = db_cots_pattern.update_XFERO_COTS_Pattern(
            self.cotspattern_id, self.cotspattern_product,
            self.cotspattern_pattern_name, self.cotspattern_params)

        # Check update
        rows = db_cots_pattern.read_XFERO_COTS_Pattern(self.cotspattern_id)

        expected_tuple = (
            1, 'FALCK_FTP', 'SEND_WITH_FALCK', 'falcksend={send_me}, \
            id={xfer_id}')

        for row in rows:
            self.assertTupleEqual(
                expected_tuple, row, 'Unexpected row retrieved')

    def test_delete_XFERO_COTS_Pattern(self):
        '''

        **Purpose:**

        DELETE rows on the XFERO_COTS_Pattern table with cotspattern_id = 1 and
        confirm that the deletion has been successful.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+
        | 10/01/2014 | Chris Falck | Tested to confirm changes to DB           |
        +------------+-------------+-------------------------------------------+
        '''
        # Create the row in the database
        for tst in [('Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      parm={PARM_ID}, fname={Path_to_File_to_Send}'),]:

            (self.cotspattern_product, self.cotspattern_pattern_name,
             self.cotspattern_params) = tst
            result = db_cots_pattern.create_XFERO_COTS_Pattern(
                self.cotspattern_product, self.cotspattern_pattern_name,
                self.cotspattern_params)

        # Perform the select
        self.cotspattern_id = '1'
        rows = db_cots_pattern.delete_XFERO_COTS_Pattern(self.cotspattern_id)

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
            cur.execute('SELECT count(*) FROM XFERO_COTS_Pattern')

        except lite.Error as err:
            print("Error %s:" % err.args[0])

        data = cur.fetchone()[0]
        expected = 0
        self.assertEqual(expected == data, True, "Unexpected row selected")

    def test_list_XFERO_COTS_Pattern(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_COTS_Pattern table and confirm that all rows
        have been returned successfully.

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
        expected_tuple = ((1, 'Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                           'cftutil send part={Send_to_Partner}, \
                           idf={IDF_Name}, parm={PARM_ID}, \
                           fname={Path_to_File_to_Send}'),
                          (2, 'Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME',
                           'cftutil send part={Send_to_Partner}, \
                           idf={IDF_Name}, fname={Path_to_File_to_Send}, \
                           nfname={Remote_File_Name}'),
                          (3, 'Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME_PARM',
                           'cftutil send part={Send_to_Partner}, \
                           idf={IDF_Name}, {PARM_ID}, \
                           fname={Path_to_File_to_Send}, \
                           nfname={Remote_File_Name}'),
                          (4, 'Boldon James Impart', 'XFERO_BJI_PATTERN',
                           'cftutil send part={Send_to_Partner}, \
                           idf={IDF_Name}, {PARM_ID}, \
                           fname={Path_to_File_to_Send}, \
                           nfname={Remote_File_Name}'),
                          (5, 'SFTPPlus', 'XFERO_FTPS_PATTERN_NO_TLS',
                           'curl -v -T {Path_to_File_to_Send} --user \
                           {User}:{Password} \
                           ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                          (6, 'SFTPPlus', 'XFERO_FTPS_PATTERN_WITH_TLS',
                           'curl -v -T {Path_to_File_to_Send} --cacert \
                           {CA_Cert} -k --ftp-ssl --cert {Cert_Bundle} --user \
                           {User}:{Password} \
                           ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                          (7, 'SFTPPlus', 'XFERO_FTPS_PATTERN_IGNORE_TLS',
                           'curl -v -T {Path_to_File_to_Send} --cacert \
                           {CA_Cert} -k --ftp-ssl --cert {Cert_Bundle} --user \
                           {User}:{Password} \
                           ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                          (8, 'Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME1',
                           'cftutil send part={Send_to_Partner}, \
                           idf={IDF_Name}, fname={Path_to_File_to_Send}, \
                           nfname={Remote_File_Name}'),
                          (9, 'Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME_PARM1',
                           'cftutil send part={Send_to_Partner}, \
                           idf={IDF_Name}, {PARM_ID}, \
                           fname={Path_to_File_to_Send}, \
                           nfname={Remote_File_Name}'),
                          (10, 'Boldon James Impart', 'XFERO_BJI_PATTERN1',
                           'cftutil send part={Send_to_Partner}, \
                           idf={IDF_Name}, {PARM_ID}, \
                           fname={Path_to_File_to_Send}, \
                           nfname={Remote_File_Name}'),
                          (11, 'SFTPPlus', 'XFERO_FTPS_PATTERN_NO_TLS1',
                           'curl -v -T {Path_to_File_to_Send} --user \
                           {User}:{Password} \
                           ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                          (12, 'SFTPPlus', 'XFERO_FTPS_PATTERN_WITH_TLS1',
                           'curl -v -T {Path_to_File_to_Send} --cacert \
                           {CA_Cert} -k --ftp-ssl --cert {Cert_Bundle} --user \
                           {User}:{Password} \
                           ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                          (13, 'SFTPPlus', 'XFERO_FTPS_PATTERN_IGNORE_TLS1', \
                           'curl -v -T {Path_to_File_to_Send} --cacert \
                           {CA_Cert} -k --ftp-ssl --cert {Cert_Bundle} --user \
                           {User}:{Password} \
                           ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'))

        for tst in [('Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                     'cftutil send part={Send_to_Partner}, \
                      idf={IDF_Name}, parm={PARM_ID}, \
                      fname={Path_to_File_to_Send}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      fname={Path_to_File_to_Send}, nfname={Remote_File_Name}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME_PARM',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('Boldon James Impart', 'XFERO_BJI_PATTERN',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_NO_TLS',
                     'curl -v -T {Path_to_File_to_Send} --user \
                     {User}:{Password} \
                     ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_WITH_TLS',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_IGNORE_TLS',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME1',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      fname={Path_to_File_to_Send}, nfname={Remote_File_Name}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME_PARM1',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('Boldon James Impart', 'XFERO_BJI_PATTERN1',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_NO_TLS1',
                     'curl -v -T {Path_to_File_to_Send} --user \
                     {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_WITH_TLS1',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_IGNORE_TLS1',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                   ]:

            (self.cotspattern_product, self.cotspattern_pattern_name,
             self.cotspattern_params) = tst
            result = db_cots_pattern.create_XFERO_COTS_Pattern(
                self.cotspattern_product, self.cotspattern_pattern_name,
                self.cotspattern_params)

        rows = db_cots_pattern.list_XFERO_COTS_Pattern()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')

    def test_list_all_patterns_XFERO_COTS_Pattern(self):
        '''

        **Purpose:**

        SELECT ALL rows on the XFERO_COTS_Pattern table and confirm that all rows
        have been returned successfully. Only COTS Patterns will be returned

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
        expected_tuple = (('XFERO_CFT_PATTERN_WITH_PARM',),
                          ('XFERO_CFT_PATTERN_WITH_NFNAME',),
                          ('XFERO_CFT_PATTERN_WITH_NFNAME_PARM',),
                          ('XFERO_BJI_PATTERN',),
                          ('XFERO_FTPS_PATTERN_NO_TLS',),
                          ('XFERO_FTPS_PATTERN_WITH_TLS',),
                          ('XFERO_FTPS_PATTERN_IGNORE_TLS',),
                          ('XFERO_CFT_PATTERN_WITH_NFNAME1',),
                          ('XFERO_CFT_PATTERN_WITH_NFNAME_PARM1',),
                          ('XFERO_BJI_PATTERN1',),
                          ('XFERO_FTPS_PATTERN_NO_TLS1',),
                          ('XFERO_FTPS_PATTERN_WITH_TLS1',),
                          ('XFERO_FTPS_PATTERN_IGNORE_TLS1',))

        for tst in [('Axway CFT', 'XFERO_CFT_PATTERN_WITH_PARM',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      parm={PARM_ID}, fname={Path_to_File_to_Send}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      fname={Path_to_File_to_Send}, nfname={Remote_File_Name}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME_PARM',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('Boldon James Impart', 'XFERO_BJI_PATTERN',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_NO_TLS',
                     'curl -v -T {Path_to_File_to_Send} --user \
                     {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_WITH_TLS',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_IGNORE_TLS',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME1',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      fname={Path_to_File_to_Send}, nfname={Remote_File_Name}'),
                    ('Axway CFT', 'XFERO_CFT_PATTERN_WITH_NFNAME_PARM1',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('Boldon James Impart', 'XFERO_BJI_PATTERN1',
                     'cftutil send part={Send_to_Partner}, idf={IDF_Name}, \
                      {PARM_ID}, fname={Path_to_File_to_Send}, \
                      nfname={Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_NO_TLS1',
                     'curl -v -T {Path_to_File_to_Send} --user \
                     {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_WITH_TLS1',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                    ('SFTPPlus', 'XFERO_FTPS_PATTERN_IGNORE_TLS1',
                     'curl -v -T {Path_to_File_to_Send} --cacert {CA_Cert} -k \
                      --ftp-ssl --cert {Cert_Bundle} --user {User}:{Password} \
                      ftp://{Common_Name}:{FTP_Ctrl_Port}/{Remote_File_Name}'),
                   ]:

            (self.cotspattern_product, self.cotspattern_pattern_name,
             self.cotspattern_params) = tst
            result = db_cots_pattern.create_XFERO_COTS_Pattern(
                self.cotspattern_product, self.cotspattern_pattern_name,
                self.cotspattern_params)

        rows = db_cots_pattern.list_all_patterns_XFERO_COTS_Pattern()
        for row in rows:
            self.assertIn(row, expected_tuple, 'Unexpected row selected')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
