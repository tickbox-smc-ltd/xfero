#!/usr/bin/env python
'''Case Conversion'''
import logging.config
import os
from /xfero/ import get_conf as get_conf
from /xfero/.workflow_manager import copy_file as renameFile

try:
    (xfero_logger,.xfero_database, outbound_directory, transient_directory,
     error_directory, xfero_pid) = get_conf.get.xfero_config()
except Exception as err:
    print('Cannot get XFERO Config: %s' % err)
    raise err

logging.config.fileConfig(xfero_logger)
# create logger
logger = logging.getLogger('case_converter')


class Case_Converter(object):

    '''

    **Purpose:**

    This :class:`case_converter.Case_Converter` class provides methods to
    convert from Upper to Lower case and Lower to Upper case.

    **Unit Test Module:** test_case_converter.py

    **Process Flow**

    .. figure::  ../process_flow/case_converter.png
       :align:   center

       Process Flow: Case Converter

    *External dependencies*

    os (/xfero/.workflow_manager.case_converter)
    /xfero/
      get_conf (/xfero/.workflow_manager.case_converter)
      workflow_manager
        copy_file (/xfero/.workflow_manager.case_converter)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/07/2013 | Chris Falck | Ported from Perl Version (FalckMon)           |
    +------------+-------------+-----------------------------------------------+
    | 01/04/2014 | Chris Falck | Converted to Object Orientation class         |
    +------------+-------------+-----------------------------------------------+
    | 27/10/2014 | Chris Falck | modified call to get_conf                     |
    +------------+-------------+-----------------------------------------------+

    '''

    def __init__(self, xfero_token=False):
        '''init'''
        logger.debug('Object initialised: To_Lower')
        self.xfero_token =.xfero_token
        self.filename = ''

    def to_lower(self, filename):
        '''

        *:func:`Case_Converter.to_lower`*

        The :func:`Case_Converter.to_lower` method will convert the supplied
        filename to lower case.

        e.g. the filename ```'FILENAME.TXT'``` would be converted to
        ```'filename.txt'```

        **Usage Notes:**

        None

        *Example usage:*

        ```obj = Case_Converter()```
        ```obj.to_lower(filename)```

        :param filename: Name of file to process
        :returns: The renamed file or raises an Exception

        '''

        self.filename = filename
        logger.info('Convert to %s to lower case. (XFERO_Token=%s)',
                    self.filename, self.xfero_token)

        # Validate input - Check from_name exists

        if os.path.isfile(self.filename) is False:
            logger.error('OSError No such file or directory: %s. \
            (XFERO_Token=%s)', self.filename, self.xfero_token)
            raise OSError(2, 'No such file or directory %s', self.filename)

        head, tail = os.path.split(self.filename)

        new_fn = head + os.sep + tail.lower()

        logger.info('Renaming file from %s to %s. (XFERO_Token=%s)',
                    self.filename, new_fn, self.xfero_token)

        try:
            rename_obj = renameFile.Copy_File(self.xfero_token)
            renamed_file = rename_obj.rename_file(self.filename, new_fn)
        except Exception as err:
            logger.error('Error Renaming file from %s to %s. \
            (XFERO_Token=%s)', self.filename, new_fn, self.xfero_token)
            raise err

        return renamed_file

    def to_upper(self, filename):
        '''

        *:func:`Case_Converter.to_upper`*

        The :func:`Case_Converter.to_upper` method will convert the supplied
        filename to upper case.

        e.g. the filename ```'filename.txt'``` would be converted to
        ```'FILENAME.TXT'```

        **Usage Notes:**

        None

        *Example usage:*

        ```obj = Case_Converter()```
        ```obj.to_upper(filename)```

        :param filename: Name of file to process
        :returns: The renamed file or raises an Exception

        '''
        self.filename = filename
        logger.info('Convert to %s to upper case. (XFERO_Token=%s)',
                    self.filename, self.xfero_token)

        # Validate input - Check from_name exists

        if os.path.isfile(self.filename) is False:
            logger.error('OSError No such file or directory: %s. \
            (XFERO_Token=%s)', self.filename, self.xfero_token)
            raise OSError(2, 'No such file or directory %s. \
            (XFERO_Token=%s)', self.filename, self.xfero_token)

        head, tail = os.path.split(self.filename)

        new_fn = head + os.sep + tail.upper()

        logger.info('Renaming file from %s to %s. (XFERO_Token=%s)',
                    self.filename, new_fn, self.xfero_token)

        try:
            rename_obj = renameFile.Copy_File(self.xfero_token)
            renamed_file = rename_obj.rename_file(self.filename, new_fn)
        except Exception as err:
            logger.error('Error Renaming file from %s to %s. \
            (XFERO_Token=%s)', self.filename, new_fn, self.xfero_token)
            raise err

        return renamed_file


if __name__ == "__main__":

    file_name = '/Users/chrisfalck/Documents/workspace/test-files/COPY_FILE.RTF'
    try:
        obj = Case_Converter()
        print(obj.to_lower(file_name))
    except Exception as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement

    file_name = '/Users/chrisfalck/Documents/workspace/test-files/copy_file.rtf'
    try:
        obj = Case_Converter()
        print(obj.to_upper(file_name))
    except Exception as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement
