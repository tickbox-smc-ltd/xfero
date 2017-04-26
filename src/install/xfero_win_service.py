'''
Service Installation
--------------------

The XFERO service can be installed as follows:

C:\TickboxConsulting\XFERO\install> python xfero_win_service.py install

Service Control
---------------

That's it! The service can now be started from the command line by

C:\TickboxConsulting\XFERO\install> NET START XFERO_Service
or from the Service Control Manager

Delete Service
sc delete XFERO_Service

'''

import win32service  
import win32serviceutil  
import win32event 
import sys
import subprocess 
from /xfero/ import scheduler as scheduler
from /xfero/.db import manage_control as db_control
  
class PySvc(win32serviceutil.ServiceFramework):  
    # you can NET START/STOP the service by the following name  
    _svc_name_ = "XFERO_Service"  
    # this text shows up as the service name in the Service  
    # Control Manager (SCM)  
    _svc_display_name_ = "/Xfero/ Service"  
    # this text shows up as the description in the SCM  
    _svc_description_ = "This service controls the XFERO service."  
      
    def __init__(self, args):  
        win32serviceutil.ServiceFramework.__init__(self,args)  
        # create an event to listen for stop requests on  
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
        #self.workdir='c:\TickboxConsulting\XFERO'
        self.pidfile='c:/TickboxConsulting/XFERO/conf/xfero-service.pid'
      
    # core logic of the service     
    def SvcDoRun(self):  
        import servicemanager  
        
        self.script='c:/Python33/Lib/site-packages//xfero//scheduler.py'
        
        theproc = subprocess.Popen(['python', self.script])
        #theproc.communicate()
        # Write PID file
        pidfile = open(self.pidfile, 'w')
        pidfile.write(str(theproc.pid))
        pidfile.close()
        
        rc = None  
          
        # if the stop event hasn't been fired keep looping  
        while rc != win32event.WAIT_OBJECT_0:  
            # block for 5 seconds and listen for a stop event  
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            rc = win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)   
      
    # called when we're being shut down      
    def SvcStop(self):  
        
        rows = db_control.update_XFERO_Control('1', 'STOPPED')
        
        # tell the SCM we're shutting down  
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  
        self.script='c:/Python33/Lib/site-packages//xfero//stop_XFERO.py'
        '''
        thecloseproc = subprocess.Popen(['python', self.script])
        try:
            outs, errs = thecloseproc.communicate(timeout=3600)
        except subprocess.TimeoutExpired:
            thecloseproc.kill()
            outs, errs = thecloseproc.communicate()
        '''
        
        # fire the stop event  
        win32event.SetEvent(self.hWaitStop)  
          
if __name__ == '__main__':  
    win32serviceutil.HandleCommandLine(PySvc)  
