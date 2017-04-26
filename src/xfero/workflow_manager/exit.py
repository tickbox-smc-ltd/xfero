#!/usr/bin/env python
'''Exit'''
import logging.config
import subprocess
import shlex
from /xfero/ import get_conf as get_conf

try:
    (xfero_logger,.xfero_database, outbound_directory, transient_directory,
     error_directory, xfero_pid) = get_conf.get.xfero_config()
except Exception as err:
    print('Cannot get XFERO Config: %s' % err)
    raise err

logging.config.fileConfig(xfero_logger)
# create logger
logger = logging.getLogger('exit')

class Exit(object):

    '''
    **Purpose:**

    The :class:`exit.Exit` class enables execution of bespoke scripts & commands
    during workflow execution.

    **Process Flow**

    .. figure::  ../process_flow/exit.png
       :align:   center

       Process Flow: Exit

    *External dependencies*

    /xfero/
      get_conf (/xfero/.workflow_manager.exit)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/06/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 27/10/2014 | Chris Falck | modified call to get_conf                     |
    +------------+-------------+-----------------------------------------------+

    '''

    def __init__(self, xfero_token=False):
        '''init'''
        logger.debug('Object initialised: Exit')
        self.xfero_token =.xfero_token
        self.filename = ''
        self.exit_call = ''

    def exit(self, filename, exit_call=None):
        '''exit'''
        self.filename = filename
        self.exit_call = exit_call.replace('{FileName}', self.filename)

        logger.info('Building exit call.... (XFERO_Token=%s)', self.xfero_token)

        args = shlex.split(self.exit_call)

        try:
            exit_out = subprocess.check_output(args)
        except Exception as err:
            logger.error('Error executing exit script %s. \
            (XFERO_Token=%s)', self.exit_call, self.xfero_token)
            raise err

        logger.info('Running exit script %s as process %s. \
        (XFERO_Token=%s)', self.exit_call, exit_out, self.xfero_token)
        return self.filename

if __name__ == "__main__":

    # Testing function xfer_exit("ls", "-lrt"
    xit_obj = Exit()
    xit_out = xit_obj.exit("/bin/ls -lrt",)
    print(xit_out)
