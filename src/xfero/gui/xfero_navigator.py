#!/usr/bin/env python
'''

**Purpose:**

This script is the main GUI Screen that is used to build and maintain XFERO
Databases.

**Unit Test Module:** None

*External dependencies*

os (/xfero/.gui.xfero_navigator)
    /xfero/
      db
       manage_cots_pattern (/xfero/.gui.xfero_navigator)
       manage_function (/xfero/.gui.xfero_navigator)
       manage_partner (/xfero/.gui.xfero_navigator)
       manage_priority (/xfero/.gui.xfero_navigator)
       manage_route (/xfero/.gui.xfero_navigator)
       manage_workflow (/xfero/.gui.xfero_navigator)
       manage_xfer (/xfero/.gui.xfero_navigator)
      gui
        xfero_av_patterns (/xfero/.gui.xfero_navigator)
        xfero_control (/xfero/.gui.xfero_navigator)
        xfero_cots_patterns (/xfero/.gui.xfero_navigator)
        xfero_functions (/xfero/.gui.xfero_navigator)
        xfero_partners (/xfero/.gui.xfero_navigator)
        xfero_priority (/xfero/.gui.xfero_navigator)
        xfero_scheduled_task (/xfero/.gui.xfero_navigator)
        xfero_tickbox (/xfero/.gui.xfero_navigator)

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+
| 05/05/2014 | Chris Falck | Added call to XFERO_Control GUI                      |
+------------+-------------+---------------------------------------------------+
| 10/05/2014 | Chris Falck | Modified call to read_XFERO_Partner which was changed|
|            |             | to facilitate working in a multiprocessing        |
|            |             | environment.                                      |
+------------+-------------+---------------------------------------------------+
| 12/05/2014 | Chris Falck | New column added to XFERO_Xfer table - 'xfer_delsrc' |
|            |             | Therefore, modified the navigator to accommodate  |
|            |             | the new column                                    |
+------------+-------------+---------------------------------------------------+
| 25/02/2015 | Chris Falck | Modified the Xfer Dialogue to enable in- line     |
|            |             | editing of the generated command                  |
+------------+-------------+---------------------------------------------------+

'''

from tkinter import Tk, Label, Entry, Button, Toplevel, sys
from tkinter import StringVar, messagebox, Checkbutton, Frame, Menu
from tkinter import END, TOP, BOTH, Y, VERTICAL
from tkinter import HORIZONTAL, NSEW, NS, EW, GROOVE
import tkinter.ttk as ttk
from tkinter.font import Font
import os
import subprocess
from /xfero/.db import manage_route as db_route
from /xfero/.db import manage_workflow as db_workflow
from /xfero/.db import manage_xfer as db_xfer
from /xfero/.db import manage_priority as db_priority
from /xfero/.db import manage_function as db_function
from /xfero/.db import manage_cots_pattern as db_cots_pattern
from /xfero/.db import manage_partner as db_partner
from /xfero/.gui import xfero_av_patterns as.xfero_av_patterns
from /xfero/.gui import xfero_cots_patterns as.xfero_cots_patterns
from /xfero/.gui import xfero_partners as.xfero_partners
from /xfero/.gui import xfero_scheduled_task as.xfero_scheduled_task
from /xfero/.gui import xfero_functions as.xfero_functions
from /xfero/.gui import xfero_priority as.xfero_priority
from /xfero/.gui import xfero_control as.xfero_control
from /xfero/.gui import xfero_tickbox as.xfero_tickbox

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global win, root
    root = Tk()
    root.title('XFERO_Navigator')
    root.geometry('829x670+6+96')
    win = XFERO_Navigator(root)
    init()
    root.mainloop()

win = None

def create_XFERO_Navigator(root):
    '''Starting point when module is imported by another program.'''
    global win, w_win
    if win:  # So we have only one instance of window.
        return
    win = Toplevel(root)
    win.title('XFERO_Navigator')
    win.geometry('829x670+6+96')
    w_win = XFERO_Navigator(win)
    init()
    return w_win

def destroy_XFERO_Navigator():
    ''' Destroy Navigator'''
    global win
    win.destroy()
    win = None

def init():
    '''initialise'''
    pass

def Menu_Control_Click():
    '''Menu Control'''
    xfero_control.vp_start_gui()
    sys.stdout.flush()

def Menu_AV_COTS_Patterns_Click():
    '''Menu AV COTS Patterns'''
    xfero_av_patterns.vp_start_gui()
    sys.stdout.flush()

def Menu_COTS_Patterns_Click():
    '''Menu COTS Patterns'''
    xfero_cots_patterns.vp_start_gui()
    sys.stdout.flush()

def Menu_Partners_Click():
    '''Menu Partners'''
    xfero_partners.vp_start_gui()
    sys.stdout.flush()

def Menu_Scheduled_Tasks_Click():
    '''Menu Scheduled Tasks'''
    xfero_scheduled_task.vp_start_gui()
    sys.stdout.flush()

def Menu_Functions_Click():
    '''Menu Functions'''
    xfero_functions.vp_start_gui()
    sys.stdout.flush()

def Menu_Priority_Click():
    '''Menu Priority'''
    xfero_priority.vp_start_gui()
    sys.stdout.flush()

def Menu_Help_Click():
    '''Menu Help'''
    path = os.getcwd()

    os.system(path + os.sep + "XFERO_Help.pdf")

    if sys.platform == 'linux2':
        subprocess.call(["xdg-open", path + os.sep + "XFERO_Help.pdf"])
    else:
        subprocess.call(["open", path + os.sep + "XFERO_Help.pdf"])

    sys.stdout.flush()

def Menu_Tickbox_Click():
    '''Menu Tickbox'''
    xfero_tickbox.vp_start_gui()
    sys.stdout.flush()

def set_Tk_var():
    '''Setup TK Vars'''
    # These are Tk variables used passed to Tkinter and must be
    # defined before the widgets using them are created.
    # , identifier
    global che40, combobox, combobox_func
    global combobox_delsrc, combobox_cots, combobox_partner
    che40 = StringVar()
    combobox = StringVar()
    combobox_func = StringVar()
    combobox_cots = StringVar(root)
    combobox_partner = StringVar(root)
    combobox_delsrc = StringVar(root)

class XferDialog:
    ''' Xfer Dialogue Class'''
    def __init__(self, parent, runas, x_id=False, x_route=False,
                 x_cotspattern=False, x_partner=False, x_cmd=False,
                 x_params=False, x_delsrc=False):
        ''' Initialise '''
        self.x_id = x_id
        self.x_route = x_route
        self.x_cotspattern = x_cotspattern
        self.x_partner = x_partner
        self.x_cmd = x_cmd
        self.x_params = x_params
        self.x_delsrc = x_delsrc
        self.runAs = runas

        top = self.top = Toplevel(parent)
        top.title('Manage XFERO Transfer Targets')
        top.geometry('800x170+169+145')

        set_Tk_var()

        # Get COTS Patterns from db
        self.data = db_cots_pattern.list_all_patterns_XFERO_COTS_Pattern()

        self.l1 = ['<Select COTS Prototype>']
        for cots in self.data:
            self.l1.append(cots[0])

        self.TCombobox_COTS = ttk.OptionMenu(top, combobox_cots, *self.l1)
        self.TCombobox_COTS.place(
            relx=0.03, rely=0.13, relheight=0.17, relwidth=0.30)
        # self.TCombobox_COTS.configure(width=100)

        # Get Partners from db
        self.data1 = db_partner.list_service_name_XFERO_Partner()
        print(self.data1)

        self.l2 = ['<Select Target Partner>']
        for part in self.data1:
            self.l2.append(part[0])

        self.TCombobox_Partner = ttk.OptionMenu(
            top, combobox_partner, *self.l2)
        self.TCombobox_Partner.place(
            relx=0.35, rely=0.13, relheight=0.17, relwidth=0.30)
        # self.TCombobox_Partner.configure(width=100)

        self.l3 = ['<Select Del-Source>', 'No', 'Yes']

        self.TCombobox_DelSRC = ttk.OptionMenu(top, combobox_delsrc, *self.l3)
        self.TCombobox_DelSRC.place(
            relx=0.67, rely=0.13, relheight=0.17, relwidth=0.30)
        # self.TCombobox_DelSRC.configure(width=6)

        self.Label1 = Label(top)
        self.Label1.place(relx=0.03, rely=0.35, height=22, width=105)
        # self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#bfbfbf")
        # self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''COTS Prototype:''')

        self.Label2 = Label(top)
        self.Label2.place(relx=0.03, rely=0.57, height=22, width=71)
        # self.Label2.configure(background=_bgcolor)
        self.Label2.configure(disabledforeground="#bfbfbf")
        # self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Command:''')
        self.Label2.configure(width=71)

        self.Entry_CMD = Entry(top)
        self.Entry_CMD.place(
            relx=0.18, rely=0.54, relheight=0.20, relwidth=0.79)
        self.Entry_CMD.configure(background="white")
        self.Entry_CMD.configure(disabledforeground="#bfbfbf")
        # self.Entry_CMD.configure(font=font11)
        self.Entry_CMD.configure(foreground="#000000")
        self.Entry_CMD.configure(insertbackground="black")
        self.Entry_CMD.configure(width=382)

        self.Entry_COTS_Prototype = Entry(top)
        self.Entry_COTS_Prototype.place(
            relx=0.18, rely=0.32, relheight=0.20, relwidth=0.79)
        self.Entry_COTS_Prototype.configure(background="white")
        self.Entry_COTS_Prototype.configure(disabledforeground="#bfbfbf")
        # self.Entry_COTS_Prototype.configure(font=font11)
        self.Entry_COTS_Prototype.configure(foreground="#000000")
        self.Entry_COTS_Prototype.configure(insertbackground="black")
        self.Entry_COTS_Prototype.configure(width=382)

        self.Button_OK = Button(top)
        self.Button_OK.place(relx=0.91, rely=0.78, height=28, width=47)
        self.Button_OK.configure(activebackground="#ffffff")
        self.Button_OK.configure(activeforeground="#000000")
        # self.Button_OK.configure(background=_bgcolor)
        self.Button_OK.configure(disabledforeground="#bfbfbf")
        # self.Button_OK.configure(font=font10)
        self.Button_OK.configure(foreground="#000000")
        self.Button_OK.configure(highlightbackground="#ffffff")
        self.Button_OK.configure(highlightcolor="black")
        self.Button_OK.configure(text='''OK''')
        self.Button_OK.configure(state='disabled')
        self.Button_OK.configure(command=self.Button_OK_Click)

        self.Button_Generate = Button(top)
        self.Button_Generate.place(relx=0.80, rely=0.78, height=28, width=87)
        self.Button_Generate.configure(activebackground="#ffffff")
        self.Button_Generate.configure(activeforeground="#000000")
        # self.Button_Generate.configure(background=_bgcolor)
        self.Button_Generate.configure(disabledforeground="#bfbfbf")
        # self.Button_Generate.configure(font=font10)
        self.Button_Generate.configure(foreground="#000000")
        self.Button_Generate.configure(highlightbackground="#ffffff")
        self.Button_Generate.configure(highlightcolor="black")
        self.Button_Generate.configure(text='''Generate''')
        self.Button_Generate.configure(command=self.Button_Generate_Click)

        self.Button_Cancel = Button(top)
        self.Button_Cancel.place(relx=0.71, rely=0.78, height=28, width=70)
        self.Button_Cancel.configure(activebackground="#ffffff")
        self.Button_Cancel.configure(activeforeground="#000000")
        # self.Button_Cancel.configure(background=_bgcolor)
        self.Button_Cancel.configure(disabledforeground="#bfbfbf")
        # self.Button_Cancel.configure(font=font10)
        self.Button_Cancel.configure(foreground="#000000")
        self.Button_Cancel.configure(highlightbackground="#ffffff")
        self.Button_Cancel.configure(highlightcolor="black")
        self.Button_Cancel.configure(text='''Cancel''')
        self.Button_Cancel.configure(command=self.top.destroy)

        if self.runAs == 'edit':

            rows = db_cots_pattern.read_XFERO_COTS_Pattern(self.x_cotspattern)

            # for row in rows:
            self.c_id = rows[0]
            self.c_product = rows[1]
            self.c_pattern_name = rows[2]
            self.c_prototype = rows[3]
            combobox_cots.set(self.c_pattern_name)

            self.p_detail = ''

            self.p_row = db_partner.read_XFERO_Partner(self.x_partner)

            self.p_detail = self.p_row[1]
            # for c in self.p_row:
            #    print(c)
            #    self.p_detail = c[1]

            combobox_partner.set(self.p_detail)

            self.Button_Generate_Click()
            
            print(x_id, x_cmd, self.x_params)
            
            self.Entry_CMD.insert(
                0, x_cmd + ' ' + self.x_params)

    def Button_OK_Click(self):
        ''' Button OK Click '''
        #self.Button_Generate_Click()

        self.write_cmd_tup = self.Entry_CMD.get().partition(' ')
        delsrc = combobox_delsrc.get()

        # Determine if Update of Insert
        if self.runAs == 'edit':

            db_xfer.update_XFERO_Xfer(self.x_id, self.x_route, self.c_id,
                                   self.p_id, self.write_cmd_tup[0],
                                   self.write_cmd_tup[2], delsrc)

        else:

            db_xfer.create_XFERO_Xfer(self.x_route, self.c_id, self.p_id,
                                   self.write_cmd_tup[0],
                                   self.write_cmd_tup[2], delsrc)

        self.top.destroy()

    def Button_Generate_Click(self):
        ''' Button Generate Click '''
        self.Entry_COTS_Prototype.delete(0, END)
        self.Entry_CMD.delete(0, END)

        # Get the cots pattern and populate
        cots_pattern_name = combobox_cots.get()
        partner_name = combobox_partner.get()

        if cots_pattern_name == '<Select>' or partner_name == '<Select>':
            messagebox.showwarning(
                message='Please select COTS Prototype and Target System',
                icon='warning', title='Make Selections')
            self.Button_OK.configure(state="disabled")
        else:

            rows = db_cots_pattern.read_with_name_XFERO_COTS_Pattern(
                cots_pattern_name)

            self.c_id = rows[0]
            self.c_prototype = rows[3]
            self.Entry_COTS_Prototype.insert(0, self.c_prototype)

            rows = db_partner.read_psn_XFERO_Partner(partner_name)

            self.p_id = rows[0]
            self.p_service_name = rows[1]
            self.p_service_description = rows[2]
            self.p_cots_type = rows[3]
            self.p_remote_system_id = rows[4]
            self.p_code = rows[5]
            self.p_mode = rows[6]
            self.p_local_username = rows[7]
            self.p_local_password = rows[8]
            self.p_remote_user = rows[9]
            self.p_remote_password = rows[10]
            self.p_ca_cert = rows[11]
            self.p_cert_bundle = rows[12]
            self.p_control_port = rows[13]
            self.p_idf = rows[14]
            self.p_parm = rows[15]

            self.cmd_tup = self.c_prototype.partition(' ')
            self.cmd_params = self.cmd_tup[2]
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_REMOTE_SYSTEM_ID]', self.p_remote_system_id)
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_CODE]', self.p_code)
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_MODE]', self.p_mode)
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_LOCAL_USERNAME]', self.p_local_username)
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_LOCAL_PASSWORD]', self.p_local_password)
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_REMOTE_USER]', self.p_remote_user)
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_REMOTE_PASSWORD]', self.p_remote_password)
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_CA_CERT]', self.p_ca_cert)
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_CERT_BUNDLE]', self.p_cert_bundle)
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_CONTROL_PORT]', str(self.p_control_port))
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_IDF]', self.p_idf)
            self.cmd_params = self.cmd_params.replace(
                '[PARTNER_PARM]', self.p_parm)

            self.Entry_CMD.insert(
                0, self.cmd_tup[0] + self.cmd_tup[1] + self.cmd_params)

            self.Button_OK.configure(state="active")
            self.Button_Generate.configure(state="active")

class WFDialog:
    '''WFDialog class '''
    def __init__(self, parent, runas, wf_id=False, wf_route=False,
                 wf_class=False, wf_func=False, wf_args=False,
                 wf_run_order=False):
        ''' Initialise '''
        self.id = wf_id
        self.wf_route_id = wf_route
        self.wf_class = wf_class
        self.wf_func = wf_func
        self.wf_args = wf_args
        self.wf_run_order = wf_run_order
        self.runAs = runas

        top = self.top = Toplevel(parent)
        top.title('Manage XFERO Workflow')
        top.geometry('600x138+167+145')

        set_Tk_var()

        self.Label2 = Label(top)
        self.Label2.place(relx=0.07, rely=0.22, height=22, width=65)
        # self.Label2.configure(background=_bgcolor)
        self.Label2.configure(disabledforeground="#bfbfbf")
        # self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Function:''')

        # Get Functions from db
        self.data = db_function.list_fname_XFERO_Function()

        self.tup1 = ['<Select>']
        for func in self.data:
            print(func)
            self.tup1.append(func[0] + '-' + func[1])

        self.TCombobox1 = ttk.OptionMenu(top, combobox_func, *self.tup1)
        self.TCombobox1.place(
            relx=0.3, rely=0.17, relheight=0.2, relwidth=0.35)
        self.TCombobox1.configure(width=396)

        self.Label3 = Label(top)
        self.Label3.place(relx=0.07, rely=0.41, height=22, width=139)
        # self.Label3.configure(background=_bgcolor)
        self.Label3.configure(disabledforeground="#bfbfbf")
        # self.Label3.configure(font=font10)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Function Arguments:''')

        self.Entry_Func_Args = Entry(top)
        self.Entry_Func_Args.place(
            relx=0.3, rely=0.39, relheight=0.2, relwidth=0.62)
        self.Entry_Func_Args.configure(background="white")
        self.Entry_Func_Args.configure(disabledforeground="#bfbfbf")
        # self.Entry_Func_Args.configure(font=font11)
        self.Entry_Func_Args.configure(foreground="#000000")
        self.Entry_Func_Args.configure(insertbackground="black")
        self.Entry_Func_Args.configure(width=372)

        self.Label4 = Label(top)
        self.Label4.place(relx=0.71, rely=0.2, height=22, width=71)
        # self.Label4.configure(background=_bgcolor)
        self.Label4.configure(disabledforeground="#bfbfbf")
        # self.Label4.configure(font=font10)
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''Run Order:''')

        self.Entry_RunOrder = Entry(top)
        self.Entry_RunOrder.place(
            relx=0.85, rely=0.16, relheight=0.2, relwidth=0.07)
        self.Entry_RunOrder.configure(background="white")
        self.Entry_RunOrder.configure(disabledforeground="#bfbfbf")
        # self.Entry_RunOrder.configure(font=font11)
        self.Entry_RunOrder.configure(foreground="#000000")
        self.Entry_RunOrder.configure(insertbackground="black")
        self.Entry_RunOrder.configure(width=42)

        self.Button_OK = Button(top)
        self.Button_OK.place(relx=0.83, rely=0.65, height=28, width=47)
        self.Button_OK.configure(activebackground="#ffffff")
        self.Button_OK.configure(activeforeground="#000000")
        # self.Button_OK.configure(background=_bgcolor)
        self.Button_OK.configure(disabledforeground="#bfbfbf")
        # self.Button_OK.configure(font=font10)
        self.Button_OK.configure(foreground="#000000")
        self.Button_OK.configure(highlightbackground="#ffffff")
        self.Button_OK.configure(highlightcolor="black")
        self.Button_OK.configure(text='''OK''')
        self.Button_OK.configure(command=self.Button_WF_OK_Click)

        self.Button_Cancel = Button(top)
        self.Button_Cancel.place(relx=0.71, rely=0.65, height=28, width=70)
        self.Button_Cancel.configure(activebackground="#ffffff")
        self.Button_Cancel.configure(activeforeground="#000000")
        # self.Button_Cancel.configure(background=_bgcolor)
        self.Button_Cancel.configure(disabledforeground="#bfbfbf")
        # self.Button_Cancel.configure(font=font10)
        self.Button_Cancel.configure(foreground="#000000")
        self.Button_Cancel.configure(highlightbackground="#ffffff")
        self.Button_Cancel.configure(highlightcolor="black")
        self.Button_Cancel.configure(text='''Cancel''')
        self.Button_Cancel.configure(command=self.top.destroy)

        if self.runAs == 'edit':
            self.Entry_Func_Args.insert(0, self.wf_args)
            self.Entry_RunOrder.insert(0, wf_run_order)

            combobox_func.set(self.wf_func + '-' + self.wf_class)

    def Button_WF_OK_Click(self):
        ''' Button WF OK Click '''
        # Get info from screen
        run_order = self.Entry_RunOrder.get()
        f_args = self.Entry_Func_Args.get()

        # Get Function
        self.f_call = combobox_func.get()
        f_call, f_class = self.f_call.split('-')

        if self.runAs == 'edit':
            result = db_workflow.update_XFERO_Workflow_Item(
                self.id, self.wf_route_id, f_class, f_call, f_args, run_order)
        else:
            result = db_workflow.create_XFERO_Workflow_Item(
                self.wf_route_id, f_class, f_call, f_args, run_order)

        self.top.destroy()


class RouteDialog:
    ''' Route Dialogue'''
    def __init__(self, parent, runas, identifier=False, mon_dir=False,
                 filename_pattern=False, route_active=False,
                 route_priority=False):
        ''' Initialise '''
        self.id = identifier
        self.runAs = runas

        top = self.top = Toplevel(parent)
        top.title('Manage XFERO Route')
        top.geometry('600x199+51+118')

        set_Tk_var()

        self.Label1 = Label(top)
        self.Label1.place(relx=0.08, rely=0.15, height=22, width=65)
        # self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#bfbfbf")
        # self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Route ID:''')

        self.Label2 = Label(top)
        self.Label2.place(relx=0.08, rely=0.34, height=22, width=137)
        # self.Label2.configure(background=_bgcolor)
        self.Label2.configure(disabledforeground="#bfbfbf")
        # self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Monitored Directory:''')

        self.Label3 = Label(top)
        self.Label3.place(relx=0.08, rely=0.52, height=22, width=116)
        # self.Label3.configure(background=_bgcolor)
        self.Label3.configure(disabledforeground="#bfbfbf")
        # self.Label3.configure(font=font10)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Filename Pattern:''')

        self.Label4 = Label(top)
        self.Label4.place(relx=0.4, rely=0.15, height=22, width=49)
        # self.Label4.configure(background=_bgcolor)
        self.Label4.configure(disabledforeground="#bfbfbf")
        # self.Label4.configure(font=font10)
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''Active:''')

        self.Label5 = Label(top)
        self.Label5.place(relx=0.58, rely=0.15, height=22, width=56)
        # self.Label5.configure(background=_bgcolor)
        self.Label5.configure(disabledforeground="#bfbfbf")
        # self.Label5.configure(font=font10)
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(text='''Priority:''')

        self.Checkbutton1 = Checkbutton(top)
        self.Checkbutton1.place(
            relx=0.48, rely=0.14, relheight=0.12, relwidth=0.09)
        # self.Checkbutton1.configure(activebackground="#ffffff")
        self.Checkbutton1.configure(activeforeground="#000000")
        # self.Checkbutton1.configure(background=_bgcolor)
        self.Checkbutton1.configure(disabledforeground="#bfbfbf")
        # self.Checkbutton1.configure(font=font10)
        self.Checkbutton1.configure(foreground="#000000")
        self.Checkbutton1.configure(highlightbackground="#ffffff")
        self.Checkbutton1.configure(highlightcolor="black")
        self.Checkbutton1.configure(state="active")
        self.Checkbutton1.configure(variable=che40)
        self.Checkbutton1.configure(width=55)
        self.Checkbutton1.configure(onvalue=1)
        self.Checkbutton1.configure(offvalue=0)
        self.Checkbutton1.select()

        # Get COTS Patterns from db
        self.data = db_priority.list_XFERO_Priority_detail()

        self.tup1 = ['<Select>']
        for cots in self.data:
            self.tup1.append(cots[0])

        self.TCombobox_Priority = ttk.OptionMenu(top, combobox, *self.tup1)
        self.TCombobox_Priority.place(
            relx=0.7, rely=0.13, relheight=0.14, relwidth=0.24)
        self.TCombobox_Priority.configure(width=246)

        self.Entry_Route_ID = Entry(top)
        self.Entry_Route_ID.place(
            relx=0.2, rely=0.15, relheight=0.14, relwidth=0.20)
        self.Entry_Route_ID.configure(background="#F2F0F0")
        # self.Entry_Route_ID.configure(state="readonly")
        self.Entry_Route_ID.configure(disabledforeground="#bfbfbf")
        # self.Entry_Route_ID.configure(font=font11)
        self.Entry_Route_ID.configure(foreground="#000000")
        self.Entry_Route_ID.configure(insertbackground="black")
        self.Entry_Route_ID.configure(width=20)

        self.Entry_FilePattern = Entry(top)
        self.Entry_FilePattern.place(
            relx=0.31, rely=0.51, relheight=0.14, relwidth=0.64)
        self.Entry_FilePattern.configure(background="white")
        self.Entry_FilePattern.configure(disabledforeground="#bfbfbf")
        # self.Entry_FilePattern.configure(font=font11)
        self.Entry_FilePattern.configure(foreground="#000000")
        self.Entry_FilePattern.configure(insertbackground="black")
        self.Entry_FilePattern.configure(width=380)

        self.Entry_MonDir = Entry(top)
        self.Entry_MonDir.place(
            relx=0.31, rely=0.32, relheight=0.14, relwidth=0.64)
        self.Entry_MonDir.configure(background="white")
        self.Entry_MonDir.configure(disabledforeground="#bfbfbf")
        # self.Entry_MonDir.configure(font=font11)
        self.Entry_MonDir.configure(foreground="#000000")
        self.Entry_MonDir.configure(insertbackground="black")
        self.Entry_MonDir.configure(width=382)

        self.Button_Add = Button(top)
        self.Button_Add.place(relx=0.85, rely=0.76, height=28, width=54)
        self.Button_Add.configure(activebackground="#ffffff")
        self.Button_Add.configure(activeforeground="#000000")
        # self.Button_Add.configure(background=_bgcolor)
        self.Button_Add.configure(disabledforeground="#bfbfbf")
        # self.Button_Add.configure(font=font10)
        self.Button_Add.configure(foreground="#000000")
        self.Button_Add.configure(highlightbackground="#ffffff")
        self.Button_Add.configure(highlightcolor="black")
        self.Button_Add.configure(text='''OK''')
        self.Button_Add.configure(command=self.Button_Route_Add_Click)

        self.Button_Cancel = Button(top)
        self.Button_Cancel.place(relx=0.73, rely=0.76, height=28, width=70)
        self.Button_Cancel.configure(activebackground="#ffffff")
        self.Button_Cancel.configure(activeforeground="#000000")
        # self.Button_Cancel.configure(background=_bgcolor)
        self.Button_Cancel.configure(disabledforeground="#bfbfbf")
        # self.Button_Cancel.configure(font=font10)
        self.Button_Cancel.configure(foreground="#000000")
        self.Button_Cancel.configure(highlightbackground="#ffffff")
        self.Button_Cancel.configure(highlightcolor="black")
        self.Button_Cancel.configure(text='''Cancel''')
        self.Button_Cancel.configure(command=self.top.destroy)

        if self.runAs == 'edit':
            self.Entry_FilePattern.insert(0, filename_pattern)
            self.Entry_MonDir.insert(0, mon_dir)
            self.Entry_Route_ID.insert(0, self.id)

            if route_active == '0' or route_active == 0:
                self.Checkbutton1.deselect()
            else:
                self.Checkbutton1.select()

            self.p_row = db_priority.read_XFERO_Priority(route_priority)
            # for c in self.p_row:
            #    self.p_detail = c[1]
            # combobox.set(self.p_detail)

            self.p_detail = self.p_row[1]
            combobox.set(self.p_detail)

    def Button_Route_Add_Click(self):
        ''' Button Route Add Click '''
        # Get info from screen
        # Is Active selected or not
        active = che40.get()

        # Get Priority
        self.priority_level = '1'
        priority_detail = combobox.get()

        # Get the level for the priority detail
        priority_level_tup = db_priority.read_XFERO_Priority_level(
            priority_detail)
        # for c in priority_level_tup:
        self.priority_level = priority_level_tup[0]

        # Get info from Entry Fields
        file_pattern = self.Entry_FilePattern.get()
        mon_dir = self.Entry_MonDir.get()

        if self.runAs == 'edit':
            result = db_route.update_XFERO_Route(
                mon_dir, file_pattern, active, self.priority_level, self.id)
        else:
            result = db_route.create_XFERO_Route(
                mon_dir, file_pattern, active, self.priority_level,)

        self.top.destroy()


class XFERO_Navigator:
    ''' Navigatoe Class '''
    # class variable to track direction of column
    # header sort
    SortDir = True     # descending

    def __init__(self, master=None):
        ''' Initialise '''
        _bgcolor = '#ffffff'  # X11 color: #ffffff
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#ffffff'  # X11 color: #ffffff
        _ana2color = '#ffffff'  # X11 color: #ffffff
        font12 = "-family {Lucida Grande} -size 14 -weight normal \
        -slant roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        # self.style.configure('.',background=_bgcolor)
        # self.style.configure('.',foreground=_fgcolor)
        # self.style.configure('.',font=font10)
        self.style.map(
            '.', background=[('selected', _compcolor), ('active', _ana2color)])

        self.Frame1 = Frame(master)
        self.Frame1.place(relx=0.02, rely=0.03, relheight=0.29, relwidth=0.95)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(width=785)

        self.TLabelframe1 = ttk.Labelframe(master)
        self.TLabelframe1.place(
            relx=0.04, rely=0.05, relheight=0.22, relwidth=0.91)
        self.TLabelframe1.configure(text='''Routes''')
        self.TLabelframe1.configure(width=785)

        frame = ttk.Frame(self.TLabelframe1)
        frame.pack(side=TOP, fill=BOTH, expand=Y)

        # create the tree and scrollbars
        self.dataCols = (
            'Identifier', 'Monitored Directory', 'Filename Pattern', 'Active',
            'Priority')
        self.tree = ttk.Treeview(columns=self.dataCols, show='headings')

        ysb = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        # add tree and scrollbars to frame
        self.tree.grid(in_=frame, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=frame, row=0, column=1, sticky=NS)
        xsb.grid(in_=frame, row=1, column=0, sticky=EW)

        # set frame resize priorities
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        # load tree data
        self._load_data()
        # Bind selection
        self.tree.bind('<Button-1>', self.Tree_Select)

        self.Button_Route_Delete = Button(self.Frame1)
        self.Button_Route_Delete.place(
            relx=0.9, rely=0.83, height=28, width=68)
        self.Button_Route_Delete.configure(activebackground="#ffffff")
        self.Button_Route_Delete.configure(activeforeground="#000000")
        # self.Button_Route_Delete.configure(background=_bgcolor)
        self.Button_Route_Delete.configure(disabledforeground="#bfbfbf")
        # self.Button_Route_Delete.configure(font=font10)
        self.Button_Route_Delete.configure(foreground="#000000")
        self.Button_Route_Delete.configure(highlightbackground="#ffffff")
        self.Button_Route_Delete.configure(highlightcolor="black")
        self.Button_Route_Delete.configure(state="disabled")
        self.Button_Route_Delete.configure(text='''Delete''')
        self.Button_Route_Delete.configure(
            command=lambda: self.Button_Route_Delete_Click())

        self.Button_Route_Edit = Button(self.Frame1)
        self.Button_Route_Edit.place(relx=0.81, rely=0.83, height=28, width=65)
        self.Button_Route_Edit.configure(activebackground="#ffffff")
        self.Button_Route_Edit.configure(activeforeground="#000000")
        # self.Button_Route_Edit.configure(background=_bgcolor)
        self.Button_Route_Edit.configure(disabledforeground="#bfbfbf")
        # self.Button_Route_Edit.configure(font=font10)
        self.Button_Route_Edit.configure(foreground="#000000")
        self.Button_Route_Edit.configure(highlightbackground="#ffffff")
        self.Button_Route_Edit.configure(highlightcolor="black")
        self.Button_Route_Edit.configure(state="disabled")
        self.Button_Route_Edit.configure(text='''Edit...''')
        self.Button_Route_Edit.configure(
            command=lambda: self.edit_route_dialog())

        self.Button_Route_Add = Button(self.Frame1)
        self.Button_Route_Add.place(relx=0.72, rely=0.83, height=28, width=66)
        self.Button_Route_Add.configure(activebackground="#ffffff")
        self.Button_Route_Add.configure(activeforeground="#000000")
        # self.Button_Route_Add.configure(background=_bgcolor)
        self.Button_Route_Add.configure(disabledforeground="#bfbfbf")
        # self.Button_Route_Add.configure(font=font10)
        self.Button_Route_Add.configure(foreground="#000000")
        self.Button_Route_Add.configure(highlightbackground="#ffffff")
        self.Button_Route_Add.configure(highlightcolor="black")
        self.Button_Route_Add.configure(text='''Add...''')
        self.Button_Route_Add.configure(
            command=lambda: self.create_route_dialog())

        self.Frame2 = Frame(master)
        self.Frame2.place(relx=0.02, rely=0.34, relheight=0.29, relwidth=0.95)
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(width=785)

        self.TLabelframe2 = ttk.Labelframe(master)
        self.TLabelframe2.place(
            relx=0.04, rely=0.36, relheight=0.22, relwidth=0.91)
        self.TLabelframe2.configure(text='''Workflow''')
        self.TLabelframe2.configure(width=785)

        f_wf = ttk.Frame(self.TLabelframe2)
        f_wf.pack(side=TOP, fill=BOTH, expand=Y)

        # create the tree and scrollbars
        self.dataCols_wf = (
            'Identifier', 'Route ID', 'Class', 'Method', 'Arguments',
            'Run Order')
        self.tree_wf = ttk.Treeview(columns=self.dataCols_wf, show='headings')

        ysb_wf = ttk.Scrollbar(orient=VERTICAL, command=self.tree_wf.yview)
        xsb_wf = ttk.Scrollbar(orient=HORIZONTAL, command=self.tree_wf.xview)
        self.tree_wf['yscroll'] = ysb_wf.set
        self.tree_wf['xscroll'] = xsb_wf.set

        # add tree and scrollbars to frame
        self.tree_wf.grid(in_=f_wf, row=0, column=0, sticky=NSEW)
        ysb_wf.grid(in_=f_wf, row=0, column=1, sticky=NS)
        xsb_wf.grid(in_=f_wf, row=1, column=0, sticky=EW)

        # set frame resize priorities
        f_wf.rowconfigure(0, weight=1)
        f_wf.columnconfigure(0, weight=1)

        self.Button_Workflow_Delete = Button(self.Frame2)
        self.Button_Workflow_Delete.place(
            relx=0.9, rely=0.83, height=28, width=73)
        self.Button_Workflow_Delete.configure(activebackground="#ffffff")
        self.Button_Workflow_Delete.configure(activeforeground="#000000")
        # self.Button_Workflow_Delete.configure(background=_bgcolor)
        self.Button_Workflow_Delete.configure(disabledforeground="#bfbfbf")
        # self.Button_Workflow_Delete.configure(font=font10)
        self.Button_Workflow_Delete.configure(foreground="#000000")
        self.Button_Workflow_Delete.configure(highlightbackground="#ffffff")
        self.Button_Workflow_Delete.configure(highlightcolor="black")
        self.Button_Workflow_Delete.configure(state="disabled")
        self.Button_Workflow_Delete.configure(text='''Delete''')
        self.Button_Workflow_Delete.configure(
            command=lambda: self.Button_Workflow_Delete_Click())

        self.Button_Workflow_Edit = Button(self.Frame2)
        self.Button_Workflow_Edit.place(
            relx=0.82, rely=0.83, height=28, width=65)
        self.Button_Workflow_Edit.configure(activebackground="#ffffff")
        self.Button_Workflow_Edit.configure(activeforeground="#000000")
        # self.Button_Workflow_Edit.configure(background=_bgcolor)
        self.Button_Workflow_Edit.configure(disabledforeground="#bfbfbf")
        # self.Button_Workflow_Edit.configure(font=font10)
        self.Button_Workflow_Edit.configure(foreground="#000000")
        self.Button_Workflow_Edit.configure(highlightbackground="#ffffff")
        self.Button_Workflow_Edit.configure(highlightcolor="black")
        self.Button_Workflow_Edit.configure(state="disabled")
        self.Button_Workflow_Edit.configure(text='''Edit...''')
        self.Button_Workflow_Edit.configure(
            command=lambda: self.Button_Workflow_Edit_Click())

        self.Button_Workflow_Add = Button(self.Frame2)
        self.Button_Workflow_Add.place(
            relx=0.73, rely=0.83, height=28, width=66)
        self.Button_Workflow_Add.configure(activebackground="#ffffff")
        self.Button_Workflow_Add.configure(activeforeground="#000000")
        # self.Button_Workflow_Add.configure(background=_bgcolor)
        self.Button_Workflow_Add.configure(disabledforeground="#bfbfbf")
        # self.Button_Workflow_Add.configure(font=font10)
        self.Button_Workflow_Add.configure(foreground="#000000")
        self.Button_Workflow_Add.configure(highlightbackground="#ffffff")
        self.Button_Workflow_Add.configure(highlightcolor="black")
        self.Button_Workflow_Add.configure(state="disabled")
        self.Button_Workflow_Add.configure(text='''Add...''')
        self.Button_Workflow_Add.configure(
            command=lambda: self.Button_Workflow_Add_Click())

        self.Frame3 = Frame(master)
        self.Frame3.place(relx=0.02, rely=0.65, relheight=0.31, relwidth=0.95)
        self.Frame3.configure(relief=GROOVE)
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(relief="groove")
        self.Frame3.configure(width=785)

        self.TLabelframe3 = ttk.Labelframe(master)
        self.TLabelframe3.place(
            relx=0.04, rely=0.67, relheight=0.22, relwidth=0.91)
        self.TLabelframe3.configure(text='''Transfer Targets''')
        self.TLabelframe3.configure(width=785)

        f_xfer = ttk.Frame(self.TLabelframe3)
        f_xfer.pack(side=TOP, fill=BOTH, expand=Y)

        # create the tree and scrollbars
        self.dataCols_xfer = ('Identifier', 'Route ID', 'COTS Pattern',
                              'Partner ID', 'Command', 'Parameters',
                              'Delete Source File')
        self.tree_xfer = ttk.Treeview(
            columns=self.dataCols_xfer, show='headings')

        ysb_xfer = ttk.Scrollbar(orient=VERTICAL, command=self.tree_xfer.yview)
        xsb_xfer = ttk.Scrollbar(
            orient=HORIZONTAL, command=self.tree_xfer.xview)
        self.tree_xfer['yscroll'] = ysb_xfer.set
        self.tree_xfer['xscroll'] = xsb_xfer.set

        # add tree and scrollbars to frame
        self.tree_xfer.grid(in_=f_xfer, row=0, column=0, sticky=NSEW)
        ysb_xfer.grid(in_=f_xfer, row=0, column=1, sticky=NS)
        xsb_xfer.grid(in_=f_xfer, row=1, column=0, sticky=EW)

        # set frame resize priorities
        f_xfer.rowconfigure(0, weight=1)
        f_xfer.columnconfigure(0, weight=1)

        self.Button_Xfer_Delete = Button(self.Frame3)
        self.Button_Xfer_Delete.place(relx=0.9, rely=0.83, height=28, width=73)
        self.Button_Xfer_Delete.configure(activebackground="#ffffff")
        self.Button_Xfer_Delete.configure(activeforeground="#000000")
        # self.Button_Xfer_Delete.configure(background=_bgcolor)
        self.Button_Xfer_Delete.configure(disabledforeground="#bfbfbf")
        # self.Button_Xfer_Delete.configure(font=font10)
        self.Button_Xfer_Delete.configure(foreground="#000000")
        self.Button_Xfer_Delete.configure(highlightbackground="#ffffff")
        self.Button_Xfer_Delete.configure(highlightcolor="black")
        self.Button_Xfer_Delete.configure(state="disabled")
        self.Button_Xfer_Delete.configure(text='''Delete''')
        self.Button_Xfer_Delete.configure(
            command=lambda: self.Button_Xfer_Delete_Click())

        self.Button_Xfer_Edit = Button(self.Frame3)
        self.Button_Xfer_Edit.place(relx=0.82, rely=0.83, height=28, width=65)
        self.Button_Xfer_Edit.configure(activebackground="#ffffff")
        self.Button_Xfer_Edit.configure(activeforeground="#000000")
        # self.Button_Xfer_Edit.configure(background=_bgcolor)
        self.Button_Xfer_Edit.configure(disabledforeground="#bfbfbf")
        # self.Button_Xfer_Edit.configure(font=font10)
        self.Button_Xfer_Edit.configure(foreground="#000000")
        self.Button_Xfer_Edit.configure(highlightbackground="#ffffff")
        self.Button_Xfer_Edit.configure(highlightcolor="black")
        self.Button_Xfer_Edit.configure(state="disabled")
        self.Button_Xfer_Edit.configure(text='''Edit...''')
        self.Button_Xfer_Edit.configure(
            command=lambda: self.Button_Xfer_Edit_Click())

        self.Button_Xfer_Add = Button(self.Frame3)
        self.Button_Xfer_Add.place(relx=0.73, rely=0.83, height=28, width=66)
        self.Button_Xfer_Add.configure(activebackground="#ffffff")
        self.Button_Xfer_Add.configure(activeforeground="#000000")
        # self.Button_Xfer_Add.configure(background=_bgcolor)
        self.Button_Xfer_Add.configure(disabledforeground="#bfbfbf")
        # self.Button_Xfer_Add.configure(font=font10)
        self.Button_Xfer_Add.configure(foreground="#000000")
        self.Button_Xfer_Add.configure(highlightbackground="#ffffff")
        self.Button_Xfer_Add.configure(highlightcolor="black")
        self.Button_Xfer_Add.configure(state="disabled")
        self.Button_Xfer_Add.configure(text='''Add...''')
        self.Button_Xfer_Add.configure(
            command=lambda: self.Button_Xfer_Add_Click())

        self.menubar = Menu(master, font=font12, bg=_bgcolor, fg=_fgcolor)
        master.configure(menu=self.menubar)

        self.management_functions = Menu(master, tearoff=0)
        self.menubar.add_cascade(menu=self.management_functions,
                                 activebackground="#ffffff",
                                 activeforeground="#111111",
                                 background="#ffffff",
                                 # font=font12,
                                 foreground="#000000",
                                 label="Management Functions")
        self.management_functions.add_command(
            activebackground="#ffffff",
            activeforeground="#000000",
            background="#ffffff",
            command=Menu_Partners_Click,
            # font=font12,
            foreground="#000000",
            label="Partners...")
        self.management_functions.add_command(
            activebackground="#ffffff",
            activeforeground="#000000",
            background="#ffffff",
            command=Menu_COTS_Patterns_Click,
            # font=font12,
            foreground="#000000",
            label="COTS Patterns...")
        self.management_functions.add_command(
            activebackground="#ffffff",
            activeforeground="#000000",
            background="#ffffff",
            command=Menu_AV_COTS_Patterns_Click,
            # font=font12,
            foreground="#000000",
            label="AV COTS Patterns...")
        self.management_functions.add_command(
            activebackground="#ffffff",
            activeforeground="#000000",
            background="#ffffff",
            command=Menu_Functions_Click,
            # font=font12,
            foreground="#000000",
            label="Transformation Functions...")
        self.management_functions.add_command(
            activebackground="#ffffff",
            activeforeground="#000000",
            background="#ffffff",
            command=Menu_Priority_Click,
            # font=font12,
            foreground="#000000",
            label="Priority Levels...")
        self.management_functions.add_command(
            activebackground="#ffffff",
            activeforeground="#000000",
            background="#ffffff",
            command=Menu_Control_Click,
            # font=font12,
            foreground="#000000",
            label="Control...")
        self.schedule_management = Menu(master, tearoff=0)
        self.menubar.add_cascade(menu=self.schedule_management,
                                 activebackground="#ffffff",
                                 activeforeground="#111111",
                                 background="#ffffff",
                                 # font=font12,
                                 foreground="#000000",
                                 label="Schedule Management")
        self.schedule_management.add_command(
            activebackground="#ffffff",
            activeforeground="#000000",
            background="#ffffff",
            command=Menu_Scheduled_Tasks_Click,
            # font=font12,
            foreground="#000000",
            label="Scheduled Tasks...")
        self.help = Menu(master, tearoff=0)
        self.menubar.add_cascade(menu=self.help,
                                 activebackground="#ffffff",
                                 activeforeground="#111111",
                                 background="#ffffff",
                                 # font=font12,
                                 foreground="#000000",
                                 label="Help")
        self.help.add_command(
            activebackground="#ffffff",
            activeforeground="#000000",
            background="#ffffff",
            command=Menu_Help_Click,
            # font=font12,
            foreground="#000000",
            label="'XFERO Help...")
        self.help.add_command(
            activebackground="#ffffff",
            activeforeground="#000000",
            background="#ffffff",
            command=Menu_Tickbox_Click,
            # font=font12,
            foreground="#000000",
            label="About Tickbox SMC Limited...")

    def reload_tree(self):
        ''' reload tree '''
        # Delete treview items
        tree_list = self.tree.get_children()
        for tree in tree_list:
            self.tree.delete(tree)
        # reload treview with new row
        self._load_data()

        self.Button_Route_Delete.configure(state="disabled")
        self.Button_Route_Edit.configure(state="disabled")

    def reload_tree_wf(self):
        ''' reload tree '''
        # Delete treview items
        tree_list_wf = self.tree_wf.get_children()
        for tree in tree_list_wf:
            self.tree_wf.delete(tree)
        # reload treview with new row
        self._load_data_wf()
        self.Button_Workflow_Delete.configure(state='disabled')
        self.Button_Workflow_Edit.configure(state='disabled')

    def reload_tree_xfer(self):
        ''' reload tree '''
        # Delete treview items
        tree_list_xfer = self.tree_xfer.get_children()
        for tree in tree_list_xfer:
            self.tree_xfer.delete(tree)
        # reload treview with new row
        self._load_data_xfer()
        self.Button_Xfer_Delete.configure(state='disabled')
        self.Button_Xfer_Edit.configure(state='disabled')

    def delete_tree_wf(self):
        ''' delete tree '''
        # Delete treview items
        tree_list_wf = self.tree_wf.get_children()
        for tree in tree_list_wf:
            self.tree_wf.delete(tree)

    def delete_tree_xfer(self):
        ''' delete tree '''
        # Delete treview items
        tree_list_xfer = self.tree_xfer.get_children()
        for tree in tree_list_xfer:
            self.tree_xfer.delete(tree)

    def Tree_Select(self, p1_tree):
        ''' tree select '''
        self.Button_Route_Delete.configure(state="normal")
        self.Button_Route_Edit.configure(state="normal")
        self.Button_Workflow_Add.configure(state="normal")
        self.Button_Xfer_Add.configure(state="normal")
        self.route_selected = p1_tree

        self.delete_tree_wf()
        self.delete_tree_xfer()

        item = self.tree.identify('item', p1_tree.x, p1_tree.y)

        values = self.tree.item(item, 'values')
        if values:
            self.identifier = values[0]
            self.route_mon_dir = values[1]
            self.route_filename_pattern = values[2]
            self.route_active = values[3]
            self.route_priority = values[4]

            # load tree data
            # self._load_data_wf()
            self.reload_tree_wf()
            self.reload_tree_xfer()
            # self._load_data_xfer()
            # Bind selection
            self.tree_wf.bind('<Button-1>', self.Tree_Select_WF)
            self.tree_xfer.bind('<Button-1>', self.Tree_Select_Xfer)

        sys.stdout.flush()

    def Tree_Select_WF(self, p1_tree):
        ''' tree select '''
        self.delete_tree_xfer()
        item = self.tree_wf.identify('item', p1_tree.x, p1_tree.y)
        values = self.tree_wf.item(item, 'values')
        if values:
            self.identifier_wf = values[0]
            self.wf_route = values[1]
            self.wf_class = values[2]
            self.wf_func = values[3]
            self.wf_args = values[4]
            self.wf_run_order = values[5]

            self.reload_tree_xfer()

        self.Button_Workflow_Delete.configure(state="normal")
        self.Button_Workflow_Edit.configure(state="normal")

    def Tree_Select_Xfer(self, p1_tree):
        ''' tree select '''
        item = self.tree_xfer.identify('item', p1_tree.x, p1_tree.y)

        values = self.tree_xfer.item(item, 'values')
        if values:
            self.identifier_xfer = values[0]
            self.xfer_route = values[1]
            self.xfer_cotspattern = values[2]
            self.xfer_partner = values[3]
            self.xfer_cmd = values[4]
            self.xfer_params = values[5]
            self.xfer_delsrc = values[6]

        self.Button_Xfer_Delete.configure(state="normal")
        self.Button_Xfer_Edit.configure(state="normal")

    def _load_data(self):
        ''' load data '''
        self.data = db_route.list_XFERO_Route()

        # configure column headings
        for col in self.dataCols:
            self.tree.heading(col, text=col.title(),
                              command=lambda col=col:
                              self._column_sort(col, XFERO_Navigator.SortDir))
            self.tree.column(col, width=Font().measure(col.title()))

        # add data to the tree
        for item in self.data:
            self.tree.insert('', 'end', values=item)

            # and adjust column widths if necessary
            for idx, val in enumerate(item):
                iwidth = Font().measure(val)
                if self.tree.column(self.dataCols[idx], 'width') < iwidth:
                    self.tree.column(self.dataCols[idx], width=iwidth)

    def _load_data_wf(self):
        ''' load data '''
        self.data_workflow = \
        db_workflow.list_XFERO_Workflow_Item_OrderBy_Run_Order(
            self.identifier)

        # configure column headings
        for c_wf in self.dataCols_wf:
            self.tree_wf.heading(c_wf, text=c_wf.title(),
                                 command=lambda c_wf=c_wf:
                                 self._column_sort_wf(c_wf,
                                                      XFERO_Navigator.SortDir))
            self.tree_wf.column(c_wf, width=Font().measure(c_wf.title()))

        # add data to the tree
        for item_wf in self.data_workflow:
            self.tree_wf.insert('', 'end', values=item_wf)

            # and adjust column widths if necessary
            for idx_wf, val_wf in enumerate(item_wf):
                iwidth_wf = Font().measure(val_wf)
                if self.tree_wf.column(self.dataCols_wf[idx_wf], 'width') < \
                iwidth_wf:
                    self.tree_wf.column(
                        self.dataCols_wf[idx_wf], width=iwidth_wf)

    def _load_data_xfer(self):
        ''' load data '''
        self.data_xfer = db_xfer.list_XFERO_Xfer_Route(self.identifier)

        # configure column headings
        for c_x in self.dataCols_xfer:
            self.tree_xfer.heading(c_x, text=c_x.title(),
                                   command=lambda c_x=c_x:
                                   self._column_sort_xfer(c_x,
                                                          XFERO_Navigator.SortDir))
            self.tree_xfer.column(c_x, width=Font().measure(c_x.title()))

        # add data to the tree
        for item_x in self.data_xfer:
            self.tree_xfer.insert('', 'end', values=item_x)

            # and adjust column widths if necessary
            for idx_x, val_x in enumerate(item_x):
                iwidth_x = Font().measure(val_x)
                if self.tree_xfer.column(self.dataCols_xfer[idx_x], 'width') < \
                iwidth_x:
                    self.tree_xfer.column(
                        self.dataCols_xfer[idx_x], width=iwidth_x)

    def _column_sort(self, col, descending=False):
        ''' columns sorting '''
        # grab values to sort as a list of tuples (column value, column id)
        data = [(self.tree.set(child, col), child)
                for child in self.tree.get_children('')]

        # reorder data
        # tkinter looks after moving other items in
        # the same row
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            self.tree.move(item[1], '', indx)

        # reverse sort direction for next sort operation
        XFERO_Navigator.SortDir = not descending

    def _column_sort_wf(self, col, descending=False):
        ''' columns sorting '''
        # grab values to sort as a list of tuples (column value, column id)
        data_wf = [(self.tree_wf.set(child, col), child)
                   for child in self.tree_wf.get_children('')]

        # reorder data
        # tkinter looks after moving other items in
        # the same row
        data_wf.sort(reverse=descending)
        for indx, item in enumerate(data_wf):
            self.tree_wf.move(item[1], '', indx)

        # reverse sort direction for next sort operation
        XFERO_Navigator.SortDir = not descending

    def _column_sort_xfer(self, col, descending=False):
        ''' columns sorting '''
        # grab values to sort as a list of tuples (column value, column id)
        data_x = [(self.tree_xfer.set(child, col), child)
                  for child in self.tree_xfer.get_children('')]

        # reorder data
        # tkinter looks after moving other items in
        # the same row
        data_x.sort(reverse=descending)
        for indx, item in enumerate(data_x):
            self.tree_xfer.move(item[1], '', indx)

        # reverse sort direction for next sort operation
        XFERO_Navigator.SortDir = not descending

    def create_route_dialog(self):
        ''' create route dialogue '''
        runas = 'add'
        root.update()
        dialog = RouteDialog(root, runas)
        root.wait_window(dialog.top)

        self.reload_tree()
        self.delete_tree_wf()
        self.delete_tree_xfer()

    def edit_route_dialog(self):
        ''' edit route dialogue '''
        runas = 'edit'
        root.update()

        d = RouteDialog(root, runas, self.identifier, self.route_mon_dir,
                        self.route_filename_pattern, self.route_active,
                        self.route_priority)
        root.wait_window(d.top)

        self.reload_tree()
        self.delete_tree_wf()
        self.delete_tree_xfer()

    def Button_Route_Delete_Click(self):
        ''' Button Route Delete '''
        db_route.delete_XFERO_Route(self.identifier)

        self.reload_tree()
        self.delete_tree_wf()
        self.delete_tree_xfer()

    def Button_Workflow_Add_Click(self):
        ''' Button Workflow Add '''
        runas = 'add'
        root.update()
        dialog = WFDialog(root, runas, False, self.identifier)
        root.wait_window(dialog.top)

        # self.reload_tree()
        # self.delete_tree_wf()
        # self.delete_tree_xfer()
        self.Tree_Select(self.route_selected)
        self.reload_tree_wf()

    def Button_Workflow_Delete_Click(self):
        ''' Button Workflow Delete '''
        db_workflow.delete_XFERO_Workflow_Item(self.identifier_wf)

        self.reload_tree_wf()

    def Button_Workflow_Edit_Click(self):
        ''' Button Workflow Edit '''
        runas = 'edit'
        root.update()
        dialog = WFDialog(root, runas, self.identifier_wf, self.wf_route,
                          self.wf_class, self.wf_func, self.wf_args,
                          self.wf_run_order)
        root.wait_window(dialog.top)

        # self.reload_tree()
        # self.delete_tree_wf()
        # self.delete_tree_xfer()
        self.Tree_Select(self.route_selected)
        self.reload_tree_wf()

    def Button_Xfer_Add_Click(self):
        ''' Button Xfer Add '''
        runas = 'add'
        root.update()
        dialog = XferDialog(root, runas, False, self.identifier)
        root.wait_window(dialog.top)

        # self.reload_tree()
        # self.delete_tree_wf()
        # self.delete_tree_xfer()
        self.Tree_Select(self.route_selected)
        self.reload_tree_xfer()

    def Button_Xfer_Delete_Click(self):
        ''' Button Xfer Delete '''
        db_xfer.delete_XFERO_Xfer(self.identifier_xfer)

        # self.reload_tree()
        # self.delete_tree_wf()
        # self.delete_tree_xfer()
        self.Tree_Select(self.route_selected)
        self.reload_tree_xfer()

    def Button_Xfer_Edit_Click(self):
        ''' Button Xfer Edit '''
        runas = 'edit'
        root.update()

        dialog = XferDialog(root, runas, self.identifier_xfer, self.xfer_route,
                            self.xfer_cotspattern, self.xfer_partner,
                            self.xfer_cmd, self.xfer_params, self.xfer_delsrc)
        root.wait_window(dialog.top)

        # self.reload_tree()
        # self.delete_tree_wf()
        # self.delete_tree_xfer()
        self.Tree_Select(self.route_selected)
        self.reload_tree_xfer()

if __name__ == '__main__':
    vp_start_gui()
