#!/usr/bin/env python
'''Manage Archives'''
import logging.config
import os
import shutil
import zipfile
import tarfile
import datetime
from /xfero/ import get_conf as get_conf

try:
    (xfero_logger,.xfero_database, outbound_directory, transient_directory,
     error_directory, xfero_pid) = get_conf.get.xfero_config()
except Exception as err:
    print('Cannot get XFERO Config: %s' % err)
    raise err

logging.config.fileConfig(xfero_logger)
# create logger
logger = logging.getLogger('manage_archives')

class Manage_Archives(object):

    '''

    **Purpose:**

    The :class:`manage_archives.Manage_Archives` class manages file archives. It
    provides methods to create archive files or extract files from an existing
    archive.

    *Archive Creation*

    Archives are created in either tar.gz or zip format.

    There are 2 methods for Archive creation. These are ``compress_file`` and
    ``compress_dir``

    The file or files contained in the directory passed into this class is
    included in the Archive at the root level. So a file called
    ``/tmp/chris/mytext.txt`` will be added to the archive as ``/mytext.txt``.

    The compress methods always look for a sum file which matches the file name
    or directory name with a ``.sum`` extension to include in the archive but if
    one is not found the archive is still produced without the sum file.

    *Archive Extraction*

    Archives in either tar.gz or zip format can be extracted.

    Extracted files will be placed in the directory passed to the method.

    *Usage Notes:*

    The parameter args will hold the following parameters:

    * filename or directory name - A file or directory of files to include in
    the archive.
    * self.archive_type - The type of archive to be created.
      * Accepted values = .tar.gz or .zip.

    *Example usage:*

    For an individual file:

    ```obj = Compress_Object()```
    ```obj.compress_file(args)```

    For a directory of files:

    ```obj = Compress_Object()```
    ```obj.compress_dir(args)```


    :param args: string containing a comma separated list of parameters to the
    compress_file function
    :returns: archive_name: The name of the archive produced or raises an
    Exception

    **Unit Test Module:** test_compress_file.py

    **Process Flow**

    .. figure::  ../process_flow/manage_archives.png
       :align:   center

       Process Flow: Manage Archives

    *External dependencies*

    os (/xfero/.workflow_manager.manage_archives)
    shutil (/xfero/.workflow_manager.manage_archives)
    tarfile (/xfero/.workflow_manager.manage_archives)
    /xfero/
      get_conf (/xfero/.workflow_manager.manage_archives)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/07/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 02/04/2014 | Chris Falck | Converted to Object Orientation class         |
    |            |             | Added compress_dir method                     |
    +------------+-------------+-----------------------------------------------+
    | 27/10/2014 | Chris Falck | modified call to get_conf                     |
    +------------+-------------+-----------------------------------------------+
    | 30/10/2014 | Chris Falck | Added functionality to methods compress_file  |
    |            |             | and compress_dir to delete either the file or |
    |            |             | the directory provided it has been Archived.  |
    +------------+-------------+-----------------------------------------------+
    '''

    def __init__(self, xfero_token):
        '''init'''
        logger.debug('Object initialised: Manage_Archives')
        self.xfero_token =.xfero_token
        self.filename = ''

    def compress_file(self, filename, archive_type):
        '''compress file'''
        self.filename = filename
        self.archive_type = archive_type

        logger.info('Compress File: %s. (XFERO_Token=%s)',
                    self.filename, self.xfero_token)

        # Validate input - Check from_name exists
        if os.path.isfile(self.filename) is False:
            logger.error('OSError No such file or directory: %s. \
            (XFERO_Token=%s)', self.filename, self.xfero_token)
            raise OSError(2, 'No such file or directory: %s. \
            (XFERO_Token=%s)' % (self.filename, self.xfero_token))

        # Determine if a zip or a tar.gz is required
        logger.debug('Determine if a .zip or a .tar.gz is required: Type: %s. \
        (XFERO_Token=%s)', self.archive_type, self.xfero_token)

        if self.archive_type == "tar.gz" or self.archive_type == ".tar.gz":
            logger.info('Archive Type is .tar.gz. (XFERO_Token=%s)', self.xfero_token)
            archive_name = self.filename + ".tar.gz"

            # Create Archive
            logger.info('Create Archive %s. (XFERO_Token=%s)', archive_name,
                        self.xfero_token)
            atar = tarfile.open(archive_name, "w:gz")

        elif self.archive_type == "zip" or self.archive_type == ".zip":
            logger.info('Archive Type is .zip. (XFERO_Token=%s)', self.xfero_token)
            archive_name = self.filename + ".zip"

            # Create Archive
            logger.info('Create Archive %s. (XFERO_Token=%s)', archive_name,
                        self.xfero_token)
            azip = zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED)

        else:
            logger.error('TypeError: Invalid Archive Type supplied: %s. \
            (XFERO_Token=%s)', self.archive_type, self.xfero_token)
            return 'stop'

        # Check if there is a matching sum file
        sumfile = self.filename + '.sum'

        path, filen = os.path.split(self.filename)

        logger.info('Write %s to archive %s. (XFERO_Token=%s)',
                    self.filename, archive_name, self.xfero_token)

        if self.archive_type == "zip" or self.archive_type == ".zip":
            azip.write(self.filename, filen)
            if os.path.isfile(sumfile):
                path, filen = os.path.split(sumfile)
                azip.write(sumfile, filen)
            azip.close()
        else:
            atar.add(self.filename, filen)
            if os.path.isfile(sumfile):
                path, filen = os.path.split(sumfile)
                atar.add(sumfile, filen)
            atar.close()
        # Close the Archive
        logger.info("Close the Archive. (XFERO_Token=%s)", self.xfero_token)

        # Archive created successfully - delete the file and return the archive
        # name
        try:
            os.remove(self.filename)
        except OSError:
            logger.warning('Unable to delete the file %s following successful \
            archive creation. (XFERO_Token=%s)', self.filename, self.xfero_token)

        if os.path.isfile(sumfile):
            try:
                os.remove(sumfile)
            except OSError:
                logger.warning('Unable to delete the file %s following \
                successful archive creation. (XFERO_Token=%s)', sumfile,
                               self.xfero_token)

        return archive_name

    def compress_dir(self, dirname, archive_type, archive_name):
        '''compress dire'''
        self.dirname = dirname
        self.archive_type = archive_type
        self.archive_name = archive_name

        # Make sure that there is no trailing separator on directory
        self.dirname = self.dirname.rstrip(os.sep)
        self.basedir, filen = os.path.split(self.dirname)

        logger.info('Compress Directory: %s. (XFERO_Token=%s)', self.dirname,
                    self.xfero_token)

        # Validate input - Check from_name exists
        if os.path.isdir(self.dirname) is False:
            logger.error('OSError No such file or directory: %s. \
            (XFERO_Token=%s)', self.dirname, self.xfero_token)
            raise OSError(2, 'No such file or directory: %s. (XFERO_Token=%s)' % (
                self.dirname, self.xfero_token))

        # Create timestamp
        now = datetime.datetime.now()
        tstamp = now.strftime("%Y%m%dT%H%M%S")

        # Determine if a zip or a tar.gz is required
        logger.debug(
            'Determine if a .zip or a .tar.gz is required. \
            (XFERO_Token=%s)', self.xfero_token)

        if self.archive_type == "tar.gz" or self.archive_type == ".tar.gz":
            logger.info('Archive Type is .tar.gz - Type %s. \
            (XFERO_Token=%s)', self.archive_type, self.xfero_token)
            self.ts_archive_name = self.basedir + os.sep + \
                self.archive_name + '_' + tstamp + ".tar.gz"

            # Create Archive
            logger.info('Create Archive %s. (XFERO_Token=%s)',
                        self.ts_archive_name, self.xfero_token)
            atar = tarfile.open(self.ts_archive_name, "w:gz")

        elif self.archive_type == "zip" or self.archive_type == ".zip":
            logger.info('Archive Type is .zip - Type %s. (XFERO_Token=%s)',
                        self.archive_type, self.xfero_token)
            self.ts_archive_name = self.basedir + os.sep + \
                self.archive_name + '_' + tstamp + ".zip"

            # Create Archive
            logger.info('Create Archive %s. (XFERO_Token=%s)',
                        self.ts_archive_name, self.xfero_token)
            azip = zipfile.ZipFile(
                self.ts_archive_name, 'w', zipfile.ZIP_DEFLATED)

        else:
            logger.error('TypeError: Invalid Archive Type supplied: %s. \
            (XFERO_Token=%s)', self.archive_type, self.xfero_token)
            raise TypeError(2, 'Invalid Archive Type supplied %s. \
            (XFERO_Token=%s)' % (self.archive_type, self.xfero_token))

        logger.info('Write %s to archive %s. (XFERO_Token=%s)', self.dirname,
                    self.ts_archive_name, self.xfero_token)

        if self.archive_type == "zip" or self.archive_type == ".zip":

            for filename in os.listdir(self.dirname):

                if os.path.isfile(self.dirname + os.sep + filename):
                    azip.write(self.dirname + os.sep + filename, filename)

            azip.close()
        else:

            for filename in os.listdir(self.dirname):

                if os.path.isfile(self.dirname + os.sep + filename):
                    atar.add(self.dirname + os.sep + filename, filename)

            atar.close()
        # Delete the directory
        try:
            shutil.rmtree(self.dirname)
        except shutil.Error as err:
            logger.warning('Unable to delete Directory tree %s following \
            successful archive creation: Error %s. (XFERO_Token=%s)',
                           self.dirname, err, self.xfero_token)
        # eg. source or destination doesn't exist
        except IOError as err:
            logger.warning('Unable to delete Directory tree %s following \
            successful archive creation: Error %s. (XFERO_Token=%s)', self.dirname,
                           err.strerror, self.xfero_token)

        return self.ts_archive_name

    def extract(self, filename, to_path):
        '''extract'''
        self.filename = filename
        self.to_path = to_path

        # Validate input - Check from_name exists
        if os.path.isfile(self.filename) is False:
            logger.error('OSError No such file or directory: %s. \
            (XFERO_Token=%s)', self.filename, self.xfero_token)
            raise OSError(2, 'No such file or directory %s. (XFERO_Token=%s)' % (
                self.filename, self.xfero_token))

        if not os.path.exists(self.to_path):
            try:
                os.makedirs(self.to_path)
            except OSError:
                raise OSError(2, 'Unable to create directory %s. \
                (XFERO_Token=%s)' % (self.to_path, self.xfero_token))

        # Determine if a zip or a tar.gz is required
        logger.debug(
            'Determine if a .zip or a .tar.gz is required. \
            (XFERO_Token=%s)', self.xfero_token)

        if self.filename.endswith('.zip'):
            opener, mode = zipfile.ZipFile, 'r'
        elif self.filename.endswith('.tar.gz') or \
        self.filename.endswith('.tgz'):
            opener, mode = tarfile.open, 'r:gz'
        else:
            raise ValueError('Could not extract file as no appropriate \
            extractor is found: %s. (XFERO_Token=%s)' % (self.filename,
                                                      self.xfero_token))

        try:
            file = opener(self.filename, mode)
            try:
                logger.info('Extracting file %s. (XFERO_Token=%s)', self.filename,
                            self.xfero_token)
                try:
                    file.extractall(self.to_path)
                except Exception as err:
                    raise err
            finally:
                file.close()
                os.remove(self.filename)
        except Exception as err:
            raise ValueError(
                'Can not open archive file: %s. \
                (XFERO_Token=%s)' % (self.filename, self.xfero_token))

        return self.to_path

if __name__ == "__main__":
    '''
    file_name = '/xfero/WIN1/win1_archive'
    args = (file_name, '.tar.gz')

    try:
        obj = Manage_Archives('test')
        print(obj.compress_file(*args))
    except Exception as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement

    dir_name = '/Users/chrisfalck/Documents/test_folder'
    args = (dir_name, '.zip', 'my-archive')

    try:
        obj = Manage_Archives('test')
        print(obj.compress_dir(*args))
    except Exception as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement

    '''
    file_name = '/Users/chrisfalck/Documents/renamed-test2.zip'
    to_path = '/Users/chrisfalck/Documents/renamed/'
    args = (file_name, to_path)

    try:
        obj = Manage_Archives('test')
        print(obj.extract(*args))
    except Exception as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement
