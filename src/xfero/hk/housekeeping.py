#!/usr/bin/env python

'''Housekeeping'''

def delete_old_files(purge_dir, fn_pattern, num_days, subdir):
    '''

    **Purpose:**

    This is a housekeeping module which removes files that match the supplied
    filename pattern from specified directories which are older than a supplied
    age.

    This function is a timed event that ensures that the file system is managed
    after a period of time.

    With subdir=True files in subdirectories will also be processed.

    NOTE: Files that are successfully transferred would be automatically removed
    by the COTS product used. This function is specifically for managing service
    files/logs which need to be retained for a specified time

    **Usage Notes:**

    *Example usage:*

    ```renameFile(from_name,to_name)``

    :param purge_dir: Directory to purge
    :param fn_pattern: Filename pattern match
    :param num_days: Number of days old the file must be to be purged (This can
    be a fraction of a day expressed as a decimal)
    :param subdir: True or False. Indicates if sub-directories are to be
    processed
    :returns: renamed file
    :returns: OSError: 2, No such file or directory
    :returns: OSError: 3, Error Renaming file

    **Unit Test Module:** test_delete_old_files.py

    *External dependencies*

    os (/xfero/.hk.housekeeping)
    re (/xfero/.hk.housekeeping)
    time (/xfero/.hk.housekeeping)
    /xfero/
      get_conf (/xfero/.hk.housekeeping)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/07/2013 | Chris Falck | Ported from Perl Version (FalckMon)           |
    +------------+-------------+-----------------------------------------------+
    | 27/10/2014 | Chris Falck | modified call to get_conf                     |
    +------------+-------------+-----------------------------------------------+

    '''

    import os
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

    # Remove trailing space
    purge_dir = purge_dir.strip()
    fn_pattern = fn_pattern.strip()
    num_days = num_days.strip()
    subdir = subdir.strip()

    try:
        os.path.isdir(purge_dir)
    except:
        logger.error('Supplied directory is not a directory %s', purge_dir)
        raise TypeError('Error: %s is not a Directory!', purge_dir)

    logger.info('purge_dir=%s, fn_pattern=%s, num_days=%s, subdir=%s',
                purge_dir, fn_pattern, num_days, subdir)

    # logger.info(type(num_days))

    logger.info(
        'Calculate age of file above which they should be deleted in seconds')
    purge_age = (float(num_days) * 86400)  # Get in seconds
    logger.info('Age of files to delete in seconds = %s', purge_age)

    # Loose any decimal places
    purge_age = (int(round(float(purge_age))))

    now = time.time()

    for found in os.listdir(purge_dir):
        fullpath = os.path.join(purge_dir, found)
        if os.path.isfile(fullpath):
            if os.path.getmtime(fullpath) < (now - purge_age):
                logger.info(
                    'Testing filename pattern %s with file %s',
                    fn_pattern, fullpath)
                matched = re.search(fn_pattern, found)
                logger.info('matched=%s', matched)
                if matched is None:
                    matched = re.match(fn_pattern, found)
                logger.info('matched=%s', matched)
                if matched is not None:
                    logger.info('Deleting file %s', fullpath)
                    try:
                        os.remove(fullpath)
                    except (OSError, IOError) as err:
                        raise err

        elif os.path.isdir(fullpath) and subdir == 'True':
            logger.info('Deleting files from sub-directory %s', fullpath)

            delete_old_files(fullpath, fn_pattern, num_days, subdir)

    return

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_cksum']
    purge_dir = "/xfero/transient"
    num_days = '20'
    pattern = '^.*'
    delete_old_files(purge_dir, pattern, num_days, 'True')
