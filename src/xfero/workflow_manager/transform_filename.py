#!/usr/bin/env python
'''Transform Filename'''
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
logger = logging.getLogger('transform_filename')


class Transform_Filename(object):

    '''

    **Purpose:**

    This :class:`transform_filename.Transform_Filename` class provides methods
    delete file name extension, add file name extension, add a prefix, add a
    suffix, remove part of a file name and insert part of a file name.

    **Unit Test Module:** test_delExt.py

    **Process Flow**

    .. figure::  ../process_flow/transform_file.png
       :align:   center

       Process Flow: Transform File 1

    .. figure::  ../process_flow/transform_file_1.png
       :align:   center

       Process Flow: Transform File 2

    .. figure::  ../process_flow/transform_file_2.png
       :align:   center

       Process Flow: Transform File 3

    *External dependencies*

    os (/xfero/.workflow_manager.transform_filename)
    /xfero/
      get_conf (/xfero/.workflow_manager.transform_filename)
      workflow_manager
        copy_file (/xfero/.workflow_manager.transform_filename)

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
        '''__init__'''
        logger.debug('Object initialised: Delete_Extension')
        self.xfero_token =.xfero_token
        self.filename = ''

    def delete_extension(self, file_name):
        '''

        *:func:`Transform_Filename.delete_extension`*

        The :func:`Transform_Filename.delete_extension` method  searches for the
        final '.' and removes it and any trailing characters, effectively
        removing any filename extension.

        e.g. .txt or .csv or .fredbloggs

        **Usage Notes:**

        None

        *Example usage:*

        ```obj = Transform_Filename()```
        ```obj.delete_extension(filename))```

        :param file_name: Name of file to process
        :returns: The renamed file or raises an Exception

        '''

        self.filename = file_name
        logger.info('Delete extension from %s', self.filename)

        # Validate input - Check from_name exists
        if os.path.isfile(self.filename) is False:
            logger.error('OSError No such file or directory: %s',
                         self.filename)
            raise OSError(2, 'No such file or directory', self.filename)

        filename, fileextension = os.path.splitext(self.filename)

        logger.info('Renaming file from %s to %s', self.filename, filename)

        try:
            rename_obj = renameFile.Copy_File(self.xfero_token)
            renamed_file = rename_obj.rename_file(self.filename, filename)
        except OSError as err:
            logger.error('Error Renaming file from %s to %s',
                         self.filename, filename)
            raise err

        return renamed_file

    def add_extension(self, filename, extension):
        '''

        *:func:`Transform_Filename.add_extension`*

        The :func:`Transform_Filename.add_extension` method  inserts the
        supplied file extension to the filename.

        e.g. .txt or .csv or .fredbloggs

        **Usage Notes:**

        None

        *Example usage:*

        ```obj = Transform_Filename()```
        ```obj.add_extension(filename, extension)```

        :param: filename: Name of file to process
        :param: extension: Extension to add to the file name
        :returns: The renamed file or raises an Exception

        '''

        self.filename = filename
        self.extension = extension

        logger.info('Add extension %s to file %s', self.extension,
                    self.filename)

        # Validate input - Check from_name exists
        if os.path.isfile(self.filename) is False:
            logger.error('OSError No such file or directory: %s', self.filename)
            raise OSError(2, 'No such file or directory', self.filename)

        logger.info('renaming file from %s to %s', self.filename,
                    (self.filename + self.extension))

        try:
            rename_obj = renameFile.Copy_File(self.xfero_token)
            renamed_file = rename_obj.rename_file(
                self.filename, self.filename + self.extension)
        except Exception as err:
            logger.error('Error Renaming file from %s to %s',
                         self.filename, self.filename + self.extension)
            raise err

        return renamed_file

    def add_prefix(self, filename, prefix):
        '''
        *:func:`Transform_Filename.add_prefix`*

        The :func:`Transform_Filename.add_prefix` method prepends the supplied
        prefix to the supplied filename.

        *Usage Notes:*

        None

        *Example usage:*

        ```obj = Transform_Filename()```
        ```obj.add_prefix(filename, prefix)```

        :param: filename: Name of file to process
        :param: prefix: Prefix to add to the file name
        :returns: The renamed file or raises an Exception

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/07/2013 | Chris Falck | Ported from Perl Version (FalckMon)       |
        +------------+-------------+-------------------------------------------+

        '''
        self.filename = filename
        self.prefix = prefix

        logger.info('Add Prefix %s to file %s', self.prefix, self.filename)

        # Validate input - Check from_name exists
        if os.path.isfile(self.filename) is False:
            logger.error('OSError No such file or directory: %s',
                         self.filename)
            raise OSError(2, 'No such file or directory', self.filename)

        head, tail = os.path.split(self.filename)

        new_fn = head + os.sep + self.prefix + tail

        logger.info('renaming file from %s to %s', self.filename, new_fn)

        try:
            rename_obj = renameFile.Copy_File(self.xfero_token)
            renamed_file = rename_obj.rename_file(self.filename, new_fn)
        except OSError as err:
            logger.error('Error Renaming file from %s to %s', self.filename,
                         new_fn)
            raise err

        return renamed_file

    def add_suffix(self, filename, suffix):
        '''

        *:func:`Transform_Filename.add_suffix`*

        The :func:`Transform_Filename.add_suffix` method adds the supplied
        suffix to the supplied filename.

        *Usage Notes:*

        None

        *Example usage:*

        ```obj = Transform_Filename()```
        ```obj.add_prefix(filename, suffix)```

        :param: filename: Name of file to process
        :param: suffix: Suffix to add to the file name
        :returns: The renamed file or raises an Exception

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/07/2013 | Chris Falck | Ported from Perl Version (FalckMon)       |
        +------------+-------------+-------------------------------------------+

        '''
        self.filename = filename
        self.suffix = suffix

        logger.info('Add Suffix %s to file %s', self.suffix, self.filename)

        # Validate input - Check from_name exists
        if os.path.isfile(self.filename) is False:
            logger.error('OSError No such file or directory: %s', self.filename)
            raise OSError(2, 'No such file or directory', self.filename)

        logger.info('renaming file from %s to %s',
                    self.filename, (self.filename + self.suffix))

        try:
            rename_obj = renameFile.Copy_File(self.xfero_token)
            renamed_file = rename_obj.rename_file(
                self.filename, self.filename + self.suffix)
        except OSError as err:
            logger.error('Error Renaming file from %s to %s',
                         self.filename, (self.filename + self.suffix))
            raise err

        return renamed_file

    def remove_name_part(self, filename, name_element):
        '''

        *:func:`Transform_Filename.remove_name_part`*

        The :func:`Transform_Filename.remove_name_part` method Find the first
        occurrence of the name_element supplied and remove it from the filename.

        *Usage Notes:*

        None

        *Example usage:*

        ```obj = Transform_Filename()```
        ```obj.remove_name_part(filename, name_element)```

        :param: filename: Name of file to process
        :param: name_element: Element to be removed from the file name.

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/07/2013 | Chris Falck | Ported from Perl Version (FalckMon)       |
        +------------+-------------+-------------------------------------------+

        '''
        self.filename = filename
        self.name_element = name_element

        logger.info('Remove filename element %s from file %s',
                    self.name_element, self.filename)

        # Validate input - Check filename exists
        if os.path.isfile(self.filename) is False:
            logger.error('OSError No such file or directory: %s',
                         self.filename)
            raise OSError(2, 'No such file or directory', self.filename)

        head, tail = os.path.split(self.filename)

        # index holds the starting index of the name_element
        index = tail.find(self.name_element)

        if index == -1:
            logger.error('TypeError: Request to remove name element from file \
            %s, but invalid self.name_element %s supplied',
                         self.filename, self.name_element)
            raise TypeError(1, 'Invalid name_element: %s' % self.name_element)

        part1 = tail[0:index]
        part2 = tail[index + len(self.name_element): len(tail)]

        new_fn = head + os.sep + part1 + part2
        logger.info('Rename file from %s to %s', self.filename, new_fn)

        try:
            rename_obj = renameFile.Copy_File(self.xfero_token)
            renamed_file = rename_obj.rename_file(self.filename, new_fn)
        except Exception as err:
            # raise err
            logger.error('Error Renaming file from %s to %s',
                         self.filename, new_fn)
            raise err

        return renamed_file

    def insert_name_part(self, filename, eyecatcher, insert_element, where):
        '''
        *:func:`Transform_Filename.insert_name_part`*

        The :func:`Transform_Filename.insert_name_part` method Find the first
        occurrence of the eyecatcher supplied and inserts the supplied text
        element into the filename either before or after the eyecatcher.

        *Usage Notes:*

        None

        *Example usage:*

        ```obj = Transform_Filename()```
        ```obj.insert_name_part(filename, name_element)```

        :param: filename: Name of file to process
        :param: eyecatcher: The eyecatcher that helps identify where text is to
        be inserted into the filename.
        :param: insert_element: The element which is to be inserted into the
        filename.
        :param: where: Ths parameter determines where the element to be inserted
        is to be placed. Either before or after the eyecatcher.
        :returns: renamed file

        +------------+-------------+-------------------------------------------+
        | Date       | Author      | Change Details                            |
        +============+=============+===========================================+
        | 02/07/2013 | Chris Falck | Ported from Perl Version (FalckMon)       |
        +------------+-------------+-------------------------------------------+

        '''
        self.filename = filename
        self.eyecatcher = eyecatcher
        self.insert_element = insert_element
        self.where = where

        logger.info('Insert filename elements into %s', self.filename)

        # Validate input - Check filename exists
        if os.path.isfile(self.filename) is False:
            logger.error('OSError No such file or directory: %s', self.filename)
            raise OSError(2, 'No such file or directory', self.filename)

        head, tail = os.path.split(self.filename)

        # index holds the starting index of the eyecatcher
        index = tail.find(self.eyecatcher)
        if index == -1:
            logger.error('TypeError: Request to insert name element into file \
            %s, but invalid eyecatcher %s suplied', self.filename,
                         self.eyecatcher)
            raise TypeError("Eye-catcher invalid: %s" % self.eyecatcher)

        if where.capitalize() == 'Before':
            part1 = tail[0:index]
            part2 = tail[index:len(self.filename)]
        elif where.capitalize() == 'After':
            new_index = index + len(eyecatcher)
            part1 = tail[0:new_index]
            part2 = tail[new_index:len(self.filename)]
        else:
            logger.error(
                'TypeError: Invalid Position supplied. \
                Should be Before or After')
            raise TypeError(
                'Invalid Position supplied. \
                Should be Before or After')

        new_fn = head + os.sep + part1 + insert_element + part2

        logger.info('Rename file from %s to %s', self.filename, new_fn)

        try:
            rename_obj = renameFile.Copy_File(self.xfero_token)
            renamed_file = rename_obj.rename_file(self.filename, new_fn)
        except OSError as err:
            # raise err
            logger.error('Error Renaming file from %s to %s',
                         self.filename, new_fn)
            raise err

        return renamed_file


if __name__ == "__main__":

    file_name = '/Users/chrisfalck/Documents/LetterHead.docx'
    try:
        obj = Transform_Filename()
        print(obj.delete_extension(file_name))
    except Exception as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement
