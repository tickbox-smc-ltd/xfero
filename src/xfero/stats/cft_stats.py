#!/usr/bin/env python
''' Axway CFT Transfer Details '''
import shlex
import subprocess
import logging.config
import /xfero/.get_conf as get_conf


def collect():
    '''

    **Purpose:**

    The collect function collects transfer statistics from Axway CFT Catalogue.

    Uses XferoDisplayModel.xml to retrieve the required information from the Axway
    catalogue.

    **Usage Notes:**

    None

    *Example usage:*

    ```collect()```

    **Process Flow**

    None

    *External dependencies*

    /xfero/
      get_conf (/xfero/.stats.cft_stats)

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 02/12/2013 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+
    | 27/10/2014 | Chris Falck | modified call to get_conf                     |
    +------------+-------------+-----------------------------------------------+

    '''

    try:
        (xfero_logger,.xfero_database, outbound_directory, transient_directory,
         error_directory, xfero_pid) = get_conf.get.xfero_config()
    except Exception as err:
        print('Cannot get XFERO Config: %s', err)
        raise err

    logging.config.fileConfig(xfero_logger)

    # create logger
    logger = logging.getLogger('cftrecvstats')

    # The states should be modified to include all states so all transfers
    # successful or otherwise can be written to the log
    recv_cmd = 'cftutil display fmodel=XferoDisplayModel.xml, \
    content=xferocustom, state=tx, direct=recv'
    send_cmd = 'cftutil display fmodel=XferoDisplayModel.xml, \
    content=xferocustom, state=tx, direct=send'

    try:
        args = shlex.split(recv_cmd.replace('\\', '\\\\'))
        popen = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p_stdout, p_stderr = popen.communicate()

        print(p_stdout)
        print(p_stderr)
        logger.info('STDOUT = %s', p_stdout)
        logger.error('STDERR = %s', p_stderr)

        # Now we have the catalogue results in the p_stdout pipe we will be able
        # to remove the transfers from the catalogue
        # For each record we should get the IDT and issue the following command:
        # cftutil delete part=GSI_PART, IDT=J3109504, DIRECT=RECV

    except Exception as err:
        logger.error(
            'Unable to get CFT Received files from CFT Catalogue',
            exc_info=True)

        # create logger
    logger = logging.getLogger('cftsendstats')

    try:
        args = shlex.split(send_cmd.replace('\\', '\\\\'))
        popen = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p_stdout, p_stderr = popen.communicate()

        print(p_stdout)
        print(p_stderr)
        logger.info('STDOUT = %s', p_stdout)
        logger.error('STDERR = %s', p_stderr)

        # Now we have the catalogue results in the p_stdout pipe we will be able
        # to remove the transfers from the catalogue
        # For each record we should get the IDT and issue the following command:
        # cftutil delete part=GSI_PART, IDT=J3109504, DIRECT=RECV

    except Exception as err:
        logger.error(
            'Unable to get CFT Sent files from CFT Catalogue', exc_info=True)
