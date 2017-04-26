#!/usr/bin/env python
'''

**Purpose:**

The xfer thread retrieve items of work from the Output Priority Queue and
initiates file transfers to the sites specified in the XFERO_Xfer table.

A xfer thread will read from the Output Queue in Priority Order with 1 being
High and therefore processed first and 999 being low and processed last.

The xfer threads have been cast so as to make interactions easy.

The work retrieved from the output queue contains the following items:

+--------------------------+---------------------------------------------------+
| Item                     | Description                                       |
+==========================+===================================================+
| Priority                 | The priority assigned to the route                |
+--------------------------+---------------------------------------------------+
| Route ID                 | Route ID from the XFERO_Route table                  |
+--------------------------+---------------------------------------------------+
| File Name                | Working file name                                 |
+--------------------------+---------------------------------------------------+
| Original File Name       | Original file name                                |
+--------------------------+---------------------------------------------------+
| XFERO Token                 | Unique logging token                              |
+--------------------------+---------------------------------------------------+

**Usage Notes:**

The xfer thread will poll the Output Queue until it receives a None record,
indicating that there is no further work to be done. At which point the xfer
thread will terminate.

*Example usage:*

```x = Xfer_Thread(outq)```
```x.start()```

:param outq: Output queue where this process places work to be handles by xfer
threads

**Unit Test Module:** None

**Process Flow**

.. figure::  ../process_flow/xfer.png
   :align:   center

   Process Flow: Xfer

+------------+-------------+----------------------------------------------------+
| Date       | Author      | Change Details                                     |
+============+=============+====================================================+
| 04/05/2014 | Chris Falck | Created                                            |
+------------+-------------+----------------------------------------------------+
| 10/05/2014 | Chris Falck | Modified function join_xfer_partner to ensure that |
|            |             | connections to the database are opened and closed  |
|            |             | within the function call. This enables the function|
|            |             | to be called in a multiprocessing environment      |
+------------+-------------+----------------------------------------------------+
| 12/05/2014 | Chris Falck | Added new column to XFERO_Xfer table. Added the new   |
|            |             | column from int variable self.delsrc into process  |
|            |             | Value is used in run method to determine if the    |
|            |             | source file should be deleted.                     |
+------------+-------------+----------------------------------------------------+
| 12/05/2014 | Chris Falck | New element passed on queue 'xfero_token'. Used in    |
|            |             | Logging.                                           |
+------------+-------------+----------------------------------------------------+
| 24/09/2014 | Chris Falck | Added retrieval of error_directory from the config |
|            |             | file. This is used to hold files that have failed  |
|            |             | during workflow or transfer processing.            |
|            |             | Also added functionality to move files that have   |
|            |             | failed to the error_directory                      |
+------------+-------------+----------------------------------------------------+
| 25/02/2015 | Chris Falck | Modified class to send from transient directory    |
|            |             | rather than make copies of the file into processing|
|            |             | directory.
+------------+-------------+----------------------------------------------------+

'''
# identity = lambda x: x

import threading
import sys
import os
import shutil
import shlex
import subprocess
import logging.config
import xfero.get_conf as get_conf
from xfero.db import manage_xfer as db_xfer
from xfero.workflow_manager.copy_file import Copy_File

try:
    (xfero_logger,.xfero_database, outbound_directory, transient_directory,
     error_directory, xfero_pid) = get_conf.get.xfero_config()
except Exception as err:
    print('Cannot get XFERO Config: %s' % err)
    raise err

logging.config.fileConfig(xfero_logger)

# create logger
logger = logging.getLogger('xfer')


class Xfer_Thread(threading.Thread):

    def __init__(self, q, outbound_directory, *args, **kw):
        """Initialize process and save queue reference."""
        threading.Thread.__init__(self, *args, **kw)

        self.queue = q  # Output queue
        self.outbound_directory = outbound_directory
        self.prefix = 'xfero_'
        self.output = []  # create list for output
        self.filename = ''
        self.original_filename = ''
        self.priority = ''
        self.sendfile = ''
        self.delsrc = 'No'
        self.subproc_return = 0

    def run(self):

        logging.config.fileConfig(xfero_logger)
        # create logger
        logger = logging.getLogger('xfer')

        # while not self.queue.empty():

        #    print('in xfer loop')
        #    logger.debug('%s - Dequeue xfer from queue' % self.name)

        #    try:
        # work = self.queue.get_nowait() # Get work item from queue
        #    except self.iq.Empty:
        #        pass
        #    else:
        #        logger.debug('%s - Xfer retrieved' % self.name)

        while True:
            print('in xfer loop')
            logger.debug('%s - Dequeue xfer from queue' % self.name)
            work = self.queue.get()  # Get work item from queue
            logger.debug('%s - Xfer retrieved' % self.name)

            if len(work) == 2:  # If no further work to process
                logger.debug('%s has no further work to do.' % self.name)
                logger.debug('%s - DONE' % self.name)
                self.queue.task_done()
                break

            self.priority, route_id, self.filename, self.original_filename, self.xfero_token = work

            try:
                # this is the "work"
                result = (self.xfer_process(route_id, self.filename))
                logger.debug(
                    '%s - Result of xfer_process: %s. (XFERO_Token=%s)' % (self.name, result, self.xfero_token))

                if result == 0:

                    self.queue.task_done()

                    if self.delsrc == 'Yes':
                        # Delete self.filename
                        try:
                            os.remove(self.filename)
                        except (OSError, IOError) as e:
                            logger.warning("%s - Exception deleting transferred source file %s exception: %s. (XFERO_Token=%s)" % (
                                self.name, self.filename, e, self.xfero_token))

                    if os.path.isfile(self.sendfile):
                        try:
                            os.remove(self.sendfile)
                        except (OSError, IOError) as e:
                            logger.warning(
                                "%s - Delete file %s exception: %s. (XFERO_Token=%s)" % (self.name, self.sendfile, e, self.xfero_token))

                else:
                    logger.error(
                        '%s - Error in thread: Error %s. (XFERO_Token=%s)' % (self.name, result, self.xfero_token))
                    logger.error('%s - Exception: Original file name: %s. (XFERO_Token=%s)' %
                                 (self.name, self.original_filename, self.xfero_token))
                    logger.error('%s - Exception: Current file name: %s. (XFERO_Token=%s)' %
                                 (self.name, self.sendfile, self.xfero_token))

                    self.queue.task_done()

                    args = (self.sendfile, error_directory)

                    try:
                        obj = Copy_File()
                        print(obj.move_file(*args))
                    except Exception as err:
                        logger.error('%s - Exception moving file from %s to %s: Error %s. (XFERO_Token=%s)' % (
                            self.name, self.sendfile, error_directory, err, self.xfero_token), exc_info=True)

            except Exception as err:
                logger.error('%s - Error in thread: Error %s. (XFERO_Token=%s)' %
                             (self.name, err, self.xfero_token), exc_info=True)
                logger.error('%s - Exception: Original file name: %s. (XFERO_Token=%s)' %
                             (self.name, self.original_filename, self.xfero_token))
                logger.error('%s - Exception: Current file name: %s. (XFERO_Token=%s)' %
                             (self.name, self.filename, self.xfero_token))
                # Move to error dir
                logger.error('%s - Exception: Moving %s to %s. (XFERO_Token=%s)' %
                             (self.name, self.filename, error_directory, self.xfero_token))

                args = (self.filename, error_directory)

                try:
                    obj = Copy_File()
                    print(obj.move_file(*args))
                except Exception as err:
                    logger.error('%s - Exception moving file from %s to %s: Error %s. (XFERO_Token=%s)' % (
                        self.name, self.filename, error_directory, err, self.xfero_token), exc_info=True)

                self.queue.task_done()
                # raise err

        sys.stdout.flush()
        # print('Xfer Terminating')

    def xfer_process(self, route_id, filename):

        logging.config.fileConfig(xfero_logger)
        # create logger
        logger = logging.getLogger('xfer')

        logger.info('%s - Performing Xfer on file %s. (XFERO_Token=%s)' %
                    (self.name, filename, self.xfero_token))

        try:
            logger.debug(
                'db_xfer.join_xfer_partner: %s. (XFERO_Token=%s)' % (route_id, self.xfero_token))
            x_rows = db_xfer.join_xfer_partner(str(route_id), self.xfero_token)

        except Exception as err:
            logger.error('%s - Exception while retrieving xfer: Error %s. (XFERO_Token=%s)' %
                         (self.name, err, self.xfero_token), exc_info=True)
            raise err

        if not x_rows:
            logger.info('%s - No xfer to perform. (XFERO_Token=%s)' %
                        (self.name, self.xfero_token))
            return 'nothing_to_xfer'

        logger.info('%s - Perform xfer. (XFERO_Token=%s)' %
                    (self.name, self.xfero_token))

        #20150225 - rename self.filename to prefix filename
        path, filename_no_path = os.path.split(filename)
        prefix_file = self.prefix + filename_no_path

        try:
            rename_func = Copy_File()
            self.sendfile = rename_func.rename_file(
                            filename,
                            path +
                            os.sep +
                            prefix_file)
        except Exception as err:
            logger.error(
                    'Rename File %s to %s. Error: %s (XFERO_Token=%s)',
                    filename, prefix_file, err, self.xfero_token)
            raise err

        for row in x_rows:
            xfer_id = row['xfer_id']
            xfer_route = row['xfer_route']
            xfer_cotspattern = row['xfer_cotspattern']
            xfer_partner = row['xfer_partner']
            xfer_cmd = row['xfer_cmd']
            xfer_params = row['xfer_params']
            self.delsrc = row['xfer_delsrc']
            partner_service_name = row['partner_service_name']

            # 20150225 - decided not to create a copy files into processing
            # instead send to all targets from transient directory
            #send_dir = self.outbound_directory + os.sep + partner_service_name
            #p, filename_no_path = os.path.split(filename)
            #self.send_file = send_dir + os.sep + self.prefix + filename_no_path

            # Do create directory in try except
            #try:
            #    os.stat(send_dir)
            #except:
            #    os.makedirs(send_dir)

            #logger.info('%s - Copy file to target output directory: %s to %s. (XFERO_Token=%s)' %
            #            (self.name, filename, self.send_file, self.xfero_token))

            #try:
            #    shutil.copy(filename, self.send_file)
            #except OSError as err:
            #    logger.error('%s - Unable to copy file from %s to %s: %s. (XFERO_Token=%s)' %
            #                 (self.name, filename, self.send_file, err, self.xfero_token))
            #    # self.queue.task_done()
            #    raise err

            # Construct send command for the transfer subprocess
            # Will need to add the file name to the xfer params passed to the subprocess to add the send file name
            # Things to replace from xfer_params = {File_to_Send_with_Path} ,
            # {Remote_File_Name_No_Path}, {Remote_File_Name_With_Path}

            #prefix_file = self.prefix + filename_no_path
            #20150225 - rename self.filename to prefix filename


            # 20150225 replaced with line below
            #params = xfer_params.replace(
            #    '{File_to_Send_with_Path}', self.send_file)
            params = xfer_params.replace(
                '{File_to_Send_with_Path}', self.sendfile)
            ############# only works for FTP ############### Ibelieve this should work now we can specify target directory in the GUI !!!!!!!!!!!!!!!!!
            xfer_params = params.replace(
                '{Remote_File_Name}', filename_no_path)
            params = xfer_params.replace('{Prefix_File_Name}', prefix_file)
            ############# only works for FTP ###############
            cmd = xfer_cmd + ' ' + params
            # Added cmd.replace in shlex below to accommodate issues with
            # windows file paths in shlex
            args = shlex.split(cmd.replace('\\', '\\\\'))

            logger.debug('%s - Shlex arguments = %s. (XFERO_Token=%s)' %
                         (self.name, args, self.xfero_token))

            if xfer_cmd == 'curl':
                try:
                    logger.info(
                        '%s - Performing Transfer: %s. (XFERO_Token=%s)' % (self.name, args, self.xfero_token))

                    popen = subprocess.Popen(
                        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    p_stdout, p_stderr = popen.communicate()
                    # XFERS.append(popen)
                    print(p_stdout)
                    print(p_stderr)
                    print(args)
                    logger_stats = logging.getLogger('ftstats')
                    logger_stats.info(
                        "%s - Transfer initiated: %s. (XFERO_Token=%s)" % (self.name, cmd, self.xfero_token))
                    try:
                        #20150225 - modified line below
                        #sz = os.path.getsize(self.send_file)
                        sz = os.path.getsize(self.sendfile)
                        logger_stats.info(
                            "%s - File: %s is %s bytes. (XFERO_Token=%s)" % (self.name, self.sendfile, sz, self.xfero_token))
                    except OSError as e:
                        logger_stats.error(
                            "%s - Can not get size of the file: %s. (XFERO_Token=%s)" % (self.name, self.sendfile, self.xfero_token))

                    logger = logging.getLogger('xfer')
                    logger.info(
                        '%s - Transfer initiated: %s. (XFERO_Token=%s)' % (self.name, cmd, self.xfero_token))
                    logger.info('%s - Subprocess: %s. (XFERO_Token=%s)' %
                                (self.name, p_stdout, self.xfero_token))
                    logger.info('%s - Subprocess: %s. (XFERO_Token=%s)' %
                                (self.name, p_stderr, self.xfero_token))

                    if (popen.returncode != 0):
                        logger.error('%s - Transfer Failed RC: %s. (XFERO_Token=%s)' %
                                     (self.name, popen.returncode, self.xfero_token))
                        logger.error('%s - Failed to send file: %s. (XFERO_Token=%s)' %
                                     (self.name, self.sendfile, self.xfero_token))

                        self.subproc_return = self.subproc_return + \
                            popen.returncode

                        #20150225 - # Delete self.sendfile
                        #try:
                        #    os.remove(self.send_file)
                        #except (OSError, IOError) as e:
                        #    logger.warning("%s - Exception deleting transferred source file %s exception: %s. (XFERO_Token=%s)" % (
                        #        self.name, self.send_file, e, self.xfero_token))

                    else:
                        logger.info('%s - Transfer Successful: %s. (XFERO_Token=%s)' %
                                    (self.name, popen.returncode, self.xfero_token))
                        logger.info('%s - Successfully sent file: %s. (XFERO_Token=%s)' %
                                    (self.name, self.sendfile, self.xfero_token))
                        #20150225 - # Delete self.sendfile
                        #try:
                        #    os.remove(self.send_file)
                        #except (OSError, IOError) as e:
                        #    logger.warning("%s - Exception deleting transferred source file %s exception: %s. (XFERO_Token=%s)" % (
                        #        self.name, self.send_file, e, self.xfero_token))

                except Exception as err:
                    logger.error('%s - Unable to call subprocess %s to %s: Error %s. (XFERO_Token=%s)' %
                                 (self.name, xfer_cmd, params, err, self.xfero_token), exc_info=True)
                    #20150225 - # Delete self.sendfile
                    #try:
                    #    os.remove(self.send_file)
                    #except (OSError, IOError) as e:
                    #    logger.warning("%s - Exception deleting transferred source file %s exception: %s. (XFERO_Token=%s)" % (
                    #        self.name, self.send_file, e, self.xfero_token))

                    raise err
            else:
                print('Calling %s' % cmd)
                os.system(cmd)

        #if os.path.isfile(self.sendfile):
        #    try:
        #        os.remove(self.sendfile)
        #    except (OSError, IOError) as e:
        #        logger.warning("%s - Delete file %s exception: %s. (XFERO_Token=%s)" %
        #        (self.name, self.sendfile, e, self.xfero_token))

        return self.subproc_return
