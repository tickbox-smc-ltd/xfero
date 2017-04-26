#!/usr/bin/env python
'''
File locking module
'''
import os
import time
import socket
import errno
import sys


class FileLock(object):

    '''

    **Purpose:**

    A file locking class that enables context-manager via a with statement. It
    has cross platform capabilities as it doesn't rely on msvcrt or fcntl for
    the locking.

    It purpose is to enable xfero to function in a clustered environment. Because
    the lockfile is atomic in its creation it ensures that only one process can
    act on a directory at a time. Thus enabling xfero to function in an Active/
    Active cluster.

    If a lock of a directory cannot be established within a specified timeout
    period an exception is raised.

    When a lock is created the hostname and the pid of the locking process is
    written to the lock file.

    If there is a processing error, the lockfile may remain in the directory
    despite the fact that the host or the process on which it is running has
    crashed or errored. This would effectively stop other operational xfero
    processes from accessing the directory despite files being written their
    for processing.

    If employed in a cluster, the cluster management function should be
    designed to monitor if processes are running or if a host in the cluster is
    down. If this is the case it should check the monitored directories for
    locks that are held by the host or for a host that does not have an active
    monitor process.

    **Usage Notes:**

    None

    *Example usage:*

    ```with FileLock("/xfero/WIN1/test.txt", timeout=2) as lock:```
        ```print("Lock acquired.")```
        ```# Do something with the locked file```

    :param filename: Name of the Lockfile
    :param timeout: Maximum time to wait for the a lock to be aquired
    :param delay : Time delay in seconds between retries to aquire the lock

    **Unit Test Module:**

    None

    +------------+-------------+-----------------------------------------------+
    | Date       | Author      | Change Details                                |
    +============+=============+===============================================+
    | 15/10/2014 | Chris Falck | Created                                       |
    +------------+-------------+-----------------------------------------------+

    '''

    class FileLockException(Exception):
        '''
        Exception class
        '''
        pass

    def __init__(self, protected_file_path, timeout=None, delay=1,
                 lock_file_contents=None):
        '''
        Initialise - Prepare the file locker. Specify the file to lock and
        optionally the maximum timeout and the delay between each attempt to
        lock.
        '''
        self.is_locked = False
        self.lockfile = protected_file_path + ".lock"
        self.file_name = protected_file_path
        self.timeout = timeout
        self.delay = delay
        self.hostname = socket.gethostname()
        self.pid = str(os.getpid())
        self._lock_file_contents = lock_file_contents
        if self._lock_file_contents is None:
            self._lock_file_contents = "Owning process args:\n"
            for arg in sys.argv:
                self._lock_file_contents += arg + "\n"

    def locked(self):
        """
        Returns True if the file is owned by THIS FileLock instance. (Even if
        this returns false, the file could be owned by another FileLock
        instance, possibly in a different thread or process).
        """
        return self.is_locked

    def available(self):
        """
        Returns True if the file is currently available to be locked.
        """
        return not os.path.exists(self.lockfile)

    def acquire(self, blocking=True):
        '''
        Acquire the lock, if possible. If the lock is in use, and `blocking` is
        False, return False. Otherwise, check again every `self.delay` seconds
        until it either gets the lock or exceeds `timeout` number of seconds, in
        which case it raises an exception.
        '''

        start_time = time.time()
        while True:
            try:
                # Attempt to create the lockfile.
                # These flags cause os.open to raise an OSError if the file
                # already exists.
                filed = os.open(self.lockfile, os.O_CREAT | os.O_EXCL |
                                os.O_RDWR)
                with os.fdopen(filed, 'a') as lockfile:
                    lockfile.write(self.hostname + '\n' + self.pid + '\n')
                    # Print some info about the current process as debug info
                    # for anyone who bothers to look.
                    lockfile.write(self._lock_file_contents)
                break
            except OSError as err:
                if err.errno != errno.EEXIST:
                    raise
                if self.timeout is not None and \
                (time.time() - start_time) >= self.timeout:
                    raise FileLock.FileLockException("Timeout occurred.")
                if not blocking:
                    return False
                time.sleep(self.delay)
        self.is_locked = True
        return True

    def release(self):
        '''
        Get rid of the lock by deleting the lockfile.
        When working in a `with` statement, this gets automatically called at
        the end.
        '''
        self.is_locked = False
        os.unlink(self.lockfile)

    def __enter__(self):
        '''
        Activated when used in the with statement.
        Should automatically acquire a lock to be used in the with block.
        '''
        self.acquire()
        return self

    def __exit__(self, typee, value, traceback):
        '''
        Activated at the end of the with statement.
        It automatically releases the lock if it isn't locked.
        '''
        self.release()

    def __del__(self):
        '''
        Make sure this ``FileLock`` instance doesn't leave a .lock file lying
        around.
        '''
        if self.is_locked:
            self.release()

    def purge(self):
        """
        For debug purposes only.  Removes the lock file from the hard disk.
        """
        if os.path.exists(self.lockfile):
            self.release()
            return True
        return False

if __name__ == "__main__":

    import functools
    import threading
    import tempfile
    temp_dir = tempfile.mkdtemp()
    protected_filepath = os.path.join(temp_dir, "somefile.txt")
    print("Protecting file: {}".format(protected_filepath))
    fl = FileLock(protected_filepath)

    def writeLines(line, repeat=10):
        with fl:
            for _ in range(repeat):
                with open(protected_filepath, 'a') as pf:
                    pf.write(line + "\n")
                    pf.flush()

    th1 = threading.Thread(
        target=functools.partial(writeLines, "1111111111111111111111111111111"))
    th2 = threading.Thread(
        target=functools.partial(writeLines, "2222222222222222222222222222222"))
    th3 = threading.Thread(
        target=functools.partial(writeLines, "3333333333333333333333333333333"))
    th4 = threading.Thread(
        target=functools.partial(writeLines, "4444444444444444444444444444444"))

    th1.start()
    th2.start()
    th3.start()
    th4.start()

    th1.join()
    th2.join()
    th3.join()
    th4.join()

    assert not os.path.exists(fl.lockfile), "The lock file wasn't cleaned up!"

    # Print the contents of the file.
    # Please manually inspect the output.  Does it look like the operations
    # were atomic?
    with open(protected_filepath, 'r') as pfp:
        sys.stdout.write(pfp.read())
