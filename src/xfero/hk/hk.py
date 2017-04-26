#!/usr/bin/env python
'''HK'''
import os
import sys
import time
import re
import logging.config
import /xfero/.get_conf as get_conf

try:
    (xfero_logger,.xfero_database, outbound_directory, transient_directory,
     error_directory, xfero_pid) = get_conf.get.xfero_config()
except Exception as err:
    print('Cannot get XFERO Config: %s' % err)
    raise err

logging.config.fileConfig(xfero_logger)
# create logger# create logger
logger = logging.getLogger('housekeeping')


class HK(object):

    '''

    **Purpose:**

    The :class:`housekeeping.HK` class removes files that match the supplied
    filename pattern from specified directories which are older than a supplied
    age.

    **Unit Test Module:** test_delete_old_files.py

    **Process Flow**

    .. figure::  ../process_flow/housekeeping.png
       :align:   center

       Process Flow: Housekeeping

    *External dependencies*

        os (/xfero/.hk.housekeeping-class)
        re (/xfero/.hk.housekeeping-class)
        time (/xfero/.hk.housekeeping-class)
        /xfero/
          get_conf (/xfero/.hk.housekeeping-class)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/07/2013 | Chris Falck | Ported from Perl Version (FalckMon)           |
    +------------+-------------+-----------------------------------------------+
    | 22/04/2014 | Chris Falck | Converted to OO                               |
    +------------+-------------+-----------------------------------------------+
    | 27/10/2014 | Chris Falck | modified call to get_conf                     |
    +------------+-------------+-----------------------------------------------+

    '''

    def __init__(self):
        '''init'''
        logger.info('Object initialised: HK')
        self.purge_dir = ''
        self.fn_pattern = ''
        self.num_days = 32
        self.subdir = False

    def delete_old_file(self, purge_dir, fn_pattern, num_days, subdir=False):
        '''

        *:func:`HK.delete_old_files`*

        The :func:`HK.delete_old_files` method is designed to be run from a
        scheduled task to ensures that the file system is managed efficiently.

        **Usage Notes:**

        Files that are successfully transferred should be automatically removed
        by the COTS product used. This is not always the case and in some
        circumstances it is necessary to do this manually, hence the need for
        this method.

        This method is also for managing service files/logs which need to be
        retained for a specified time before being discarded.

        With subdir=True files in sub-directories below the supplied directory
        will also be house kept.

        *Example usage:*

        ```delete_old_files(purge_dir, fn_pattern, num_days, subdir)```

        :param purge_dir: Directory to purge
        :param fn_pattern: Filename pattern match
        :param num_days: Number of days old the file must be to be purged
        :param subdir: True or False. Indicates if subdirectories are to be
        processed
        :returns: OSError: 2, No such file or directory
        :returns: OSError: 3, Error Renaming file

        '''

        self.purge_dir = purge_dir
        self.fn_pattern = fn_pattern
        self.num_days = num_days
        self.subdir = subdir

        try:
            os.path.isdir(self.purge_dir)
        except Exception as err:
            logger.error(
                'Supplied directory is not a directory %s', self.purge_dir)
            raise TypeError('Error: %s is not a Directory!', self.purge_dir)

        logger.info('purge_dir=%s, fn_pattern=%s, num_days=%s, subdir=%s',
                    self.purge_dir, self.fn_pattern, self.num_days, self.subdir)

        logger.info(
            'Calculate age of file above which they should be \
            deleted in seconds')
        purge_age = (int(self.num_days) * 86400)  # Get in seconds
        logger.info('Age of files to delete in seconds = %s', purge_age)

        now = time.time()

        for found in os.listdir(self.purge_dir):
            fullpath = os.path.join(self.purge_dir, found)

            if os.path.isfile(fullpath):
                if os.path.getmtime(fullpath) < (now - purge_age):
                    logger.info(
                        'Testing filename pattern %s with file %s',
                        self.fn_pattern, fullpath)
                    matched = re.search(self.fn_pattern, found)
                    logger.info('matched=%s', matched)
                    if matched is None:
                        matched = re.match(self.fn_pattern, found)
                    logger.info('matched=%s', matched)
                    if matched is not None:
                        logger.info('Deleting file %s', fullpath)
                        try:
                            os.remove(fullpath)
                        except (OSError, IOError) as err:
                            raise err

            elif os.path.isdir(fullpath) and self.subdir == 'True':
                logger.info('Deleting files from sub-directory %s', fullpath)

                subdir_obj = HK()
                subdir_obj.delete_old_file(
                    fullpath, fn_pattern, num_days, subdir)

        return

if __name__ == "__main__":

    purge_dir = "/Users/chrisfalck/Documents/workspace/XFERO/test_files/tmp"
    num_days = 20
    pattern = '^Fred'
    obj = HK()
    obj.delete_old_file(purge_dir, pattern, num_days, 'True')
