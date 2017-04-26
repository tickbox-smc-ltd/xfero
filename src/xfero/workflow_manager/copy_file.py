#!/usr/bin/env python
'''Copy File'''
import shutil
import os
import time
import logging.config
import errno
from /xfero/ import get_conf as get_conf

try:
    (xfero_logger,.xfero_database, outbound_directory, transient_directory,
     error_directory, xfero_pid) = get_conf.get.xfero_config()
except Exception as err:
    print('Cannot get XFERO Config: %s' % err)
    raise err

logging.config.fileConfig(xfero_logger)
# create logger
logger = logging.getLogger('copy_file')


class Copy_File(object):

    '''

    **Purpose:**

    This :class:`copy_file.Copy_File` class provides file copy, move and rename
    functionality.

    **Unit Test Module:** test_copy_file.py

    **Process Flow**

    .. figure::  ../process_flow/copy_file.png
       :align:   center

       Process Flow: Copy File

    *External dependencies*

    os (/xfero/.workflow_manager.copy_file)
    shutil (/xfero/.workflow_manager.copy_file)
    time (/xfero/.workflow_manager.copy_file)
    /xfero/
      get_conf (/xfero/.workflow_manager.copy_file)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/07/2013 | Chris Falck | Ported from Perl Version (FalckMon)           |
    +------------+-------------+-----------------------------------------------+
    | 04/04/2014 | Chris Falck | Converted to Object Orientation class         |
    +------------+-------------+-----------------------------------------------+
    | 27/10/2014 | Chris Falck | modified call to get_conf                     |
    +------------+-------------+-----------------------------------------------+

    '''

    def __init__(self, xfero_token=False):

        logger.debug('Object initialised: Copy_File')
        self.xfero_token =.xfero_token
        self.filename = ''
        self.target = ''

    def copy_file(self, filename):
        '''

        *:func:`Copy_File.copy_file`*

        The :func:`Copy_File.copy_file` method will copy a file in the same
        directory adding an underscore followed by a timestamp to create a
        unique name for the file.

        **Usage Notes:**

        None

        *Example usage:*

        ```obj = Copy_File()```
        ```copied_filename = obj.copy_file(file_name))```

        :param filename: Name of file to copy
        :returns: Copied File Name or OSError

        '''

        logger.info('Copying file %s. (XFERO_Token=%s)',
                    self.filename, self.xfero_token)

        if os.path.exists(filename):
            self.filename = filename

        if not self.filename:
            logger.error("Filename not supplied. (XFERO_Token=%s)", self.xfero_token)
            raise Exception(
                'Filename not supplied to copy_file. \
                (XFERO_Token=%s)' % (self.xfero_token))

        # Get a timestamp
        tstamp = time.time()
        copy_fn = self.filename + '_' + str(tstamp)

        try:
            shutil.copy(self.filename, copy_fn)
        except OSError as err:
            logger.error('Error copying file %s retrying: ERR - %s. \
            (XFERO_Token=%s)', self.filename, err, self.xfero_token)
            try:
                time.sleep(10)
                shutil.copy(self.filename, copy_fn)
            except Exception as err:
                logger.info('Error copying file %s: ERR - %s. (XFERO_Token=%s)',
                            self.filename, err, self.xfero_token)
                raise err

        try:
            os.remove(self.filename)
        except (OSError, IOError) as err:
            logger.warning("Delete file %s exception: %s. (XFERO_Token=%s)",
                           self.filename, err, self.xfero_token)
        return copy_fn

    def move_file(self, filename, target):
        '''

        *:func:`Copy_File.move_file`*

        The :func:`Copy_File.move_file` method renames (moves) the file supplied
        to a destination directory or renames the file in the current directory.

        **Usage Notes:**

        None

        *Example usage:*

        :func:`Copy_File.move_file('``*args``')

        :param filename: Name of file to copy
        :param: target: Directory into which the file will be moved
        :returns: Path to moved file or OSError

        '''

        self.filename = filename
        self.target = target

        # Ensure file to move exists
        logger.info('Checking if %s is a file. (XFERO_Token=%s)',
                    self.filename, self.xfero_token)
        if not os.path.isfile(self.filename):
            logger.error(
                'OSError: No such file or directory - %s. (XFERO_Token=%s)',
                self.filename, self.xfero_token)
            raise OSError(
                2, 'No such file or directory - %s. \
                (XFERO_Token=%s)' % (self.filename, self.xfero_token))
            # return('stop')

        logger.debug('Confirmed that %s is a file. (XFERO_Token=%s)',
                     self.filename, self.xfero_token)

        # Test if target directory exists and if not create it
        logger.debug('Check if %s is a Directory, if not create it. \
        (XFERO_Token=%s)', self.target, self.xfero_token)

        try:
            os.makedirs(self.target)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                logger.error('OSError: Failed to create self.target - %s : \
                errno = %s. (XFERO_Token=%s)', self.target, exc.errno,
                             self.xfero_token)
                raise exc

        logger.debug('Confirmed that %s Directory exists. (XFERO_Token=%s)',
                     self.target, self.xfero_token)

        # Move files
        basename = os.path.basename(self.filename)
        target_file = os.path.join(self.target, basename)

        logger.info('Moving %s to %s. (XFERO_Token=%s)',
                    self.filename, self.target, self.xfero_token)
        try:
            # os.rename(self.filename, target_file)
            shutil.move(self.filename, target_file)
        except OSError as exc:
            logger.error('OSError: Failed to move file - %s to %s : \
            errno = %s. (XFERO_Token=%s)', self.filename, self.target, exc.errno,
                         self.xfero_token)

            time.sleep(10)

            if exc.errno == 18:
                try:
                    shutil.copy2(self.filename, target_file)
                except OSError as exc1:
                    logger.error('Failed to move file - %s to %s : errno = %s. \
                    (XFERO_Token=%s)', self.filename, self.target, exc1.errno,
                                 self.xfero_token)

            time.sleep(10)

            try:
                shutil.move(self.filename, target_file)
            except OSError as exc:
                logger.error('OSError: Failed to move file - %s to %s : \
                errno = %s. (XFERO_Token=%s)', self.filename, self.target,
                             exc.errno, self.xfero_token)
                return 'stop'

        logger.info('Successful move from %s to %s. (XFERO_Token=%s)',
                    self.filename, self.target, self.xfero_token)

        return target_file

    def rename_file(self, from_name, to_name):
        '''

        *:func:`Copy_File.move_file`*

        The :func:`Copy_File.rename_file` method renames a file.

        **Usage Notes:**

        None

        *Example usage:*

        :func:`Copy_File.rename_file('``*args``')

        :param from_name: Name of file to rename
        :param: to_name: Renamed file
        :returns: Path to moved file or OSError

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/07/2013 | Chris Falck | Ported from Perl Version (FalckMon)       |
        +------------+-------------+-------------------------------------------+

        '''
        logger.info('Rename file from %s to %s. (XFERO_Token=%s)',
                    from_name, to_name, self.xfero_token)

        self.filename = from_name
        self.target = to_name

        # Validate input - Check from_name exists
        if os.path.isfile(self.filename) is False:
            logger.error('OSError: No such file or directory: %s. \
            (XFERO_Token=%s)', self.filename, self.xfero_token)
            raise OSError(
                2, 'No such file or directory: %s. \
                (XFERO_Token=%s)' % (self.filename, self.xfero_token))

        # Check to_name directory exists
        head, tail = os.path.split(self.target)

        if os.path.isdir(head) is False:
            logger.error(
                'OSError: No such file or directory: %s. \
                (XFERO_Token=%s)', head, self.xfero_token)
            raise OSError(
                2, 'No such file or directory: %s. \
                (XFERO_Token=%s)' % (head, self.xfero_token))

        try:
            os.rename(self.filename, self.target)
        except OSError as err:
            logger.error('Error Renaming file from %s to %s: \
            (XFERO_Token=%s)', self.filename, self.target, self.xfero_token)
            raise err

        return self.target

if __name__ == "__main__":

    file_name = '/Users/chrisfalck/Documents/workspace/test-files/copy-test.rtf'

    try:
        obj = Copy_File()
        print(obj.copy_file(file_name))
    except OSError as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement

    file_name = '/Users/chrisfalck/Documents/workspace/test-files/move-test.rtf'
    move_dir = '/Users/chrisfalck/Documents/workspace/test-files/tmp/'

    # args = file_name + ', ' + move_dir
    args = (file_name, move_dir)

    try:
        obj = Copy_File()
        print(obj.move_file(*args))
    except OSError as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement
