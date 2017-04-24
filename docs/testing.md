# Testing

Testing has been performed using a unit testing framework called ```Unittest```.

## Assertions

An important statement is the assert statement. The syntax for this statement is:

```assert condition[, message]```

In the assert statement, the condition is tested, and if it evaluates false, an AssertionError exception is raised. If there's a message, it is printed with the AssertionError.

We have used assert statements to test all functionality of 'XO', to assert conditions that we believe must always be true. If we are correct, the program runs as expected. But, if a programming error or mistaken assumption invalidates the condition, we are informed by an assertion error.

AssertionError exceptions are handled using the unittest module. To write tests, we create test cases that are subclasses of the unit test. Test Case class. Our subclasses can use the methods defined by the superclass. Many of those methods' names begin with the prefix "assert." By calling these methods, you have the test case make assertions about your program in a controlled environment. Any AssertionErrors that arise are handled by the framework and reported as a failure of the associated test. Other exceptions are regarded as errors.

## Test Failures

When errors and failures occur, you are informed about it:

F

FAIL: test_bad_input (__main__.TestCube)

- Traceback (most recent call last):
File "V:\workspace\UnitTesting\src\testable.py", line 17, in test_bad_input self.assertRaises(TypeError, cube, 'x')

AssertionError: TypeError not raised by cube

## Test Success

When a test is successful, very little information is returned as it runs silently. Below is sample output from a successful run of 3 tests:

...

- Ran 3 tests in 0.000s

OK

The three dots at the top represent the three tests. If they had failed, you would have seen an "F" replacing each failure. If there were significant errors, you would have seen an "E." Such error indications usually mean that something is wrong with your logic. You see the test count and the time for the duration of the tests' run.
