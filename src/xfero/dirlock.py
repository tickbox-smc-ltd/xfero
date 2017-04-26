'''
Directory locking module
'''

import os
import shutil
import time
import socket

class Lock:

    '''

    **Purpose:**

    A directory locking class that works works across threads and processes (or
    even servers), since only one will get to do mkdir.

    It purpose is to enable Xfero to function in a clustered environment. Because
    the mkdir is atomic in its creation it ensures that only one process can act
    on a directory at a time. Thus enabling xfero to function in an Active/Active
    cluster.

    When a lock directory is created a lock file will also be written within the
    directory with the following name pattern:

    hostname_pid

    Where Hostname is the server name and pid is the process id of the creating
    process. If there is a processing error, the lockfile may remain in the
    directory despite the fact that the host or the process on which it is
    running has crashed or errored. This would effectively stop other
    operational xfero processes from accessing the directory despite files being
    written their for processing.

    If employed in a cluster, a cluster management function should check the
    lock files to ensure that the process on the host is still running and if it
    isn't, delete the lockdir to free the lock.

    **Usage Notes:**

    None

    *Example usage:*

    ```with Lock("/xfero/WIN1/xfero"):```
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

    def __init__(self, *args, **kwds):
        '''
        Initialise - cross-platform locking. Locking will raise exceptions.
        Unlocking won't. So, unlock all you want
        '''
        if not len(args):
            raise ValueError
        # detemine how long to wait for locks(min)
        if 'wait' in kwds:
            self.wait = kwds['wait'] * 60
        else:
            self.wait = 5
        name = args[0]
        self.dirname = name + '_lock/'
        self.hostname = socket.gethostname()
        self.pid = str(os.getpid())

    def acquire(self):
        '''
        Acquire the lock, if possible.
        '''
        try:
            os.mkdir(self.dirname)  # ATOMIC
            filehandle = open(self.dirname + os.sep + self.hostname + \
                               '_' +self.pid, 'w')
            filehandle.write('Locked by xfero')
            filehandle.close()

        except OSError as err:
            print('OSError: %s' % err)
            raise

    def unlock(self):
        '''
        Unlock - does not raise an exception, safe to unlock as often as you
        want it may just do nothing
        '''

        try:
            # os.rmdir(self.dirname)
            shutil.rmtree(self.dirname)
            return True
        except OSError:
            return False

    def __enter__(self):
        '''
        Activated when used in the with statement. Should automatically acquire
        a lock to be used in the with block.
        '''
        self.acquire()
        return self

    def __exit__(self, typeof, value, traceback):
        '''
        Activated at the end of the with statement. It automatically releases
        the lock if it isn't locked.
        '''
        self.unlock()

if __name__ == "__main__":
    # print('testing lock')
    dirn = 'xfero'
    # l=Lock(name)
    # f=open(file,'w')
    # f.write('test')
    # f.close()
    # print(l)
    # time.sleep(30)
    # l.unlock()

    # Acquire a lock in the directory
    try:
        with Lock(dirn) as lock:
            print('Lock acquired.')
            # Do something with the locked file
            time.sleep(30)

    except Lock.FileLockException:
        print('Unable to acquire a lock')
    except KeyboardInterrupt:
        pass

'''
# This is a test of threads using the lock to ensure that the threads do not
access the file at the same time

if __name__ == "__main__":
    import sys
    import functools
    import threading
    import tempfile
    temp_dir = tempfile.mkdtemp()
    protected_path = os.path.join( temp_dir, "xfero" )
    print("Protecting file: {}".format( protected_path ))
    fl = Lock( protected_path )

    def writeLines(line, repeat=10):
        with fl:
            for _ in range(repeat):
                with open( 'poo', 'a' ) as f:
                    f.write( line + "\n" )
                    f.flush()
                #print(line + "\n")
                #time.sleep(10)

    th1 = threading.Thread(target=functools.partial( writeLines,
    "1111111111111111111111111111111" ) )
    th2 = threading.Thread(target=functools.partial( writeLines,
    "2222222222222222222222222222222" ) )
    th3 = threading.Thread(target=functools.partial( writeLines,
    "3333333333333333333333333333333" ) )
    th4 = threading.Thread(target=functools.partial( writeLines,
    "4444444444444444444444444444444" ) )

    th1.start()
    th2.start()
    th3.start()
    th4.start()

    th1.join()
    th2.join()
    th3.join()
    th4.join()

    # Print the contents of the file.
    # Please manually inspect the output.  Does it look like the operations were
    # atomic?
    with open( 'poo', 'r' ) as f:
        sys.stdout.write( f.read() )
'''
