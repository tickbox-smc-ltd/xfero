'''

**Purpose:**

This is a basic test harness which creates files to be processed by XFERO.

The script creates X number of file per minute for Y minutes.

It takes a list of file name suffixes which it selects randomly from to create
the file names

**Unit Test Module:** None

+------------+-------------+----------------------------------------------------+
| Date       | Author      | Change Details                                     |
+============+=============+====================================================+
| 07/02/2014 | Chris Falck | Created                                            |
+------------+-------------+----------------------------------------------------+

'''
import datetime
import os
import shutil
import time
import os.path
import subprocess
import random
import shlex

#workdir = "C:\Python33\File-injector\Created-files"
#workdir = "C:\\tmp"
#outdir  = "C:\Python33\File-injector\Output-files"
#outdir  = "C:\\xfero\\mon_dir"
#file_name = 'TESTFILE_'

workdir = "/tmp"
outdir  = "/xfero/WIN1"
file_list = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF']
file_create_size = [1, 2, 3, 4, 5]
s = 0
n = 1
total_cnt = 0
while True:
    try:
        num_files = int(input("Please enter the number of files of each type to create: "))
    except ValueError:
        print("Could you at least give me an actual number?")
        continue
    break

while True:
    try:
        delay_secs = int(input("How long in seconds to wait between each file creation?: "))
    except ValueError:
        print("Could you at least give me an actual number?")
        continue
    break

#Create and move files+++++++++++++++++++++++++++++++++++
for f in file_list:

    for i in range(num_files):

        ts_now = datetime.datetime.now().time()
        ts = str(datetime.datetime.now())

        ts_file = ts.replace('-', '').replace(' ', '').replace(':', '').replace('.', '')
        testfile = workdir + os.sep + f + '_' + ts_file

        # create the file with dd - dd if=/dev/zero of=test-file bs=1MB count=1
        file_size = random.choice(file_create_size)
        cmd = 'mkfile ' + str(file_size) +'M ' + testfile
        # Added cmd.replace in shlex below to accommodate issues with windows file paths in shlex
        args = shlex.split(cmd.replace('\\','\\\\'))

        print(args)

        try:
            popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p_stdout, p_stderr = popen.communicate()

        except:
            print('Error!!!!!!!!!!!')

        if (popen.returncode != 0):
            print('Error calling dd!!!!!!!!!!!!!!!!!!!')
        else:
            total_cnt += 1
            shutil.move(workdir + os.sep + f + '_' + ts_file, outdir)
            print('File %s created' % (f + '_' + ts_file))
            print('File moved to %s' % (outdir))
            time.sleep(delay_secs)

print('Total Files = %s' % total_cnt)


#Time Add Function addSecs +++++++++++++++++++++++++++++++++++++
def addSecs(tm, delay_secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=delay_secs)
    return fulldate.time()
