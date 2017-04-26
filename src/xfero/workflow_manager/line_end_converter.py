#!/usr/bin/env python
'''Line End Conversion'''
import logging.config
import os
from /xfero/ import get_conf as get_conf

try:
    (xfero_logger,.xfero_database, outbound_directory, transient_directory,
     error_directory, xfero_pid) = get_conf.get.xfero_config()
except Exception as err:
    print('Cannot get XFERO Config: %s' % err)
    raise err

logging.config.fileConfig(xfero_logger)
# create logger
logger = logging.getLogger('line_end_converter')


class Line_End_Converter(object):

    '''

    **Purpose:**

    The Line_End_Converter class provides methods to convert the line end
    convention of the file.
    If a file is transferred in TEXT format line end conversion between windows
    & unix will be performed by the file transfer mechanism. However, if the
    file is transferred in BINARY format, either as part of a ZIP or TAR.GZ,
    line end conversion will not be possible.
    This class has been provided to perform this conversion where required.

    **Usage Notes:**

    PyDevPackage: file_manager
    Dir Structure - src/file_manager/

    import file_manager.line_end_converter as c
    fn = '/home/gby9ajbl/Documents/test.txt'
    obj = c.Line_End_Converter(fn)
    d2u= obj.dos2unix()


    *Example usage:*

    ```obj = file_manager.line_end_converter.Line_End_Converter(fn)```
    ```d2u= obj.dos2unix()```

    :param filename: Original filename
    :returns: The converted filename or raises an Exception

    **Unit Test Module:** test_line_end_converter.py

    **Process Flow**

    .. figure::  ../process_flow/line_end_converter.png
       :align:   center

       Process Flow: Line End Converter

    *External dependencies*

    os (/xfero/.workflow_manager.line_end_converter)
    /xfero/
      get_conf (/xfero/.workflow_manager.line_end_converter)

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
        logger.debug('Object initialised: Line_End_Converter')
        self.xfero_token =.xfero_token
        self.filename = ''
        self.newline = None
        self.retv = None
        self.filepath = None

    def dos2unix(self, filename):
        '''dos2unix conversion'''
        self.filename = filename
        self.retv = filename
        self.newline = '\n'

        logger.info('Converting dos file to unix: %s. (XFERO_Token=%s)',
                    self.filename, self.xfero_token)

        try:
            self.convert()
            return self.retv
        except Exception as err:
            raise err

    def unix2dos(self, filename):
        '''unix2dos conversion'''
        self.filename = filename
        self.retv = filename
        self.newline = '\r\n'

        logger.info('Converting unix to dos file: %s. (XFERO_Token=%s)',
                    self.filename, self.xfero_token)

        try:
            self.convert()
            return self.retv
        except Exception as err:
            raise err

    def convert(self):
        '''Conversion method'''
        if os.path.isdir(self.filename):

            for filen in os.listdir(self.filename):

                try:
                    self.filecontents = open(
                        os.path.join(self.filename, filen), "r").read()
                except:
                    logger.error('FileNotFoundError: [Errno 2] No such file or \
                    directory: %s. (XFERO_Token=%s)', os.path.join(self.filename,
                                                                filen),
                                 self.xfero_token)
                    raise IOError('Error opening file: %s. (XFERO_Token=%s)' % (
                        os.path.join(self.filename, filen), self.xfero_token))

                self.filepath = os.path.join(self.filename, filen)

                try:
                    self.process()
                except:
                    raise
        else:
            try:
                self.filecontents = open(self.filename, "r").read()
            except:
                logger.error('FileNotFoundError: [Errno 2] No such file or \
                directory: %s. (XFERO_Token=%s)', self.filename, self.xfero_token)
                raise IOError(
                    'Error opening file: %s. \
                    (XFERO_Token=%s)' % (self.filename, self.xfero_token))

            self.filepath = self.filename

            try:
                self.process()
            except:
                raise

    def process(self):
        '''Process method'''
        try:
            filen = open(self.filepath, "w", newline=self.newline)
        except IOError:
            logger.error('IOError opening file %s. (XFERO_Token=%s)',
                         self.filepath, self.xfero_token)
            raise IOError('Error opening file %s. (XFERO_Token=%s)' %
                          (self.filepath, self.xfero_token))

        try:
            filen.write(self.filecontents)
            filen.close()
        except IOError:
            logger.error('IOError writing file %s. (XFERO_Token=%s)',
                         self.filepath, self.xfero_token)
            raise IOError('Error writing file %s. (XFERO_Token=%s)' %
                          (self.filepath, self.xfero_token))

if __name__ == "__main__":

    fname = '/ftran/dos.txt'
    try:
        obj = Line_End_Converter()
        try:
            print(obj.dos2unix(fname))
        except Exception as err:
            print('Caught an exception: %s' % err)
            # Here we would continue processing other files in the loop with
            # the continue statement

    except Exception as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement

    fname = '/ftran/unix.txt'
    try:
        obj = Line_End_Converter()
        try:
            print(obj.unix2dos(fname))
        except Exception as err:
            print('Caught an exception: %s' % err)
            # Here we would continue processing other files in the loop with
            # the continue statement
    except Exception as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement

    fname = '/ftran/conv'
    try:
        obj = Line_End_Converter()
        try:
            print(obj.unix2dos(fname))
        except Exception as err:
            print('Caught an exception: %s' % err)
            # Here we would continue processing other files in the loop with
            # the continue statement
    except Exception as err:
        print('Caught an exception: %s' % err)
        # Here we would continue processing other files in the loop with the
        # continue statement
