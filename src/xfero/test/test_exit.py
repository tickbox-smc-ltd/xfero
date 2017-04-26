#!/usr/bin/env python
'''Test Exit'''
import unittest
import /xfero/.workflow_manager.exit as run


class Test(unittest.TestCase):

    '''

    **Purpose:**

    Unit Test class for the function ```exit```


    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/06/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+

    '''

    def setUp(self):
        '''

        **Purpose:**

        Set up Unit Test artifacts for the function ```wf_exit```

        There is no requirement to create artifacts for this test

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
        ```wf_exit```

        There is no requirement to delete artifacts for this test

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''

        pass

    def test_wf_exit_execute_command(self):
        '''

        **Purpose:**

        Uses the ```wf_exit``` function to execute a simple Unix command:
        ```ls -lrt```

        *Test Confirmation*

        The following assertions are performed to confirm that a PID has been
        returned from the call:

        Performs an ```assertIsInstance``` on the result of the call to
        ```wf_exit``` :

        ```self.assertIsInstance(child_pid, int, 'invalid test result')```

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        cmd = "/bin/ls -lrt"

        obj = run.Exit()
        child_pid = obj.exit(cmd)

        self.assertIsInstance(child_pid, int, 'invalid test result')

    def test_wf_exit_execute_script(self):
        '''

        **Purpose:**

        Uses the ```wf_exit``` function to execute a simple Shell script,
        passing it 3 parameters on the call: ```simple.sh passing these
        parameters```

        *Test Confirmation*

        The following assertions are performed to confirm that a PID has been
        returned from the call:

        Performs an ```assertIsInstance``` on the result of the call to
        ```wf_exit``` :

        ```self.assertIsInstance(child_pid, int, 'invalid test result')```

        Test ```wf_exit``` by executing a shell script.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/06/2013 | Chris Falck | Created                                   |
        +------------+-------------+-------------------------------------------+

        '''
        cmd = "/Users/Documents/test_files/sh_script/simple.sh pass the param"

        obj = run.Exit()
        child_pid = obj.exit(cmd)

        self.assertIsInstance(child_pid, int, 'invalid test result')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
