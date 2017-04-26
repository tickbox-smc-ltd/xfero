#!/usr/bin/env python
'''Test Case Converter'''
import unittest
import os
import shutil
import /xfero/.workflow_manager.case_converter as convert


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```case_converter```


    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/06/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+

    '''

    def setUp(self):
        '''

        **Purpose:**

        Set up Unit Test artifacts for the class ```Case_Converter```

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
        for filename in ("FILE1", "myfile1"):
            f = open(filename, "w")
            f.write("Just a test file\n")
            f.close()
        os.chdir(self.origdir)

    def tearDown(self):
        '''

        **Purpose:**

        Tear down Unit Test artifacts created in setup() for the function
        ```toLower```

        *Removes*

        Directory tree created in setup function

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        shutil.rmtree(self.dirname)

    def test_toLower_success(self):
        '''

        **Purpose:**

        Uses the ```toLower``` function to convert the filename to lower case
        characters

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```toLower```
        with the expected result:

        ```expected = self.dirname + os.sep + "file1"```

        ```self.assertEqual(expected,result,"To lower case transformation not
        done correctly")```

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

        old_fn = self.dirname + os.sep + "FILE1"
        expected = self.dirname + os.sep + "file1"

        converter = convert.Case_Converter()
        result = converter.to_lower(old_fn)

        self.assertEqual(
            expected, result, "To lower case transformation not done correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_toLower_file_to_xform_does_not_exist(self):
        '''

        **Purpose:**

        Test error trapping of the ```toLower``` function by attempting to
        transform a file called ```filedoesnotexist``` that does not exist on
        the file system.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```toLower```
        with the expected result specified for the OSError which is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'), 'Invalid
        test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        old_fn = self.dirname + os.sep + "filedoesnotexist"

        try:
            converter = convert.Case_Converter()
            result = converter.to_lower(old_fn)
        except OSError as err:
            # print(err)
            # print(err.args)
            # print(err.filename)
            self.assertEqual(
                err.args, (2, 'No such file or directory'),
                'Invalid test result')

    def test_toUpper_success(self):
        '''

        **Purpose:**

        Uses the ```toUpper``` function to convert the filename to upper case
        characters

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```toUpper```
        with the expected result:

        ```expected = self.dirname + os.sep + "FILE1"```

        ```self.assertEqual(expected,result,"To Upper case transformation not
        done correctly")```

        Performs an ```assertEqual``` on the path to ensure the file exists on
        the
        file system with the correct file name:

        ```self.assertEqual(os.path.exists(expected) == 1, True, "File not
        renamed correctly")```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        old_fn = self.dirname + os.sep + "file1"
        expected = self.dirname + os.sep + "FILE1"

        converter = convert.Case_Converter()
        result = converter.to_upper(old_fn)

        self.assertEqual(
            expected, result, "To Upper case transformation not done correctly")

        # Ensure file is on os
        self.assertEqual(
            os.path.exists(expected) == 1, True, "File not renamed correctly")

    def test_toUpper_file_to_xform_does_not_exist(self):
        '''

        **Purpose:**

        Test error trapping of the ```toUpper``` function by attempting to
        transform a file called ```filedoesnotexist``` that does not exist on
        the file system.

        *Test Confirmation*

        The following assertions are performed:

        Performs an ```assertEqual``` on the result of the call to ```toUpper```
        with the expected result specified for the OSError which is returned:

        ```self.assertEqual(err.args, (2, 'No such file or directory'), 'Invalid
        test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        old_fn = self.dirname + os.sep + "filedoesnotexist"

        try:
            converter = convert.Case_Converter()
            result = converter.to_upper(old_fn)
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
