#!/usr/bin/env python
'''Test HK'''
import unittest
import os
from /xfero/.hk.hk import HK


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```delete_old_files```

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/06/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+

    '''

    def setUp(self):
        '''

        **Purpose:**

        Set up Unit Test artifacts for the function ```delete_old_files```

        *Preparation:*

        Since it is necessary to have files of a specified age to test this
        module, It is necessary to manually create the structure and modify the
        modification time on specific files.

        Use touch to amend dates of files -
        ```touch -acmd 'July 10 2013 09:00:00' delete*```

        Manually create the following:

        * Directory /path/to/tmp/sub/sub
        * Create multiple new files in the each of the directories tmp, tmp/sub,
        tmp/sub/sub using these commands
          * touch Hellhathnofury.x1234560000044444 CHRISFALCK0000
          ForGodsSake.A12345678900000
          KEVIN234 BOBCDF00000000Z000ABC123
          CHRIS0000131OCT-13.csv
          * touch ForGodsSake.Z12345678999777 KEVIN222777
          WWWCDF11111111Z99999999999999999 CHRIS1234513MAR-11.csv
          Hellhathnofury.x1234569777999999 CHRISFALCK9876
          * touch sub/Hellhathnofury.x1234560000044444 sub/CHRISFALCK0000
          sub/ForGodsSake.A12345678900000 sub/KEVIN234
          sub/BOBCDF00000000Z000ABC123 sub/CHRIS0000131OCT-13.csv
          * touch sub/ForGodsSake.Z12345678999777 sub/KEVIN222777
          sub/WWWCDF11111111Z99999999999999999 sub/CHRIS1234513MAR-11.csv
          sub/Hellhathnofury.x1234569777999999 sub/CHRISFALCK9876
          * touch sub/sub/Hellhathnofury.x1234560000044444
          sub/sub/CHRISFALCK0000 sub/sub/ForGodsSake.A12345678900000
          sub/sub/KEVIN234 sub/sub/BOBCDF00000000Z000ABC123
          sub/sub/CHRIS0000131OCT-13.csv
          * touch sub/sub/ForGodsSake.Z12345678999777 sub/sub/KEVIN222777
          sub/sub/WWWCDF11111111Z99999999999999999
          sub/sub/CHRIS1234513MAR-11.csv
          sub/sub/Hellhathnofury.x1234569777999999 sub/sub/CHRISFALCK9876
        * Create specific files for the tests to match the following patterns in
        each of the directories tmp, tmp/sub, tmp/sub/sub:
        * run the command ```touch -acmd 'January 10 2000 09:00:00'
        sub/ sub/sub/``` to set the directory age to be older than all files it
        contains. This ensures that the function will traverse into the
        directories looking for files to delete.

        *Sample Patterns for pattern matching:*

        * ^\w{14}\.x123456\d{10}$
        * ^CHRISFALCK[0-9]{4}$
        * ^\w{11}\.Z123456789\d{5}$
        * ^KEVIN.*
        * ^\w{3}CDF\d{8}[AZ]\d{3}.*
        * ^CHRIS((0000[0-9])|12345|1234[0-9]|33333)([a-z]{2})([a-z]{3})-([a-z]
        {2})\.csv

        *Sample File Names with the Pattern that it will be matched by:*

        * Hellhathnofury.x1234560000000000 match = ^\w{14}\.x123456\d{10}$
        * Hellhathnofury.x1234569999999999 match = ^\w{14}\.x123456\d{10}$
        * Hellhathnofury.x1234567777777777 match = ^\w{14}\.x123456\d{10}$
        * CHRISFALCK1234 match = ^CHRISFALCK[0-9]{4}$
        * CHRISFALCK9999 match = ^CHRISFALCK[0-9]{4}$
        * CHRISFALCK7777 match = ^CHRISFALCK[0-9]{4}$
        * ForGodsSake.Z12345678900000 match = ^\w{11}\.Z123456789\d{5}$
        * ForGodsSake.Z12345678999999 match = ^\w{11}\.Z123456789\d{5}$
        * ForGodsSake.Z12345678977777 match = ^\w{11}\.Z123456789\d{5}$
        * KEVIN123 match = ^KEVIN.*
        * KEVIN222222 match = ^KEVIN.*
        * KEVINABCDEFG match = ^KEVIN.*
        * BOBCDF00000000A000ABC123 match = ^\w{3}CDF\d{8}[AZ]\d{3}.*
        * JIMCDF11111111Z99999999999999999 match = ^\w{3}CDF\d{8}[AZ]\d{3}.*
        * TIMCDF11111111Z99999999999999999 match = ^\w{3}CDF\d{8}[AZ]\d{3}.*
        * CHRIS0000101JAN-13.csv match = ^CHRIS((0000[0-9])|12345|1234[0-9]|
        33333)([a-z]{2})([a-z]{3})-([a-z]{2})\.csv
        * CHRIS1234530DEC-13.csv match = ^CHRIS((0000[0-9])|12345|1234[0-9]|
        33333)([a-z]{2})([a-z]{3})-([a-z]{2})\.csv
        * CHRIS1234920JUL-13.csv match = ^CHRIS((0000[0-9])|12345|1234[0-9]|
        33333)([a-z]{2})([a-z]{3})-([a-z]{2})\.csv

        The files above are grouped to be matched by a specific format. One of
        each file should have its file modification date set as follows:

        * > 50 days
        * > 25 < 50 days
        * < 25 days

          * touch -amt 201306010900 Hellhathnofury.x1234560000000000
          CHRISFALCK1234 ForGodsSake.Z12345678900000 KEVIN123
          BOBCDF00000000A000ABC123 CHRIS0000131JAN-13.csv
          * touch -amt 201307210900 ForGodsSake.Z12345678999999
          KEVIN222222 JIMCDF11111111Z99999999999999999 CHRIS1234513MAR-12.csv
          Hellhathnofury.x1234569999999999 CHRISFALCK9999
          * touch -amt 201306010900 sub/Hellhathnofury.x1234560000000000
          sub/CHRISFALCK1234 sub/ForGodsSake.Z12345678900000 sub/KEVIN123
          sub/BOBCDF00000000A000ABC123 sub/CHRIS0000112JUL-13.csv
          * touch -amt 201307210900 sub/ForGodsSake.Z12345678999999
          sub/KEVIN222222 sub/JIMCDF11111111Z99999999999999999
          sub/CHRIS1234511DEC-12.csv sub/Hellhathnofury.x1234569999999999
          sub/CHRISFALCK9999
          * touch -amt 201306010900 sub/sub/Hellhathnofury.x1234560000000000
          sub/sub/CHRISFALCK1234 sub/sub/ForGodsSake.Z12345678900000
          sub/sub/KEVIN123 sub/sub/BOBCDF00000000A000ABC123
          sub/sub/CHRIS0000125DEC-12.csv
          * touch -amt 201307210900 sub/sub/ForGodsSake.Z12345678999999
          sub/sub/KEVIN222222 sub/sub/JIMCDF11111111Z99999999999999999
          sub/sub/CHRIS1234503SEP-12.csv
          sub/sub/Hellhathnofury.x1234569999999999 sub/sub/CHRISFALCK9999

        Use the command ```touch -acmd 'July 10 2013 09:00:00' $FILENAME```
        Where $FILENAME = file name and date specified provides the correct age
        of the file


        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        pass

    def tearDown(self):
        '''

        **Purpose:**

        Tear down Unit Test artifacts created in setup() for the function
        ```delete_old_files```

        *Currently, no teardown() is performed for this function.*

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        pass

    def test_HK_delete_files_age_50(self):
        '''

        **Purpose:**

        Uses the ```delete_old_files``` function to delete files above a 50 days
        old that match a specified filename pattern.

        *Test Confirmation*

        The following assertions are performed:

        Because we are dealing with deleted files, the easiest way to confirm
        that the test has been successful is to check to see if the expected
        file deletion has taken place. So, the assertion we do is on whether the
        file still exists on the file system.

        Performs an ```assertEqual``` on the result of the call to
        ```os.path.isfile`` which should return ```False``` since will no longer
        exist on the system.

        The following filepatterns are tested:

        fn_pattern = '^\w{14}\.x123456\d{10}$'

        * result = os.path.isfile('/tmp/test/Hellhathnofury.x1234560000000000')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^CHRISFALCK[0-9]{4}$'

        * result = os.path.isfile('/tmp/test/Hellhathnofury.x1234560000000000')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^\w{11}\.Z123456789\d{5}$'

        * result = os.path.isfile('/tmp/test/ForGodsSake.Z12345678900000')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^KEVIN.*'

        * result = os.path.isfile('/tmp/test/KEVIN123')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^\w{3}CDF\d{8}[AZ]\d{3}.*'

        * result = os.path.isfile('/tmp/test/BOBCDF00000000A000ABC123')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^CHRIS((0000[0-9])|12345|1234[0-9]|33333)([0-9]{2})
        ([A-Z]{3})-([0-9]{2})\.csv'

        * result = os.path.isfile('/tmp/test/CHRIS0000131JAN-13.csv')
        * self.assertEqual(False,result,"File(s) not removed")```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        purge_dir = '/tmp/test'
        num_days = 50
        subdir = False

        fn_pattern = '^\w{14}\.x123456\d{10}$'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/Hellhathnofury.x1234560000000000')
        self.assertEqual(False, result, "File(s) not removed")

        fn_pattern = '^CHRISFALCK[0-9]{4}$'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/CHRISFALCK1234')
        self.assertEqual(False, result, "File(s) not removed")

        fn_pattern = '^\w{11}\.Z123456789\d{5}$'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/ForGodsSake.Z12345678900000')
        self.assertEqual(False, result, "File(s) not removed")

        fn_pattern = '^KEVIN.*'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/KEVIN123')
        self.assertEqual(False, result, "File(s) not removed")

        # BOBCDF00000000A000ABC123
        fn_pattern = '^\w{3}CDF\d{8}[AZ]\d{3}.*'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/BOBCDF00000000A000ABC123')
        self.assertEqual(False, result, "File(s) not removed")

        # CHRIS0000131JAN-13.csv
        fn_pattern = '^CHRIS((0000[0-9])|12345|1234[0-9]|33333)([0-9]{2})([A-Z]{3})-([0-9]{2})\.csv'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/CHRIS0000131JAN-13.csv')
        self.assertEqual(False, result, "File(s) not removed")

    def test_HK_delete_files_age_25(self):
        '''

        **Purpose:**

        Uses the ```delete_old_files``` function to delete files above a 25 days
        old that match a specified filename pattern.

        *Test Confirmation*

        The following assertions are performed:

        Because we are dealing with deleted files, the easiest way to confirm
        that the test has been successful is to check to see if the expected
        file deletion has taken place. So, the assertion we do is on whether the
        file still exists on the file system.

        Performs an ```assertEqual``` on the result of the call to
        ```os.path.isfile`` which should return ```False``` since will no longer
        exist on the system.

        The following filepatterns are tested:

        fn_pattern = '^\w{14}\.x123456\d{10}$'

        * result = os.path.isfile('/tmp/test/Hellhathnofury.x1234569999999999')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^CHRISFALCK[0-9]{4}$'

        * result = os.path.isfile('/tmp/test/CHRISFALCK9999')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^\w{11}\.Z123456789\d{5}$'

        * result = os.path.isfile('/tmp/test/ForGodsSake.Z12345678999999')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^KEVIN.*'

        * result = os.path.isfile('/tmp/test/KEVIN222222')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^\w{3}CDF\d{8}[AZ]\d{3}.*'

        * result = os.path.isfile('/tmp/test/JIMCDF11111111Z99999999999999999')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^CHRIS((0000[0-9])|12345|1234[0-9]|33333)([0-9]{2})
        ([A-Z]{3})-([0-9]{2})\.csv'

        * result = os.path.isfile('/tmp/test/CHRIS1234513MAR-12.csv')
        * self.assertEqual(False,result,"File(s) not removed")

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        purge_dir = '/tmp/test'
        num_days = 25
        subdir = False
        fn_pattern = '^\w{14}\.x123456\d{10}$'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/Hellhathnofury.x1234569999999999')
        self.assertEqual(False, result, "File(s) not removed")

        fn_pattern = '^CHRISFALCK[0-9]{4}$'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/CHRISFALCK9999')
        self.assertEqual(False, result, "File(s) not removed")

        fn_pattern = '^\w{11}\.Z123456789\d{5}$'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/ForGodsSake.Z12345678999999')
        self.assertEqual(False, result, "File(s) not removed")

        fn_pattern = '^KEVIN.*'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/KEVIN222222')
        self.assertEqual(False, result, "File(s) not removed")

        # BOBCDF00000000A000ABC123
        fn_pattern = '^\w{3}CDF\d{8}[AZ]\d{3}.*'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/JIMCDF11111111Z99999999999999999')
        self.assertEqual(False, result, "File(s) not removed")

        # CHRIS0000131JAN-13.csv
        fn_pattern = '^CHRIS((0000[0-9])|12345|1234[0-9]|33333)([0-9]{2})([A-Z]{3})-([0-9]{2})\.csv'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/CHRIS1234513MAR-12.csv')
        self.assertEqual(False, result, "File(s) not removed")

    def test_HK_delete_files_age_25_with_subdir(self):
        '''

        **Purpose:**

        Uses the ```delete_old_files``` function to delete files above a 25 days
        old that match a specified filename pattern and instruct the function to
        purge fromsubdirectories.

        *Test Confirmation*

        The following assertions are performed:

        Because we are dealing with deleted files, the easiest way to confirm
        that the test has been successful is to check to see if the expected
        file deletion has taken place. So, the assertion we do is on whether the
        file still exists on the file system.

        Performs an ```assertEqual``` on the result of the call to
        ```os.path.isfile`` which should return ```False``` since will no longer
        exist on the system.

        The following filepatterns are tested:

        fn_pattern = '^\w{14}\.x123456\d{10}$'

        * result = os.path.isfile('/tmp/test/sub/Hellhathnofury.
        x1234560000000000')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/Hellhathnofury.
        x1234569999999999')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/Hellhathnofury.
        x1234560000000000')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/Hellhathnofury.
        x1234569999999999')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^CHRISFALCK[0-9]{4}$'

        * result = delete_old_files(purge_dir, fn_pattern, num_days, subdir)
        * result = os.path.isfile('/tmp/test/sub/CHRISFALCK1234')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/CHRISFALCK9999')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/CHRISFALCK1234')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/CHRISFALCK9999')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^\w{11}\.Z123456789\d{5}$'

        * result = os.path.isfile('/tmp/test/sub/ForGodsSake.Z12345678900000')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/ForGodsSake.Z12345678999999')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/ForGodsSake.
        Z12345678900000')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/ForGodsSake.
        Z12345678999999')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^KEVIN.*'

        * result = os.path.isfile('/tmp/test/sub/KEVIN123')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/KEVIN222222')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/KEVIN123')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/KEVIN222222')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^\w{3}CDF\d{8}[AZ]\d{3}.*'

        * result = os.path.isfile('/tmp/test/sub/BOBCDF00000000A000ABC123')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/
        JIMCDF11111111Z99999999999999999')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/BOBCDF00000000A000ABC123')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/
        JIMCDF11111111Z99999999999999999')
        * self.assertEqual(False,result,"File(s) not removed")

        fn_pattern = '^CHRIS((0000[0-9])|12345|1234[0-9]|33333)([0-9]{2})
        ([A-Z]{3})-([0-9]{2})\.csv'

        * result = os.path.isfile('/tmp/test/sub/CHRIS0000112JUL-13.csv')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/CHRIS1234511DEC-12.csv')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/CHRIS0000125DEC-12.csv')
        * self.assertEqual(False,result,"File(s) not removed")
        * result = os.path.isfile('/tmp/test/sub/sub/CHRIS1234503SEP-12.csv')
        * self.assertEqual(False,result,"File(s) not removed")

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        purge_dir = '/tmp/test'
        num_days = 25
        subdir = True

        fn_pattern = '^\w{14}\.x123456\d{10}$'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile(
            '/tmp/test/sub/Hellhathnofury.x1234560000000000')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile(
            '/tmp/test/sub/Hellhathnofury.x1234569999999999')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile(
            '/tmp/test/sub/sub/Hellhathnofury.x1234560000000000')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile(
            '/tmp/test/sub/sub/Hellhathnofury.x1234569999999999')
        self.assertEqual(False, result, "File(s) not removed")

        fn_pattern = '^CHRISFALCK[0-9]{4}$'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/sub/CHRISFALCK1234')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/CHRISFALCK9999')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/sub/CHRISFALCK1234')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/sub/CHRISFALCK9999')
        self.assertEqual(False, result, "File(s) not removed")

        fn_pattern = '^\w{11}\.Z123456789\d{5}$'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/sub/ForGodsSake.Z12345678900000')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/ForGodsSake.Z12345678999999')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile(
            '/tmp/test/sub/sub/ForGodsSake.Z12345678900000')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile(
            '/tmp/test/sub/sub/ForGodsSake.Z12345678999999')
        self.assertEqual(False, result, "File(s) not removed")

        fn_pattern = '^KEVIN.*'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/sub/KEVIN123')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/KEVIN222222')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/sub/KEVIN123')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/sub/KEVIN222222')
        self.assertEqual(False, result, "File(s) not removed")

        # BOBCDF00000000A000ABC123
        fn_pattern = '^\w{3}CDF\d{8}[AZ]\d{3}.*'
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, subdir)

        result = os.path.isfile('/tmp/test/sub/BOBCDF00000000A000ABC123')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile(
            '/tmp/test/sub/JIMCDF11111111Z99999999999999999')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/sub/BOBCDF00000000A000ABC123')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile(
            '/tmp/test/sub/sub/JIMCDF11111111Z99999999999999999')
        self.assertEqual(False, result, "File(s) not removed")

        # CHRIS0000131JAN-13.csv
        fn_pattern = '^CHRIS((0000[0-9])|12345|1234[0-9]|33333)([0-9]{2})([A-Z]{3})-([0-9]{2})\.csv'
        subdir = False
        obj = HK()
        result = obj.delete_old_file(purge_dir, fn_pattern, num_days, True)

        result = os.path.isfile('/tmp/test/sub/CHRIS0000112JUL-13.csv')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/CHRIS1234511DEC-12.csv')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/sub/CHRIS0000125DEC-12.csv')
        self.assertEqual(False, result, "File(s) not removed")
        result = os.path.isfile('/tmp/test/sub/sub/CHRIS1234503SEP-12.csv')
        self.assertEqual(False, result, "File(s) not removed")

    def test_HK_invalid_purge_dir(self):
        '''

        **Purpose:**

        Test error trapping of the ```delete_old_files``` function by performing
        housekeeping on a directory that does not exist

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertRaises``` on the result of the call to
        ```delete_old_files``` with the expected result specified for the
        TypeError which is returned:

        ```self.assertRaises(TypeError, delete_old_files(purge_dir, fn_pattern,
        num_days, subdir), "Bad directory")```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        purge_dir = '/tmp/does_not_exist'
        num_days = 25
        subdir = True

        fn_pattern = '^\w{14}\.x123456\d{10}$'
        obj = HK()
        self.assertRaises(TypeError, obj.delete_old_file(
            purge_dir, fn_pattern, num_days, subdir), "Bad directory")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
