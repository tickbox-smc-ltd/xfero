#!/usr/bin/env python
'''Test Transform File name'''
import unittest
import os
import shutil
from /xfero/.workflow_manager import transform_filename as transform

class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```delExt```


    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/06/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+

    '''

    def setUp(self):
        '''

        **Purpose:**

        Set up Unit Test artifacts for the function ```delExt```

        *Creates:*

        Test Directory
        Test Files

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        # Create temporary directory and files to rename
        self.origdir = os.getcwd()
        self.dirname = self.origdir + os.sep + 'workingdir'
        os.makedirs(self.dirname)

        os.chdir(self.dirname)  # This is sourcedir
        for filename in ("FILE1.txt", "FILE2.xls", "FILE3.document", "file1",
                         "file2", "file3", "file_name.txt",
                         "long_file_name.txt", "an_even_longer_file_name.txt"):
            fhandle = open(filename, "w")
            fhandle.write("Just a test file\n")
            fhandle.close()
        os.chdir(self.origdir)

    def tearDown(self):
        '''

        **Purpose:**

        Tear down Unit Test artifacts created in setup() for the function
        ```delExt```

        *Removes*

        Directory tree created in setup function

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        shutil.rmtree(self.dirname)

    def test_delExt_success(self):
        '''

        **Purpose:**

        Uses the ```delExt``` function to delete the file name extension
        ```.document``` from the file called ```FILE3.document```

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```delExt```
        with the expected result:

        ```expected = self.dirname + os.sep + "FILE3"```

        ```self.assertEqual(expected,result,"delExt test result not
        expected")```

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

        old_fn = self.dirname + os.sep + "FILE3.document"
        expected = self.dirname + os.sep + "FILE3"

        transform_obj = transform.Transform_Filename()
        result = transform_obj.delete_extension(old_fn)

        self.assertEqual(expected, result, "delExt test result not expected")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_delExt_file_to_xform_does_not_exist(self):
        '''

         **Purpose:**

        Test error trapping of the ```delExt``` function by attempting to delete
        an extension from a file called ```filedoesnotexist.txt``` that does not
        exist on the file system.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```delExt```
        with the expected result specified for the OSError which is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'), 'Invalid
        test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        # Only way to test is to change permissions on the file to be renamed
        old_fn = self.dirname + os.sep + "filedoesnotexist.txt"

        try:
            transform_obj = transform.Transform_Filename()
            result = transform_obj.delete_extension(old_fn)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')

    def test_addExt_success(self):
        '''

        **Purpose:**

        Uses the ```addExt``` function to add the extension ```.txt``` to the
        file called ```file1```

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```addExt```
        with the expected result:

        ```expected = self.dirname + os.sep + "file1.txt"```

        ```self.assertEqual(expected,result,"File extension not added
        correctly")```

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

        old_fn = self.dirname + os.sep + "file1"
        expected = self.dirname + os.sep + "file1.txt"
        args = (old_fn, '.txt')

        transform_obj = transform.Transform_Filename()
        result = transform_obj.add_extension(*args)

        self.assertEqual(
            expected, result, "File extension not added correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_addExt_file_does_not_exist(self):
        '''

        **Purpose:**

        Test error trapping of the ```addExt``` function by attempting to add
        the extension ```.txt``` to a file called ```filedoesnotexist``` that
        does not exist on the file system.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```addExt```
        with the expected result specified for the OSError which is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'), 'Invalid
        test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        # Only way to test is to change permissions on the file to be renamed
        self.full_file_name = self.dirname + os.sep + "filedoesnotexist"
        args = (self.full_file_name, '.txt')

        try:
            transform_obj = transform.Transform_Filename()
            result = transform_obj.add_extension(*args)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')

    def test_addPrefix_success(self):
        '''

        **Purpose:**

        Uses the ```addPrefix``` function to add the prefix ```PREFIX_``` to the
        file called ```file1```

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```addPrefix``` with the expected result:

        ```expected = self.dirname + os.sep + "PREFIX_file1"```

        ```self.assertEqual(expected,result,"Prefix not added correctly")```

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

        old_fn = self.dirname + os.sep + "file1"
        expected = self.dirname + os.sep + "PREFIX_file1"
        args = (old_fn, 'PREFIX_')

        transform_obj = transform.Transform_Filename()
        result = transform_obj.add_prefix(*args)

        self.assertEqual(expected, result, "Prefix not added correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_addPrefix_file_does_not_exist(self):
        '''

        **Purpose:**

        Test error trapping of the ```addExt``` function by attempting to add a
        prefix ```PREFIX_``` to a file called ```filedoesnotexist``` that does
        not exist on the file system.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```addPrefix``` with the expected result specified for the OSError which
        is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'),
        'Invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        # Only way to test is to change permissions on the file to be renamed
        self.full_file_name = self.dirname + os.sep + "filedoesnotexist"
        args = (self.full_file_name, 'PREFIX_')

        try:
            transform_obj = transform.Transform_Filename()
            result = transform_obj.add_prefix(*args)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')

    def test_addSuffix_success(self):
        '''

        **Purpose:**

        Uses the ```addSuffix``` function to add the suffix ```_SUFFIX``` to the
        file called ```file1```

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```addSuffix``` with the expected result:

        ```expected = self.dirname + os.sep + "file1_SUFFIX"```

        ```self.assertEqual(expected,result,"Suffix not added correctly")```

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

        old_fn = self.dirname + os.sep + "file1"
        expected = self.dirname + os.sep + "file1_SUFFIX"
        args = (old_fn, '_SUFFIX')

        transform_obj = transform.Transform_Filename()
        result = transform_obj.add_suffix(*args)

        self.assertEqual(expected, result, "Suffix not added correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_addSuffix_file_does_not_exist(self):
        '''

        **Purpose:**

        Test error trapping of the ```addSuffix``` function by attempting to add
        a suffix ```_SUFFIX``` to a file called ```filedoesnotexist``` that does
        not exist on the file system.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```addSuffix``` with the expected result specified for the OSError which
        is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'),
        'Invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        # Only way to test is to change permissions on the file to be renamed
        self.full_file_name = self.dirname + os.sep + "filedoesnotexist"
        args = (self.full_file_name, '_SUFFIX')

        try:
            transform_obj = transform.Transform_Filename()
            result = transform_obj.add_prefix(*args)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')

    def test_removeNameElement_at_start_of_filename(self):
        '''

        **Purpose:**

        Uses the ```removeNameElement``` function to remove part of the file
        name that begins at the start of the filename
        ```an_even_longer_file_name.txt``` The test removes ```an_``` from the
        filename.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```removeNameElement``` with the expected result:

        ```expected = self.dirname + os.sep + "even_longer_file_name.txt"```

        ```self.assertEqual(expected,result,"Element removal not done
        correctly")```

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

        old_fn = self.dirname + os.sep + "an_even_longer_file_name.txt"
        to_remove = 'an_'
        expected = self.dirname + os.sep + "even_longer_file_name.txt"
        args = (old_fn, to_remove)

        transform_obj = transform.Transform_Filename()
        result = transform_obj.remove_name_part(*args)

        self.assertEqual(
            expected, result, "Element removal not done correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_removeNameElement_in_middle_of_filename(self):
        '''

        **Purpose:**

        Uses the ```removeNameElement``` function to remove part of the file
        name that is in the middle of the filename
        ```an_even_longer_file_name.txt``` The test removes ```_longer```
        from the filename.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```removeNameElement``` with the expected result:

        ```expected = self.dirname + os.sep + "an_even_file_name.txt"```

        ```self.assertEqual(expected,result,"Element removal not done
        correctly")```

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

        old_fn = self.dirname + os.sep + "an_even_longer_file_name.txt"
        to_remove = '_longer'
        expected = self.dirname + os.sep + "an_even_file_name.txt"
        args = (old_fn, to_remove)

        transform_obj = transform.Transform_Filename()
        result = transform_obj.remove_name_part(*args)

        self.assertEqual(
            expected, result, "Element removal not done correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_removeNameElement_in_end_of_filename(self):
        '''

        **Purpose:**

        Uses the ```removeNameElement``` function to remove part of the file
        name that is at the end of the filename
        ```an_even_longer_file_name.txt``` The test removes ```xt``` from the
        filename.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```removeNameElement``` with the expected result:

        ```expected = self.dirname + os.sep + "an_even_longer_file_name.t"```

        ```self.assertEqual(expected,result,"Element removal not done
        correctly")```

        Performs an ```assertEqual``` on the path to ensure the file exists on
        the file system with the correct file name:

        ```self.assertEqual(os.path.exists(expected) == 1, True,
        "File not renamed correctly")```

        Test removal of name element in the middle of a filename

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        old_fn = self.dirname + os.sep + "an_even_longer_file_name.txt"
        to_remove = 'xt'
        expected = self.dirname + os.sep + "an_even_longer_file_name.t"
        args = (old_fn, to_remove)

        transform_obj = transform.Transform_Filename()
        result = transform_obj.remove_name_part(*args)

        self.assertEqual(
            expected, result, "Element removal not done correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_removeNameElement_invalid_element(self):
        '''

        **Purpose:**

        Tests error trapping of the ```removeNameElement``` function by passing
        an invalid eyecatcher that does not exist in the filename.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```removeNameElement``` with the expected TypeError being returned:

        ```self.assertEqual(err.args, (1, 'Invalid Eyecatcher: %s'
        % eyecatcher), 'Invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        old_fn = self.dirname + os.sep + "an_even_longer_file_name.txt"
        to_remove = 'INVALID'
        args = (old_fn, to_remove)

        try:
            transform_obj = transform.Transform_Filename()
            result = transform_obj.remove_name_part(*args)
        except TypeError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (1, 'Invalid name_element: %s' % to_remove),
                'Invalid test result')

    def test_insertTxt_before_eyecatcher_success(self):
        '''

        **Purpose:**

        Uses the ```insertTxt``` function to insert text into the filename
        before the supplied eyecatcher. Filename = file_name.txt, eyecatcher =
        name, text to insert
        ``= INSERTED_``

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```insertTxt``` with the expected result:

        ```expected = self.dirname + os.sep + "file_INSERTED_name.txt"```

        ```self.assertEqual(expected,result,"Text insert not done correctly")```

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

        old_fn = self.dirname + os.sep + "file_name.txt"
        eyecatcher = 'name'
        inserted_txt = 'INSERTED_'
        expected = self.dirname + os.sep + "file_INSERTED_name.txt"

        args = (old_fn, eyecatcher, inserted_txt, 'Before')

        transform_obj = transform.Transform_Filename()
        result = transform_obj.insert_name_part(*args)

        self.assertEqual(expected, result, "Text insert not done correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_insertTxt_after_eyecatcher_success(self):
        '''

        **Purpose:**

        Uses the ```insertTxt``` function to insert text into the filename after
        the supplied eyecatcher. Filename = file_name.txt, eyecatcher = name,
        text to insert = _INSERTED

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```insertTxt``` with the expected result:

        ```expected = self.dirname + os.sep + "file_name_INSERTED.txt"```

        ```self.assertEqual(expected,result,"Text insert not done correctly")```

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
        old_fn = self.dirname + os.sep + "file_name.txt"
        eyecatcher = 'name'
        inserted_txt = '_INSERTED'
        expected = self.dirname + os.sep + "file_name_INSERTED.txt"

        args = (old_fn, eyecatcher, inserted_txt, 'After')

        transform_obj = transform.Transform_Filename()
        result = transform_obj.insert_name_part(*args)

        self.assertEqual(expected, result, "Text insert not done correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_insertTxt_invalid_eyecatcher(self):
        '''

        **Purpose:**

        Tests error trapping of the ```insertTxt``` function by passing an
        invalid eyecatcher that does not exist in the filename.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```insertTxt``` with the expected TypeError being returned:

        ```self.assertEqual(err.args, (1, 'Invalid Eyecatcher: %s'
        % eyecatcher), 'Invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        old_fn = self.dirname + os.sep + "file_name.txt"
        eyecatcher = 'chris'
        inserted_txt = '_INSERTED'

        args = (old_fn, eyecatcher, inserted_txt, 'After')

        try:
            transform_obj = transform.Transform_Filename()
            result = transform_obj.insert_name_part(*args)
        except TypeError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args[0], ('Eye-catcher invalid: %s' % eyecatcher),
                'Invalid test result')

    def test_insertTxt_file_does_not_exist(self):
        '''

        **Purpose:**

        Test error trapping of the ```insertTxt``` function by attempting to
        insert text into a file called ```doesnotexist.txt``` that does not
        exist on the file system.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to
        ```insertTxt``` with the expected result specified for the OSError which
        is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'),
        'Invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        old_fn = self.dirname + os.sep + "doesnotexist.txt"
        eyecatcher = 'not'
        inserted_txt = '_INSERTED'

        args = (old_fn, eyecatcher, inserted_txt, 'After')

        try:
            transform_obj = transform.Transform_Filename()
            result = transform_obj.insert_name_part(*args)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
