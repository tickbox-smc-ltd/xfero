#!/usr/bin/env python
''' XFERO Statistics '''
import psutil
import logging.config
from /xfero/ import get_conf as get_conf

def collect():
    '''

    **Purpose:**

    The collect function collects performance information about XFERO and the
    server it is running on. It monitors the following and produced logs.

    *CPU*

    *psutil.cpu_percent(interval=0.1, percpu=False)*

    Return a float representing the current system-wide CPU utilization as a
    percentage. When interval is > 0.0 compares system CPU times elapsed before
    and after the interval (blocking). When interval is 0.0 or None compares
    system CPU times elapsed since last call or module import, returning
    immediately. In this case is recommended for accuracy that this function be
    called with at least 0.1 seconds between calls.

    When percpu is True returns a list of floats representing the utilization as
    a percentage for each CPU. First element of the list refers to first CPU,
    second element to second CPU and so on. The order of the list is consistent
    across calls.

    *psutil.cpu_times(percpu=False)*

    Return system CPU times as a namedtuple. Every attribute represents the time
    CPU has spent in the given mode.

    The attributes availability varies depending on the platform. Here follows a
    list of all available attributes:

    .. hlist::

       * user
       * system
       * idle
       * nice (UNIX)
       * iowait (Linux)
       * irq (Linux, FreeBSD)
       * softirq (Linux)
       * steal (Linux >= 2.6.11)
       * guest (Linux >= 2.6.24)
       * guest_nice (Linux >= 3.2.0)

    *psutil.cpu_times_percent(interval=0.1, percpu=False)*

    Same as cpu_percent() but provides utilization percentages for each specific
    CPU time as is returned by cpu_times(). interval and percpu arguments have
    the same meaning as in cpu_percent().

    *MEMORY*

    *psutil.virtual_memory()*

    Return statistics about system memory usage as a namedtuple including the
    following fields, expressed in bytes:

    .. hlist::

       * total: total physical memory available
       * available: the actual amount of available memory that can be given
       instantly to processes that request more memory in bytes; this is
       calculated by summing different memory values depending on the platform
       (e.g. free + buffers + cached on Linux) and it is supposed to be used to
       monitor actual memory usage in a cross platform fashion.
       * percent: the percentage usage calculated as (total - available) / total
       x 100
       * used: memory used, calculated differently depending on the platform and
       designed for informational purposes only.
       * free: memory not being used at all (zeroed) that is readily available;
       note that this doesn't reflect the actual memory available (use
       'available' instead).

    Platform-specific fields:

    .. hlist::

       * active (UNIX): memory currently in use or very recently used, and so it
       is in RAM.
       * inactive (UNIX): memory that is marked as not used.
       * buffers (Linux, BSD): cache for things like file system metadata.
       * cached (Linux, BSD): cache for various things.
       * wired (BSD, OSX): memory that is marked to always stay in RAM. It is
       never moved to disk.
       * shared (BSD): memory that may be simultaneously accessed by multiple
       processes.

    The sum of 'used' and 'available' does not necessarily equal total. On
    Windows 'available' and 'free' are the same.

    *psutil.swap_memory()*

    Return system swap memory statistics as a named tuple including the
    following attributes:

    .. hlist::
       * total: total swap memory in bytes
       * used: used swap memory in bytes
       * free: free swap memory in bytes
       * percent: the percentage usage
       * sin: no. of bytes the system has swapped in from disk (cumulative)
       * sout: no. of bytes the system has swapped out from disk (cumulative)

    'sin' and 'sout' on Windows are meaningless and always set to 0.

    *DISK*

    *psutil.disk_partitions(all=False)*

    Return all mounted disk partitions as a list of namedtuples including
    device, mount point and filesystem type, similarly to "df" command on posix.

    If all parameter is False return physical devices only (e.g. hard disks,
    cd-rom drives, USB keys) and ignore all others (e.g. memory partitions such
    as /dev/shm).

    Namedtuple's 'fstype' field is a string which varies depending on the
    platform.

    On Linux it can be one of the values found in /proc/filesystems (e.g. 'ext3'
    for an ext3 hard drive o 'iso9660' for the CD-ROM drive).

    On Windows it is determined via GetDriveType and can be either "removable",
    "fixed", "remote", "cdrom", "unmounted" or "ramdisk".

    On OSX and FreeBSD it is retrieved via getfsstat(2).

    *psutil.disk_usage(path)*

    Return disk usage statistics about the given path as a namedtuple including
    total, used and free space expressed in bytes plus the percentage usage.
    OSError is raised if path does not exist.

    *psutil.disk_io_counters(perdisk=False)*

    Return system disk I/O statistics as a namedtuple including the following
    attributes:

    .. hlist::

       * read_count: number of reads
       * write_count: number of writes
       * read_bytes: number of bytes read
       * write_bytes: number of bytes written
       * read_time: time spent reading from disk (in milliseconds)
       * write_time: time spent writing to disk (in milliseconds)

    If perdisk is True return the same information for every physical disk
    installed on the system as a dictionary with partition names as the keys and
    the named tuple described above as the values.

    *Network*

    *psutil.net_io_counters(pernic=False)*

    Return network I/O statistics as a namedtuple including the following
    attributes:

    .. hlist::
       * bytes_sent: number of bytes sent
       * bytes_recv: number of bytes received
       * packets_sent: number of packets sent
       * packets_recv: number of packets received
       * errin: total number of errors while receiving
       * errout: total number of errors while sending
       * dropin: total number of incoming packets which were dropped
       * dropout: total number of outgoing packets which were dropped (always 0
       on OSX and BSD)

    If pernic is True return the same information for every network interface
    installed on the system as a dictionary with network interface names as the
    keys and the named tuple described above as the values.

    **Usage Notes:**

    None

    *Example usage:*

    ```collect()```

    **Process Flow**

    .. figure::  ../process_flow/stats.png
       :align:   center

       Process Flow: Stats

    *External dependencies*

    os (/xfero/.stats.xfero_stats)
    psutil (/xfero/.stats.xfero_stats)
    /xfero/
      get_conf (/xfero/.stats.xfero_stats)

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
    logger = logging.getLogger('sysinfo')

    logger.info('Running XFERO Scheduler...')

    # Capture CPU info
    logger.info(10 * '*' + ' CPU INFORMATION ' + 10 * '*')
    num_cpus = psutil.NUM_CPUS
    logger.info('Number of CPU\'s = %s', num_cpus)

    logger.info('CPU Times:')
    logger.info(psutil.cpu_times())

    logger.info(
        'Current System-wide CPU utilization as a percentage per CPU. 5 x \
        Responses with 3 second interval')
    for element in range(5):
        logger.info(psutil.cpu_percent(interval=3, percpu=True))

    logger.info(
        'CPU Times as a Percentage per CPU. Every attribute represents the \
        time a CPU has spent in the given mode. 5 x Responses with 3 second \
        interval')
    for element in range(5):
        logger.info(psutil.cpu_times_percent(interval=3, percpu=True))

    # Capture Memory info
    logger.info(10 * '*' + ' MEMORY INFORMATION ' + 10 * '*')
    logger.info('Virtual Memory:')
    logger.info(psutil.virtual_memory())
    logger.info('Swap Memory:')
    logger.info(psutil.swap_memory())

    # Capture Disk info
    logger.info(10 * '*' + ' DISK INFORMATION ' + 10 * '*')
    logger.info('Disk Partitions:')
    logger.info(psutil.disk_partitions())
    logger.info('Disk Usage:')
    logger.info(psutil.disk_usage('/'))
    logger.info('IO Counters')
    logger.info(psutil.disk_io_counters())

    # Capture Network info
    logger.info(10 * '*' + ' NETWORK INFORMATION PER NIC ' + 10 * '*')
    logger.info(psutil.net_io_counters(pernic=True))

if __name__ == '__main__':
    collect()
