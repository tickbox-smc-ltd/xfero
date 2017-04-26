#!/usr/bin/env python
'''Test Manage Archives'''
import unittest
import os
import zipfile
import tarfile
import /xfero/.workflow_manager.manage_archives as archive

class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the class ```manage_archives```


    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/06/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+

    '''

    def setUp(self):
        '''

        **Purpose:**

        Set up Unit Test artifacts for the function ```compress_file```

        *Create:*

        * Create a test_files directory
        * Create test files within the directory

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        self.path = r"/tmp/Compress_Files/"
        os.mkdir(self.path)
        self.file_names = ["file1.txt", "file2.xml", "file2.xml.sum"]
        for fname in self.file_names:
            fhandle = open(os.path.join(self.path, fname), "w")
            fhandle.close()

        self.path1 = r"/tmp/Compress_Files1/"
        os.mkdir(self.path1)
        self.file_names1 = ["file1.txt", "file2.xml", "file2.xml.sum"]
        for fn1 in self.file_names1:
            fhandle1 = open(os.path.join(self.path1, fn1), "w")
            fhandle1.close()

        args = (self.path1, '.zip', '/tmp/test-archive1')
        obj = archive.Manage_Archives('test')
        self.zipfile = obj.compress_dir(*args)

        self.path2 = r"/tmp/Compress_Files2/"
        os.mkdir(self.path2)
        self.file_names2 = ["file1.txt", "file2.xml", "file2.xml.sum"]
        for fn2 in self.file_names2:
            fhandle2 = open(os.path.join(self.path2, fn2), "w")
            fhandle2.close()

        args = (self.path2, '.tar.gz', '/tmp/test-archive2')
        obj = archive.Manage_Archives('test')
        self.tarfile = obj.compress_dir(*args)

    def tearDown(self):
        '''

        Tear down Unit Test artifacts created in setup() for the function
        ```compress_file```

        *Removes*

        Directory tree created in setup function

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        if os.path.exists(self.path):
            for fname in os.listdir(self.path):
                os.remove(self.path + fname)

            os.rmdir(self.path)

        if os.path.exists(self.path1):
            for fn1 in os.listdir(self.path1):
                os.remove(self.path1 + fn1)

            os.rmdir(self.path1)

        if os.path.exists(self.path2):
            for fn2 in os.listdir(self.path2):
                os.remove(self.path2 + fn2)

            os.rmdir(self.path2)

    def test_zip_file_no_sumfile(self):
        '''

        **Purpose:**

        Uses the ```compress_file``` function to create a zip of the file
        called ```file1.txt```. No checksum file is included.

        *Test Confirmation*

        The function returns a reference to the archive file created. This is
        interrogated to produce a list of entities that exist in the archive.

        The following assertions are performed on each of the entities in the
        archive to confirm that the contents of the archive match the expected
        result:

        Performs an ```assertEqual``` on the result of the call to
        ```compress_entities``` with the expected result:

        ```observed = set(f for f in entities_in_archive)```

        ```expected = {'file1.txt'}```

        ```self.assertEqual(observed, expected)```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        test_file = os.path.join(self.path, "file1.txt")
        args = (test_file, '.zip')

        obj = archive.Manage_Archives('test')
        zipf = obj.compress_file(*args)

        tzip = zipfile.ZipFile(zipf, "r")
        entities_in_archive = tzip.namelist()
        tzip.close()

        observed = set(f for f in entities_in_archive)
        expected = {'file1.txt'}
        self.assertEqual(observed, expected)

    def test_zip_file_with_sumfile(self):
        '''

        **Purpose:**

        Uses the ```compress_file``` function to create a zip of the file
        called ```file2.xml``` together with a checksum file created as part
        of the function.

        *Test Confirmation*

        The function returns a reference to the archive file created. This is
        interrogated to produce a list of entities that exist in the archive.

        The following assertions are performed on each of the entities in the
        archive to confirm that the contents of the archive match the expected
        result:

        Performs an ```assertEqual``` on the result of the call to
        ```compress_entities``` with the expected result:

        ```observed = set(f for f in entities_in_archive)```

        ```expected = {'file2.xml', 'file2.xml.sum'}```

        ```self.assertEqual(observed, expected)```

        Test creation of a zip archive containing one file with a sum file

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        test_file = os.path.join(self.path, "file2.xml")
        args = (test_file, '.zip')

        obj = archive.Manage_Archives('test')
        zipf = obj.compress_file(*args)

        tzip = zipfile.ZipFile(zipf, "r")
        entities_in_archive = tzip.namelist()
        tzip.close()
        # for f in entities_in_archive:
        #    print(f)
        observed = set(f for f in entities_in_archive)
        expected = {'file2.xml', 'file2.xml.sum'}
        self.assertEqual(observed, expected)

    def test_tar_file_no_sumfile(self):
        '''

        **Purpose:**

        Uses the ```compress_file``` function to create a tar.gz of the file
        called ```file1.txt```. No checksum file is included.

        *Test Confirmation*

        The function returns a reference to the archive file created. This is
        interrogated to produce a list of entities that exist in the archive.

        The following assertions are performed on each of the entities in the
        archive to confirm that the contents of the archive match the expected
        result:

        Performs an ```assertEqual``` on the result of the call to
        ```compress_entities``` with the expected result:

        ```observed = set(f for f in entities_in_archive)```

        ```expected = {'file1.txt'}```

        ```self.assertEqual(observed, expected)```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        test_file = os.path.join(self.path, "file1.txt")
        args = (test_file, '.tar.gz')

        obj = archive.Manage_Archives('test')
        tarf = obj.compress_file(*args)

        ttar = tarfile.open(tarf, "r")
        entities_in_archive = ttar.getnames()
        ttar.close()
        # for f in entities_in_archive:
        #    print(f)
        observed = set(f for f in entities_in_archive)
        expected = {'file1.txt'}
        self.assertEqual(observed, expected)

    def test_tar_file_with_sumfile(self):
        '''

        **Purpose:**

        Uses the ```compress_file``` function to create a tar.gz of the file
        called ```file2.xml``` together with a checksum file created as part
        of the function.

        *Test Confirmation*

        The function returns a reference to the archive file created. This is
        interrogated to produce a list of entities that exist in the archive.

        The following assertions are performed on each of the entities in the
        archive to confirm that the contents of the archive match the expected
        result:

        Performs an ```assertEqual``` on the result of the call to
        ```compress_entities``` with the expected result:

        ```observed = set(f for f in entities_in_archive)```

        ```expected = {'file2.xml', 'file2.xml.sum'}```

        ```self.assertEqual(observed, expected)```

        Test creation of a zip archive containing one file with a sum file

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        test_file = os.path.join(self.path, "file2.xml")
        args = (test_file, '.tar.gz')

        obj = archive.Manage_Archives('test')
        tarf = obj.compress_file(*args)

        ttar = tarfile.open(tarf, "r")
        entities_in_archive = ttar.getnames()
        ttar.close()
        # for f in entities_in_archive:
        #    print(f)
        observed = set(f for f in entities_in_archive)
        expected = {'file2.xml', 'file2.xml.sum'}
        self.assertEqual(observed, expected)

    def test_invalid_archive(self):
        '''

        **Purpose:**

        Test error trapping of the ```compress_file``` function by attempting to
        request an invalid archive type. The archive type ```zipper``` is passed
        to the function and the function expects either ```zip``` or
        ```tar.gz```.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```compress_file``` with the expected result specified for the TypeError
        which is returned:

        ```self.assertEqual(err.args, (1, 'Invalid Archive Type supplied:
        .zipper'), 'Invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        test_file = os.path.join(self.path, "file1.txt")
        args = (test_file, '.zipper')

        try:
            obj = archive.Manage_Archives('test')
            zipf = obj.compress_file(*args)
        except TypeError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (1, 'Invalid Archive Type supplied: .zipper'),
                'Invalid test result')

    def test_zip_dir(self):
        '''zip dir'''
        args = (self.path, '.zip', '/tmp/test-archive')
        obj = archive.Manage_Archives('test')
        zipf = obj.compress_dir(*args)

        tzip = zipfile.ZipFile(zipf, "r")
        entities_in_archive = tzip.namelist()
        tzip.close()
        # for f in entities_in_archive:
        #    print(f)
        observed = set(f for f in entities_in_archive)
        expected = {"file1.txt", "file2.xml", "file2.xml.sum"}
        self.assertEqual(observed, expected)

    def test_tar_dir(self):
        '''tar dir'''
        args = (self.path, '.tar.gz', '/tmp/test-archive')
        obj = archive.Manage_Archives('test')
        tarf = obj.compress_dir(*args)

        ttar = tarfile.open(tarf, "r")
        entities_in_archive = ttar.getnames()
        ttar.close()

        observed = set(f for f in entities_in_archive)
        expected = {"file1.txt", "file2.xml", "file2.xml.sum"}
        self.assertEqual(observed, expected)

    def test_extract_zip(self):
        '''extract zip'''
        args = (self.zipfile, '/tmp/extract_zip')

        obj = archive.Manage_Archives('test')
        dir = obj.extract(*args)

        listing = os.listdir(dir)
        expected = ["file1.txt", "file2.xml", "file2.xml.sum"]
        self.assertEqual(listing, expected, "Invalid listing")

    def test_extract_tar(self):
        '''extract tar'''
        args = (self.zipfile, '/tmp/extract_tar')

        obj = archive.Manage_Archives('test')
        dir = obj.extract(*args)

        listing = os.listdir(dir)
        expected = ["file1.txt", "file2.xml", "file2.xml.sum"]
        self.assertEqual(listing, expected, "Invalid listing")


if __name__ == "__main__":
    unittest.main()
