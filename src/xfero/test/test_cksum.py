#!/usr/bin/env python
'''Test CKSUM'''
import os
import unittest
import zipfile
import tarfile
import subprocess
import shutil
import /xfero/.workflow_manager.checksum as checksum


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```cksum```


    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/06/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+

    '''

    def setUp(self):
        '''

        **Purpose:**

        Set up Unit Test artifacts for the function ```cksum```

        *Notes:*

        A directory is created in during installation of XFERO under the install
        directory called ```test```. This directory contains a number of files
        whose checksums are known for the purposes of this test.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        # Create temporary directory and files to rename
        self.basedir = '/Users/chrisfalck/Documents/test-files/cksum_dir'
        self.created_files_list = []

        # Get CKSUM of them all
        self.cksum_pdf = subprocess.check_output(
            ["cksum", os.path.join(self.basedir, 'test_pdf.pdf')])
        self.cksum_xls = subprocess.check_output(
            ["cksum", os.path.join(self.basedir, 'test_xls.xlsx')])
        self.cksum_doc = subprocess.check_output(
            ["cksum", os.path.join(self.basedir, 'test_doc.docx')])

        self.origdir = os.getcwd()
        self.dirname = self.basedir + os.sep + 'workingdir'
        os.makedirs(self.dirname)

        os.chdir(self.dirname)  # This is sourcedir
        for filename in ("file_name.txt", "long_file_name.txt",
                         "an_even_longer_file_name.txt"):
            f = open(filename, "w")
            f.write("Just a test file\n")
            f.close()

        os.chdir(self.origdir)

    def tearDown(self):
        '''

        **Purpose:**

        Tear down Unit Test artifacts created in setup() for the function
        ```cksum```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        shutil.rmtree(self.dirname)

    def test_cksum_pdf(self):
        '''

        **Purpose:**

        Uses the ```cksum``` function to return the sum of the file tested and
        a zip archive containing the original file and a sum file which details
        the checksum of the file.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```cksum```
        with the expected result

        self.assertEqual(new_cksum, self.cksum_pdf, 'Invalid CKSUM')```

        Performs an ```assertEqual``` on the path to where the archive is
        created to ensure the file exists on the file system with the correct
        file name:

        ```self.assertEqual(os.path.exists(archive) == 1, True, "Archive File
        not on OS")```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        file_name = self.basedir + os.sep + 'test_pdf.pdf'
        args = (file_name, '.zip', '/ftran')

        csum = checksum.Checksum()
        archive = csum.cksum(*args)

        tz = zipfile.ZipFile(archive, "r")
        entities_in_archive = tz.namelist()
        tz.close()

        observed = set(f for f in entities_in_archive)
        expected = {'test_pdf.pdf', 'test_pdf.pdf.sum'}
        self.assertEqual(observed, expected)

    def test_cksum_doc(self):
        '''

        **Purpose:**

        Uses the ```cksum``` function to return the sum of the file tested and
        a zip archive containing the original file and a sum file which details
        the checksum of the file.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```cksum```
        with the expected result

        self.assertEqual(new_cksum, self.cksum_doc, 'Invalid CKSUM')```

        Performs an ```assertEqual``` on the path to where the archive is
        created to ensure the file exists on the file system with the correct
        file name:

        ```self.assertEqual(os.path.exists(archive) == 1, True, "Archive File
        not on OS")```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        file_name = self.basedir + os.sep + 'test_doc.docx'
        args = (file_name, '.zip', '/ftran')

        csum = checksum.Checksum()
        archive = csum.cksum(*args)

        tz = zipfile.ZipFile(archive, "r")
        entities_in_archive = tz.namelist()
        tz.close()

        observed = set(f for f in entities_in_archive)
        expected = {'test_doc.docx', 'test_doc.docx.sum'}
        self.assertEqual(observed, expected)

    def test_cksum_xls(self):
        '''

        **Purpose:**

        Uses the ```cksum``` function to return the sum of the file tested and
        a tar.gz archive containing the original file and a sum file which
        details the checksum of the file.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```cksum```
        with the expected result

        self.assertEqual(new_cksum, self.cksum_xls, 'Invalid CKSUM')```

        Performs an ```assertEqual``` on the path to where the archive is
        created to ensure the file exists on the file system with the correct
        file name:

        ```self.assertEqual(os.path.exists(archive) == 1, True, "Archive File
        not on OS")```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        file_name = self.basedir + os.sep + 'test_xls.xlsx'
        args = (file_name, '.tar.gz', '/ftran')

        csum = checksum.Checksum()
        archive = csum.cksum(*args)

        tt = tarfile.open(archive, "r")
        entities_in_archive = tt.getnames()
        tt.close()

        observed = set(f for f in entities_in_archive)
        expected = {'test_xls.xlsx', 'test_xls.xlsx.sum'}
        self.assertEqual(observed, expected)

    def test_cksum_file_to_sum_does_not_exist(self):
        '''

        **Purpose:**

        Test error trapping of the ```cksum``` function by attempting to
        generate a sum for a file called ```filedoesnotexist``` that does not
        exist on the file system.

        *Test Confirmation*

        The following assertions are performed:

        ```self.assertEqual(err.args, (2, 'No such file or directory'), 'Invalid
        test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        file_name = self.basedir + os.sep + 'filedoesnotexist.tar'
        args = (file_name, 'zip', '/ftran')
        try:
            csum = checksum.Checksum()
            archive = csum.cksum(*args)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')

    def test_cksum_file_invalid_archive_type(self):
        '''

        **Purpose:**

        Test error trapping of the ```cksum``` function by attempting to request
        an invalid archive type. The archive type ```zipper``` is passed to the
        function and the function expects either ```zip``` or ```tar.gz```.

        *Test Confirmation*

        The following assertions are performed:

        ```self.assertEqual(err.args, (1, 'Invalid Archive Type. Should be .zip
        or .tar.gz'))```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        file_name = self.basedir + os.sep + 'test_tar.tar'
        args = (file_name, '.zipper', '/ftran')
        try:
            csum = checksum.Checksum()
            archive = csum.cksum(*args)
        except TypeError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (1, 'Invalid Archive Type. \
                Should be .zip or .tar.gz'))

    def test_cksum_zipfile(self):
        file_name = self.basedir + os.sep + 'Archive.zip'
        args = (file_name, '.zip', '/ftran/zip_extract')

        csum = checksum.Checksum()
        archive = csum.cksum(*args)

        tz = zipfile.ZipFile(archive, "r")
        entities_in_archive = tz.namelist()
        tz.close()

        observed = set(f for f in entities_in_archive)
        expected = {
            'test_doc.docx', 'test_pdf.pdf', 'test_xls.xlsx', 'sumfile.sum'}
        self.assertEqual(observed, expected)

    def test_cksum_tarfile(self):

        file_name = self.basedir + os.sep + 'test_tar.tar.gz'
        args = (file_name, '.tar.gz', '/ftran/tar_extract')

        csum = checksum.Checksum()
        archive = csum.cksum(*args)

        tt = tarfile.open(archive, "r")
        entities_in_archive = tt.getnames()
        tt.close()

        observed = set(f for f in entities_in_archive)
        expected = {
            'test_doc.docx', 'test_pdf.pdf', 'test_xls.xlsx', 'sumfile.sum'}
        self.assertEqual(observed, expected)

    def test_cksum_dir_no_arc_name(self):

        args = (self.dirname, '.zip', '', '')

        csum = checksum.Checksum()
        archive = csum.cksum(*args)

        tz = zipfile.ZipFile(archive, "r")
        entities_in_archive = tz.namelist()
        tz.close()

        observed = set(f for f in entities_in_archive)
        expected = {"file_name.txt", "long_file_name.txt",
                    "an_even_longer_file_name.txt", 'sumfile.sum'}
        self.assertEqual(observed, expected)

    def test_cksum_dir_with_arc_name(self):

        args = (self.dirname, '.zip', '/ftran', 'poop')

        csum = checksum.Checksum()
        archive = csum.cksum(*args)

        tz = zipfile.ZipFile(archive, "r")
        entities_in_archive = tz.namelist()
        tz.close()

        observed = set(f for f in entities_in_archive)
        expected = {"file_name.txt", "long_file_name.txt",
                    "an_even_longer_file_name.txt", 'sumfile.sum'}
        self.assertEqual(observed, expected)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_cksum']
    unittest.main()
