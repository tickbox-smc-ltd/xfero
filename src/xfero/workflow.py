#!/usr/bin/env python
'''
Workflow Thread
'''

from threading import Thread
import sys
import os
import socket
import logging.config
from xfero import get_conf as get_conf
from xfero.workflow_manager.copy_file import Copy_File
from xfero.workflow_manager.av_check import Anti_Virus
from xfero.workflow_manager.case_converter import Case_Converter
from xfero.workflow_manager.checksum import Checksum
from xfero.workflow_manager.crypt import Crypt
from xfero.workflow_manager.exit import Exit
from xfero.workflow_manager.line_end_converter \
import Line_End_Converter
from xfero.workflow_manager.manage_archives import Manage_Archives
from xfero.workflow_manager.split_file import Split_File
from xfero.workflow_manager.transform_filename \
import Transform_Filename
from xfero.db import manage_workflow as db_workflow

try:
    (xfero_logger,
     xfero_database,
     outbound_directory,
     transient_directory,
     error_directory,
     xfero_pid) = get_conf.get.xfero_config()
except Exception as err:
    print('Cannot get XFERO Config: %s' % err)
    raise err

logging.config.fileConfig(xfero_logger)
# create logger
logger = logging.getLogger('workflow')


class Workflow_Thread(Thread):

    '''

    **Purpose:**

    The workflow thread retrieve items of work from the Input Priority Queue and
    having performed the workflow, it puts the work to the Output Priority Queue

    A workflow thread will read from the Input Queue in Priority Order with 1
    being High and therefore processed first and 999 being low and processed
    last.

    The workflow threads have been cast so as to make interactions easy.

    The work retrieved from the input queue contains the following items:

    +--------------------------+-----------------------------------------------+
    | Item                     | Description                                   |
    +==========================+===============================================+
    | Priority                 | The priority assigned to the route            |
    +--------------------------+-----------------------------------------------+
    | Route ID                 | Route ID from the XFERO_Route table              |
    +--------------------------+-----------------------------------------------+
    | File Name                | Working file name                             |
    +--------------------------+-----------------------------------------------+
    | Original File Name       | Original file name                            |
    +--------------------------+-----------------------------------------------+
    | XFERO Token                 | Unique logging token                          |
    +--------------------------+-----------------------------------------------+

    **Usage Notes:**

    The workflow thread will poll the Input Queue until it receivs a None
    record, indicating that there is no further work to be done. At which point
    the workflow thread will terminate.

    *Example usage:*

    ```w = Workflow_Thread(inq, outq)```
    ```w.start()```

    :param inq: Input queue delivers work to this process
    :param outq: Output queue where this process places work to be handles by
                 xfer threads

    **Unit Test Module:** None

    **Process Flow**

    .. figure::  ../process_flow/workflow.png
       :align:   center

       Process Flow: Workflow

    External dependencies

    os (xfero.workflow)
    xfero
      db
          manage_workflow (xfero.workflow)
      get_conf (xfero.workflow)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 04/05/2014 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 12/05/2014 | Chris Falck | New element passed on queue 'xfero_token'. For   |
    |            |             | Logging.                                      |
    +------------+-------------+-----------------------------------------------+
    | 24/09/2014 | Chris Falck | Added retrieval of error_directory from the   |
    |            |             | config file. This is used to hold files that  |
    |            |             | have failed in workflow or transfer processing|
    +------------+-------------+-----------------------------------------------+
    '''

    def __init__(self, iq, oq, *args, **kw):
        logger.debug('Initialize workflow process and save Queue references.')
        Thread.__init__(self, *args, **kw)
        self.inputq, self.outputq = iq, oq
        self.original_filename = ''
        self.transient_filename = ''
        self.working_filename = ''
        self.priority = ''
        self.done = (999, 'NONE')

    def run(self):

        logging.config.fileConfig(xfero_logger)
        # create logger
        logger = logging.getLogger('workflow')

        while True:
            print('in workflow loop')
            logger.debug('%s - Dequeue workflow from queue', self.name)
            work = self.inputq.get()  # Get work item from queue by priority

            logger.debug('%s - Workflow retrieved', self.name)

            if len(work) == 2:  # If no further work to process
                logger.debug(
                    '%s has no further work. Enqueue None on output queue',
                    self.name)
                print('None to outq worker')
                self.outputq.put(self.done)  # Enqueue None on output queue
                logger.debug('%s - DONE', self.name)
                self.inputq.task_done()
                break

            self.priority, route_id, filename, self.original_filename, \
            self.xfero_token = work
            self.transient_filename = filename

            try:
                self.working_filename = (
                    self.workflow_process(
                        route_id,
                        filename))  # this is the "work"

                logger.info(
                    '%s - Get result from workflow_process. (XFERO_Token=%s)',
                    self.name, self.xfero_token)
                logger.info(
                    '%s - Enqueue result to output queue. (XFERO_Token=%s)',
                    self.name, self.xfero_token)

                if self.working_filename is None or \
                    self.working_filename == 'success':
                    logger.debug(
                        'Enqueue None : Result %s. (XFERO_Token=%s)',
                        self.working_filename, self.xfero_token)
                    print('None to outq worker')
                    self.outputq.put(self.done)
                    self.inputq.task_done()
                    logger.info(
                        '%s - DONE. (XFERO_Token=%s)',
                        self.name, self.xfero_token)
                else:
                    # print(route_id, result, self.xfero_token)
                    work = (
                        self.priority,
                        route_id,
                        self.working_filename,
                        self.original_filename,
                        self.xfero_token)
                    logger.debug(
                        'Enqueue Work %s. (XFERO_Token=%s)',
                        work, self.xfero_token)
                    # Enqueue result which is route_id & modified filename
                    self.outputq.put(work)
                    self.inputq.task_done()
                    logger.info(
                        '%s - DONE. (XFERO_Token=%s)',
                        self.name, self.xfero_token)

            except Exception as err:
                logger.error(
                    '%s - Error in thread: Error %s. (XFERO_Token=%s)',
                    self.name, err, self.xfero_token, exc_info=True)
                self.inputq.task_done()
                # raise err
        # self.outputq.join()
        # print('joined outq')
        sys.stdout.flush()
        # print('Workflow Terminating')
        return

    def workflow_process(self, route_id, filename):
        '''
        Workflow processing
        '''

        logging.config.fileConfig(xfero_logger)
        # create logger
        logger = logging.getLogger('workflow')

        logger.info(
            '%s - Checking if workflow processing required on file %s. \
            (XFERO_Token=%s)', self.name, filename, self.xfero_token)

        try:
            logger.debug(
                'db_workflow.list_XFERO_Workflow_Item_OrderBy_Run_Order_monitor: \
                %s. (XFERO_Token=%s)', route_id, self.xfero_token)
            wf_rows = \
            db_workflow.list_XFERO_Workflow_Item_OrderBy_Run_Order_monitor(
                str(route_id),
                self.xfero_token)

        except Exception as err:
            self.oq.put(self.done)
            logger.error(
                '%s - Exception while retrieving workflow: Error %s. \
                (XFERO_Token=%s)',
                self.name, err, self.xfero_token, exc_info=True)
            logger.error(
                '%s - Exception: Original file name: %s. (XFERO_Token=%s)',
                self.name, self.original_filename, self.xfero_token)
            logger.error(
                '%s - Exception: Current file name: %s. (XFERO_Token=%s)',
                self.name, filename, self.xfero_token)
            # Move to error dir
            logger.error(
                '%s - Exception: Moving %s to %s. (XFERO_Token=%s)',
                self.name, filename, error_directory, self.xfero_token)

            args = (filename, error_directory)

            try:
                obj = Copy_File()
                print(obj.move_file(*args))
            except Exception as err:
                logger.error(
                    '%s - Exception moving file from %s to %s: Error %s. \
                    (XFERO_Token=%s)',
                    self.name,
                    filename,
                    error_directory,
                    err,
                    self.xfero_token,
                    exc_info=True)

            raise err

        if not wf_rows:
            logger.info(
                '%s - No workflow to perform. (XFERO_Token=%s)',
                self.name, self.xfero_token)
            return filename

        logger.info(
            '%s - Perform workflow. (XFERO_Token=%s)',
            self.name, self.xfero_token)
        for workflow in wf_rows:
            wf_args = ''
            wf_id = workflow['workflow_item_id']
            wf_route = workflow['workflow_item_route']
            wf_class = workflow['workflow_item_class']
            wf_function_call = workflow['workflow_item_function_call']
            if workflow['workflow_item_args'] != 'NULL':
                wf_args = workflow['workflow_item_args']
            wf_run_order = workflow['workflow_item_running_order']

            args = (filename,)
            # its possible that no parameters supplied to call
            if len(wf_args) > 0:
                # Split the wf_args on comma
                words = wf_args.split(',')

                # Convert args tuple to list temporarily
                list_args = list(args)

                for word in words:
                    list_args.append(word.strip())

                # Convert back to tuple
                args = tuple(list_args)

            # Instantiate Class:
            try:
                logger.debug(
                    '%s - Instantiate Class for thread. (XFERO_Token=%s)',
                    self.name, self.xfero_token)
                wf_instance = globals()[wf_class](self.xfero_token)
            except Exception as err:
                logger.error(
                    '%s - Error instantiating class: %s: Error %s. \
                    (XFERO_Token=%s)',
                    self.name, wf_class, err, self.xfero_token, exc_info=True)
                logger.error(
                    '%s - Exception: Original file name: %s. (XFERO_Token=%s)',
                    self.name, self.original_filename, self.xfero_token)
                logger.error(
                    '%s - Exception: Current file name: %s. (XFERO_Token=%s)',
                    self.name, filename, self.xfero_token)
                # Move to error dir
                logger.error(
                    '%s - Exception: Moving %s to %s. (XFERO_Token=%s)',
                    self.name, filename, error_directory, self.xfero_token)

                args = (filename, error_directory)

                try:
                    obj = Copy_File()
                    print(obj.move_file(*args))
                except Exception as err:
                    logger.error(
                        '%s - Exception moving file from %s to %s: Error %s. \
                        (XFERO_Token=%s)',
                        self.name, filename, error_directory, err,
                        self.xfero_token, exc_info=True)

                raise err

            # Call Method
            try:
                logger.info(
                    '%s - Calling workflow method. (XFERO_Token=%s)',
                    self.name, self.xfero_token)
                filename = getattr(wf_instance, wf_function_call)(*args)
            except Exception as err:
                logger.error(
                    '%s - Error in called method: %s: Error %s. (XFERO_Token=%s)',
                    self.name, wf_function_call, err, self.xfero_token,
                    exc_info=True)
                logger.error(
                    '%s - Exception: Original file name: %s. (XFERO_Token=%s)',
                    self.name, self.original_filename, self.xfero_token)
                logger.error(
                    '%s - Exception: Current file name: %s. (XFERO_Token=%s)',
                    self.name, filename, self.xfero_token)
                # Move to error dir
                logger.error(
                    '%s - Exception: Moving %s to %s. (XFERO_Token=%s)',
                    self.name, filename, error_directory, self.xfero_token)

                args = (filename, error_directory)

                try:
                    obj = Copy_File()
                    print(obj.move_file(*args))
                except Exception as err:
                    logger.error(
                        '%s - Exception moving file from %s to %s: Error %s. \
                        (XFERO_Token=%s)',
                        self.name, filename, error_directory, err,
                        self.xfero_token, exc_info=True)

                raise err

        return filename
