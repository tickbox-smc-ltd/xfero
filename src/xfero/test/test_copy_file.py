#!/usr/bin/env python
'''Test Copy FIle'''
import os
import shutil
import unittest
import /xfero/.workflow_manager.copy_file as copy_file


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```copy_file```


    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/06/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+

    '''

    def setUp(self):
        '''

        **Purpose:**

        Set up Unit Test artifacts for the function ```copy_file```.

        *Notes:*

        This function uses files in the ```test``` directory in the XFERO
        installation directory.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        self.origdir = os.getcwd()
        for dirn in ("targetdir", "sourcedir", 'workingdir'):
            self.dirname = self.origdir + os.sep + dirn
            os.makedirs(self.origdir + os.sep + dirn)

            os.chdir(self.dirname)  # This is sourcedir
            for filename in ("file1", "file2", "file3", "move_me.txt",
                             "dont_move.txt", "dont_move.txt"):
                fhandle = open(filename, "w")
                fhandle.write("Just a test file\n")
                fhandle.close()
            os.chdir(self.origdir)

        self.created_files_list = []

    def tearDown(self):
        '''

        **Purpose:**

        Tear down Unit Test artifacts created in setup() for the function
        ```copy_file```

        *Removes*

        Created files

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        for dirn in ('targetdir', 'sourcedir', 'doesnotexist', 'workingdir'):
            self.dirname = self.origdir + os.sep + dirn
            if os.path.isdir(self.dirname):
                shutil.rmtree(self.dirname)

    def test_copy_files(self):
        '''

        **Purpose:**

        Uses the ```copy_files``` function to create a copy of the file and add
        the current timestamp.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ``copy_file``` with the original filename:

        ```self.assertEqual(copied_fn[0:5], self.full_file_name[0:5])```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        self.src_files = os.listdir(self.dirname)
        for self.file_name in self.src_files:

            self.full_file_name = os.path.join(self.dirname, self.file_name)
            if os.path.isfile(self.full_file_name):

                copied = copy_file.Copy_File()
                copied_fn = copied.copy_file(self.full_file_name)

                self.assertEqual(copied_fn[0:5], self.full_file_name[0:5])

                self.created_files_list.append(copied_fn)

    def test_copy_file_file_does_not_exist(self):
        '''

        **Purpose:**

        Uses the ```copy_files``` function to create a copy of a file which does
        not exist to generate an OSError.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```copy_file``` with the original filename:

        ```self.assertEqual(err.args, (5, 'Error copying file
        /Users/chrisfalck/Documents/workspace/FTH/test_files/filedoesnotexist'),
        'Invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        # Only way to test is to change permissions on the file to be renamed
        self.full_file_name = self.dirname + os.sep + "filedoesnotexist"

        try:
            copied = copy_file.Copy_File()
            copied.copy_file(self.full_file_name)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')

    def test_success_move(self):
        '''

        **Purpose:**

        Uses the ```move_file``` function to move the file to a new location.
        The new location does not exist so the function will create the
        directory

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```move_file``` with the expected result:

        ```expected = self.tdir + os.sep + 'move_me.txt'```

        ```self.assertEqual(expected,result,"Not moved correctly")```

        Performs an ```assertEqual``` on the path to ensure the file exists on
        the file system with the correct file name:

        ```self.assertEqual(os.path.exists(expected) == 1, True, "File not
        renamed correctly")```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        self.origdir = os.getcwd()
        self.tdir = self.origdir + os.sep + 'doesnotexist'
        self.sfile = self.origdir + os.sep + 'sourcedir' + os.sep + \
        'move_me.txt'

        args = (self.sfile, self.tdir)

        expected = self.tdir + os.sep + 'move_me.txt'

        moved = copy_file.Copy_File()
        moved_fn = moved.move_file(*args)

        self.assertEqual(expected, moved_fn, "Not moved correctly")
        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_success_move_targetdir_exists(self):
        '''

        **Purpose:**

        Uses the ```move_file``` function to move the file to a new location.
        The new location exists so there is no need to create it

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```move_file``` with the expected result:

        ```expected = self.tdir + os.sep + 'move_me.txt'```

        ```self.assertEqual(expected,result,"Not moved correctly")```

        Performs an ```assertEqual``` on the path to ensure the file exists on
        the file system with the correct file name:

        ```self.assertEqual(os.path.exists(expected) == 1, True, "File not
        renamed correctly")```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        self.origdir = os.getcwd()
        self.tdir = self.origdir + os.sep + 'targetdir'
        self.sfile = self.origdir + os.sep + 'sourcedir' + os.sep + \
        'move_me.txt'

        args = (self.sfile, self.tdir)

        expected = self.tdir + os.sep + 'move_me.txt'

        moved = copy_file.Copy_File()
        moved_fn = moved.move_file(*args)

        self.assertEqual(expected, moved_fn, "Not moved correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_file_to_move_does_not_exist(self):
        '''

        **Purpose:**

        Test error trapping of the ```move_file``` function by attempting to
        move a file called ```non-existent_file.txt``` that does not exist on
        the file system.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```move_file``` with the expected result specified for the OSError
        which is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'),
        'Invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        self.origdir = os.getcwd()
        self.tdir = self.origdir + os.sep + 'targetdir'
        self.sfile = self.origdir + os.sep + 'sourcedir' + \
            os.sep + 'non-existent_file.txt'

        args = (self.sfile, self.tdir)

        try:
            moved = copy_file.Copy_File()
            moved_fn = moved.move_file(*args)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')

    def test_target_dir_is_not_a_directory(self):
        '''

        **Purpose:**

        Test error trapping of the ```move_file``` function by attempting to
        move a file to a location which is not a directory.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```move_file``` with the expected result specified for the OSError which
        is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'),
        'Invalid test result')```

        Error test to capture an event when the target directory is not a
        directory

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        self.origdir = os.getcwd()
        self.tdir = self.origdir + os.sep + \
            'targetdir' + os.sep + 'dont_move.txt'
        self.sfile = self.origdir + os.sep + 'sourcedir' + os.sep + \
        'move_me.txt'

        args = (self.sfile, self.tdir)

        try:
            moved = copy_file.Copy_File()
            moved_fn = moved.move_file(*args)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')

    def test_renameFile_success(self):
        '''

        **Purpose:**

        Uses the ```move_file``` function to change the name of the file

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```renameFile``` with the expected result:

        ```expected = self.dirname + os.sep + "renamed"```

        ```self.assertEqual(expected,result,"File not renamed correctly")```

        Performs an ```assertEqual``` on the path to ensure the file exists on
        the file system with the correct file name:

        ```self.assertEqual(os.path.exists(expected) == 1, True, "File not
        renamed correctly")```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        self.origdir = os.getcwd()
        self.tdir = self.origdir + os.sep + 'sourcedir'
        self.sfile = self.tdir + os.sep + 'move_me.txt'
        self.tfile = self.tdir + os.sep + 'Ive_moved.txt'

        args = (self.sfile, self.tfile)

        expected = self.tfile

        moved = copy_file.Copy_File()
        moved_fn = moved.rename_file(*args)

        self.assertEqual(expected, moved_fn, "File not renamed correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_renameFile_file_to_rename_does_not_exist(self):
        '''

        **Purpose:**

        Test error trapping of the ```renameFile``` function by rename a file
        called ```filedoesnotexist``` that does not exist on the file system.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```renameFile``` with the expected result specified for the OSError
        which is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'),
        'Invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        # Only way to test is to change permissions on the file to be renamed

        self.origdir = os.getcwd()
        self.tdir = self.origdir + os.sep + 'sourcedir'
        self.sfile = self.tdir + os.sep + "filedoesnotexist"
        self.tfile = self.tdir + os.sep + "new_file_name"

        args = (self.sfile, self.tfile)

        try:
            moved = copy_file.Copy_File()
            moved_fn = moved.rename_file(*args)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')

    def test_renameFile_directory_to_rename_file_into_does_not_exist(self):
        '''

        **Purpose:**

        Test error trapping of the ```renameFile``` function by renaming a file
        to a directory that does not exist on the file system.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```renameFile``` with the expected result specified for the OSError
        which is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'),
        'Invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        self.origdir = os.getcwd()
        self.tdir = self.origdir + os.sep + 'sourcedir'
        self.sfile = self.tdir + os.sep + "file2"
        self.tfile = "/directory/does/not/exist/new_file_name"

        args = (self.sfile, self.tfile)

        try:
            moved = copy_file.Copy_File()
            moved_fn = moved.rename_file(*args)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_cksum']
    unittest.main()
