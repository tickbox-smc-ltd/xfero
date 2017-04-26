#!/usr/bin/env python
'''

**Purpose:**

This script is the GUI Screen for managing Scheduled Tasks.

**Unit Test Module:** None

*External dependencies*

    /xfero/
      db
        manage_schedule (/xfero/.gui.xfero_scheduled_task)

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+

'''

from tkinter import Tk, Label, Entry, Button, Toplevel
from tkinter import END, TOP, BOTH, Y, VERTICAL, HORIZONTAL, NSEW, NS, EW
import tkinter.ttk as ttk
from tkinter.font import Font
import sys
from /xfero/.db import manage_schedule as db_schedule

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global win, root
    root = Tk()
    root.title('XFERO_Scheduler')
    root.geometry('600x518+128+119')
    win = XFERO_Scheduler(root)
    init()
    root.mainloop()

win = None

def create_XFERO_Scheduler(root):

    '''Starting point when module is imported by another program.'''
    global win, w_win
    if win:  # So we have only one instance of window.
        return
    win = Toplevel(root)
    win.title('XFERO_Scheduler')
    win.geometry('600x518+128+119')
    w_win = XFERO_Scheduler(win)
    init()
    return w_win

def destroy_XFERO_Scheduler():
    ''' destroy dialogue'''
    global win
    win.destroy()
    win = None

def init():
    ''' init '''
    pass

class XFERO_Scheduler:
    ''' class scheduler '''
    def __init__(self, master=None):
        ''' init '''
        _compcolor = '#ffffff'  # X11 color: #ffffff
        _ana2color = '#ffffff'  # X11 color: #ffffff
        self.data = ''
        self.identifier = ''
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        # self.style.configure('.',background=_bgcolor)
        # self.style.configure('.',foreground=_fgcolor)
        # self.style.configure('.',font=font10)
        self.style.map('.', background=[('selected', _compcolor),
                                        ('active', _ana2color)])
        master.configure(highlightcolor="black")

        self.TLabelframe1 = ttk.Labelframe(master)
        self.TLabelframe1.place(relx=0.07, rely=0.06, relheight=0.4,
                                relwidth=0.87)
        self.TLabelframe1.configure(text='''Scheduled Tasks''')
        self.TLabelframe1.configure(width=520)

        frame = ttk.Frame(self.TLabelframe1)
        frame.pack(side=TOP, fill=BOTH, expand=Y)

        # create the tree and scrollbars
        self.dataCols = ('ID', 'Task Name', 'Function', 'Year', 'Month', 'Day',
                         'Week', 'Day of Week', 'Hour', 'Minute', 'Second',
                         'Arguments', 'Active')

        self.tree = ttk.Treeview(self.TLabelframe1)
        self.tree.configure(columns=self.dataCols)
        self.tree.configure(show='headings')

        ysb = ttk.Scrollbar(self.TLabelframe1)
        ysb.configure(orient=VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(self.TLabelframe1)
        xsb.configure(orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

        # add tree and scrollbars to frame
        self.tree.grid(in_=frame, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=frame, row=0, column=1, sticky=NS)
        xsb.grid(in_=frame, row=1, column=0, sticky=EW)

        # set frame resize priorities
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self._load_data()

        self.tree.bind('<Button-1>', self.Tree_Select)

        self.Label1 = Label(master)
        self.Label1.place(relx=0.07, rely=0.5, height=22, width=77)
        self.Label1.configure(activebackground="#ffffff")
        self.Label1.configure(activeforeground="black")
        # self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#bfbfbf")
        # self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#ffffff")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Task Name:''')

        self.Label3 = Label(master)
        self.Label3.place(relx=0.06, rely=0.55, height=22, width=77)
        self.Label3.configure(activebackground="#ffffff")
        self.Label3.configure(activeforeground="black")
        # self.Label3.configure(background=_bgcolor)
        self.Label3.configure(disabledforeground="#bfbfbf")
        # self.Label3.configure(font=font10)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#ffffff")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Function:''')

        self.Label2 = Label(master)
        self.Label2.place(relx=0.04, rely=0.60, height=22, width=77)
        self.Label2.configure(activebackground="#ffffff")
        self.Label2.configure(activeforeground="black")
        # self.Label2.configure(background=_bgcolor)
        self.Label2.configure(disabledforeground="#bfbfbf")
        # self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#ffffff")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Year:''')

        self.Label4 = Label(master)
        self.Label4.place(relx=0.48, rely=0.60, height=22, width=69)
        self.Label4.configure(activebackground="#ffffff")
        self.Label4.configure(activeforeground="black")
        # self.Label4.configure(background=_bgcolor)
        self.Label4.configure(disabledforeground="#bfbfbf")
        # self.Label4.configure(font=font10)
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#ffffff")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Month:''')

        self.Label5 = Label(master)
        self.Label5.place(relx=0.07, rely=0.65, height=22, width=34)
        self.Label5.configure(activebackground="#ffffff")
        self.Label5.configure(activeforeground="black")
        # self.Label5.configure(background=_bgcolor)
        self.Label5.configure(disabledforeground="#bfbfbf")
        # self.Label5.configure(font=font10)
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(highlightbackground="#ffffff")
        self.Label5.configure(highlightcolor="black")
        self.Label5.configure(text='''Day:''')

        self.Label6 = Label(master)
        self.Label6.place(relx=0.5, rely=0.65, height=22, width=44)
        self.Label6.configure(activebackground="#ffffff")
        self.Label6.configure(activeforeground="black")
        # self.Label6.configure(background=_bgcolor)
        self.Label6.configure(disabledforeground="#bfbfbf")
        # self.Label6.configure(font=font10)
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(highlightbackground="#ffffff")
        self.Label6.configure(highlightcolor="black")
        self.Label6.configure(text='''Week:''')

        self.Label7 = Label(master)
        self.Label7.place(relx=0.07, rely=0.70, height=22, width=89)
        self.Label7.configure(activebackground="#ffffff")
        self.Label7.configure(activeforeground="black")
        # self.Label7.configure(background=_bgcolor)
        self.Label7.configure(disabledforeground="#bfbfbf")
        # self.Label7.configure(font=font10)
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(highlightbackground="#ffffff")
        self.Label7.configure(highlightcolor="black")
        self.Label7.configure(text='''Day of Week:''')

        self.Label8 = Label(master)
        self.Label8.place(relx=0.5, rely=0.70, height=22, width=42)
        self.Label8.configure(activebackground="#ffffff")
        self.Label8.configure(activeforeground="black")
        # self.Label8.configure(background=_bgcolor)
        self.Label8.configure(disabledforeground="#bfbfbf")
        # self.Label8.configure(font=font10)
        self.Label8.configure(foreground="#000000")
        self.Label8.configure(highlightbackground="#ffffff")
        self.Label8.configure(highlightcolor="black")
        self.Label8.configure(text='''Hour:''')

        self.Label9 = Label(master)
        self.Label9.place(relx=0.07, rely=0.75, height=22, width=54)
        self.Label9.configure(activebackground="#ffffff")
        self.Label9.configure(activeforeground="black")
        # self.Label9.configure(background=_bgcolor)
        self.Label9.configure(disabledforeground="#bfbfbf")
        # self.Label9.configure(font=font10)
        self.Label9.configure(foreground="#000000")
        self.Label9.configure(highlightbackground="#ffffff")
        self.Label9.configure(highlightcolor="black")
        self.Label9.configure(text='''Minute:''')

        self.Label10 = Label(master)
        self.Label10.place(relx=0.5, rely=0.75, height=22, width=56)
        self.Label10.configure(activebackground="#ffffff")
        self.Label10.configure(activeforeground="black")
        # self.Label10.configure(background=_bgcolor)
        self.Label10.configure(disabledforeground="#bfbfbf")
        # self.Label10.configure(font=font10)
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(highlightbackground="#ffffff")
        self.Label10.configure(highlightcolor="black")
        self.Label10.configure(text='''Second:''')

        self.Label11 = Label(master)
        self.Label11.place(relx=0.07, rely=0.80, height=22, width=80)
        self.Label11.configure(activebackground="#ffffff")
        self.Label11.configure(activeforeground="black")
        # self.Label11.configure(background=_bgcolor)
        self.Label11.configure(disabledforeground="#bfbfbf")
        # self.Label11.configure(font=font10)
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(highlightbackground="#ffffff")
        self.Label11.configure(highlightcolor="black")
        self.Label11.configure(text='''Arguments:''')

        self.Label12 = Label(master)
        self.Label12.place(relx=0.5, rely=0.80, height=22, width=49)
        self.Label12.configure(activebackground="#ffffff")
        self.Label12.configure(activeforeground="black")
        # self.Label12.configure(background=_bgcolor)
        self.Label12.configure(disabledforeground="#bfbfbf")
        # self.Label12.configure(font=font10)
        self.Label12.configure(foreground="#000000")
        self.Label12.configure(highlightbackground="#ffffff")
        self.Label12.configure(highlightcolor="black")
        self.Label12.configure(text='''Active:''')

        self.Entry_Task_Name = Entry(master)
        self.Entry_Task_Name.place(relx=0.28, rely=0.5, relheight=0.05,
                                   relwidth=0.65)
        self.Entry_Task_Name.configure(background="white")
        self.Entry_Task_Name.configure(disabledforeground="#bfbfbf")
        # self.Entry_Task_Name.configure(font=font11)
        self.Entry_Task_Name.configure(foreground="#000000")
        self.Entry_Task_Name.configure(highlightcolor="black")
        self.Entry_Task_Name.configure(insertbackground="black")
        self.Entry_Task_Name.configure(selectbackground="#e6e6e6")
        self.Entry_Task_Name.configure(selectforeground="black")

        self.Entry_Function = Entry(master)
        self.Entry_Function.place(relx=0.28, rely=0.55, relheight=0.05,
                                  relwidth=0.65)
        self.Entry_Function.configure(background="white")
        self.Entry_Function.configure(disabledforeground="#bfbfbf")
        # self.Entry_Function.configure(font=font11)
        self.Entry_Function.configure(foreground="#000000")
        self.Entry_Function.configure(highlightcolor="black")
        self.Entry_Function.configure(insertbackground="black")
        self.Entry_Function.configure(selectbackground="#e6e6e6")
        self.Entry_Function.configure(selectforeground="black")

        self.Entry_Year = Entry(master)
        self.Entry_Year.place(relx=0.28, rely=0.60, relheight=0.05,
                              relwidth=0.2)
        self.Entry_Year.configure(background="white")
        self.Entry_Year.configure(disabledforeground="#bfbfbf")
        # self.Entry_Year.configure(font=font11)
        self.Entry_Year.configure(foreground="#000000")
        self.Entry_Year.configure(highlightcolor="black")
        self.Entry_Year.configure(insertbackground="black")
        self.Entry_Year.configure(selectbackground="#e6e6e6")
        self.Entry_Year.configure(selectforeground="black")

        self.Entry_Month = Entry(master)
        self.Entry_Month.place(relx=0.70, rely=0.60, relheight=0.05,
                               relwidth=0.23)
        self.Entry_Month.configure(background="white")
        self.Entry_Month.configure(disabledforeground="#bfbfbf")
        # self.Entry_Month.configure(font=font11)
        self.Entry_Month.configure(foreground="#000000")
        self.Entry_Month.configure(highlightcolor="black")
        self.Entry_Month.configure(insertbackground="black")
        self.Entry_Month.configure(selectbackground="#e6e6e6")
        self.Entry_Month.configure(selectforeground="black")

        self.Entry_Day = Entry(master)
        self.Entry_Day.place(relx=0.28, rely=0.65, relheight=0.05, relwidth=0.2)
        self.Entry_Day.configure(background="white")
        self.Entry_Day.configure(disabledforeground="#bfbfbf")
        # self.Entry_Day.configure(font=font11)
        self.Entry_Day.configure(foreground="#000000")
        self.Entry_Day.configure(highlightcolor="black")
        self.Entry_Day.configure(insertbackground="black")
        self.Entry_Day.configure(selectbackground="#e6e6e6")
        self.Entry_Day.configure(selectforeground="black")

        self.Entry_Week = Entry(master)
        self.Entry_Week.place(relx=0.70, rely=0.65, relheight=0.05,
                              relwidth=0.23)
        self.Entry_Week.configure(background="white")
        self.Entry_Week.configure(disabledforeground="#bfbfbf")
        # self.Entry_Week.configure(font=font11)
        self.Entry_Week.configure(foreground="#000000")
        self.Entry_Week.configure(highlightcolor="black")
        self.Entry_Week.configure(insertbackground="black")
        self.Entry_Week.configure(selectbackground="#e6e6e6")
        self.Entry_Week.configure(selectforeground="black")

        self.Entry_Day_of_Week = Entry(master)
        self.Entry_Day_of_Week.place(relx=0.28, rely=0.70, relheight=0.05,
                                     relwidth=0.2)
        self.Entry_Day_of_Week.configure(background="white")
        self.Entry_Day_of_Week.configure(disabledforeground="#bfbfbf")
        # self.Entry_Day_of_Week.configure(font=font11)
        self.Entry_Day_of_Week.configure(foreground="#000000")
        self.Entry_Day_of_Week.configure(highlightcolor="black")
        self.Entry_Day_of_Week.configure(insertbackground="black")
        self.Entry_Day_of_Week.configure(selectbackground="#e6e6e6")
        self.Entry_Day_of_Week.configure(selectforeground="black")

        self.Entry_Hour = Entry(master)
        self.Entry_Hour.place(relx=0.70, rely=0.70, relheight=0.05,
                              relwidth=0.23)
        self.Entry_Hour.configure(background="white")
        self.Entry_Hour.configure(disabledforeground="#bfbfbf")
        # self.Entry_Hour.configure(font=font11)
        self.Entry_Hour.configure(foreground="#000000")
        self.Entry_Hour.configure(highlightcolor="black")
        self.Entry_Hour.configure(insertbackground="black")
        self.Entry_Hour.configure(selectbackground="#e6e6e6")
        self.Entry_Hour.configure(selectforeground="black")
        self.Entry_Hour.configure(width=120)

        self.Entry_Minute = Entry(master)
        self.Entry_Minute.place(relx=0.28, rely=0.75, relheight=0.05,
                                relwidth=0.2)
        self.Entry_Minute.configure(background="white")
        self.Entry_Minute.configure(disabledforeground="#bfbfbf")
        # self.Entry_Minute.configure(font=font11)
        self.Entry_Minute.configure(foreground="#000000")
        self.Entry_Minute.configure(highlightcolor="black")
        self.Entry_Minute.configure(insertbackground="black")
        self.Entry_Minute.configure(selectbackground="#e6e6e6")
        self.Entry_Minute.configure(selectforeground="black")

        self.Entry_Second = Entry(master)
        self.Entry_Second.place(relx=0.70, rely=0.75, relheight=0.05,
                                relwidth=0.23)
        self.Entry_Second.configure(background="white")
        self.Entry_Second.configure(disabledforeground="#bfbfbf")
        # self.Entry_Second.configure(font=font11)
        self.Entry_Second.configure(foreground="#000000")
        self.Entry_Second.configure(highlightcolor="black")
        self.Entry_Second.configure(insertbackground="black")
        self.Entry_Second.configure(selectbackground="#e6e6e6")
        self.Entry_Second.configure(selectforeground="black")

        self.Entry_Args = Entry(master)
        self.Entry_Args.place(relx=0.28, rely=0.80, relheight=0.05,
                              relwidth=0.2)
        self.Entry_Args.configure(background="white")
        self.Entry_Args.configure(disabledforeground="#bfbfbf")
        # self.Entry_Args.configure(font=font11)
        self.Entry_Args.configure(foreground="#000000")
        self.Entry_Args.configure(highlightcolor="black")
        self.Entry_Args.configure(insertbackground="black")
        self.Entry_Args.configure(selectbackground="#e6e6e6")
        self.Entry_Args.configure(selectforeground="black")

        self.Entry_Active = Entry(master)
        self.Entry_Active.place(relx=0.70, rely=0.80, relheight=0.05,
                                relwidth=0.23)
        self.Entry_Active.configure(background="white")
        self.Entry_Active.configure(disabledforeground="#bfbfbf")
        # self.Entry_Active.configure(font=font11)
        self.Entry_Active.configure(foreground="#000000")
        self.Entry_Active.configure(highlightcolor="black")
        self.Entry_Active.configure(insertbackground="black")
        self.Entry_Active.configure(selectbackground="#e6e6e6")
        self.Entry_Active.configure(selectforeground="black")

        self.Button_Add = Button(master)
        self.Button_Add.place(relx=0.83, rely=0.88, height=28, width=54)
        self.Button_Add.configure(activebackground="#ffffff")
        self.Button_Add.configure(activeforeground="#000000")
        # self.Button_Add.configure(background=_bgcolor)
        self.Button_Add.configure(disabledforeground="#bfbfbf")
        # self.Button_Add.configure(font=font10)
        self.Button_Add.configure(foreground="#000000")
        self.Button_Add.configure(highlightbackground="#ffffff")
        self.Button_Add.configure(highlightcolor="black")
        self.Button_Add.configure(text='''Add''')
        self.Button_Add.configure(command=self.Button_Add_Click)

        self.Button_Cancel = Button(master)
        self.Button_Cancel.place(relx=0.48, rely=0.88, height=28, width=70)
        self.Button_Cancel.configure(activebackground="#ffffff")
        self.Button_Cancel.configure(activeforeground="#000000")
        # self.Button_Cancel.configure(background=_bgcolor)
        self.Button_Cancel.configure(disabledforeground="#bfbfbf")
        # self.Button_Cancel.configure(font=font10)
        self.Button_Cancel.configure(foreground="#000000")
        self.Button_Cancel.configure(highlightbackground="#ffffff")
        self.Button_Cancel.configure(highlightcolor="black")
        self.Button_Cancel.configure(text='''Cancel''')
        self.Button_Cancel.configure(command=self.Button_Cancel_Click)

        self.Button_Update = Button(master)
        self.Button_Update.place(relx=0.71, rely=0.88, height=28, width=73)
        self.Button_Update.configure(activebackground="#ffffff")
        self.Button_Update.configure(activeforeground="#000000")
        # self.Button_Update.configure(background=_bgcolor)
        self.Button_Update.configure(disabledforeground="#bfbfbf")
        # self.Button_Update.configure(font=font10)
        self.Button_Update.configure(foreground="#000000")
        self.Button_Update.configure(highlightbackground="#ffffff")
        self.Button_Update.configure(highlightcolor="black")
        self.Button_Update.configure(state="disabled")
        self.Button_Update.configure(text='''Update''')
        self.Button_Update.configure(command=self.Button_Update_Click)

        self.Button_Delete = Button(master)
        self.Button_Delete.place(relx=0.6, rely=0.88, height=28, width=68)
        self.Button_Delete.configure(activebackground="#ffffff")
        self.Button_Delete.configure(activeforeground="#000000")
        # self.Button_Delete.configure(background=_bgcolor)
        self.Button_Delete.configure(disabledforeground="#bfbfbf")
        # self.Button_Delete.configure(font=font10)
        self.Button_Delete.configure(foreground="#000000")
        self.Button_Delete.configure(highlightbackground="#ffffff")
        self.Button_Delete.configure(highlightcolor="black")
        self.Button_Delete.configure(state="disabled")
        self.Button_Delete.configure(text='''Delete''')
        self.Button_Delete.configure(command=self.Button_Delete_Click)

    def Button_Add_Click(self):
        '''button add'''
        sched_task_name = self.Entry_Task_Name.get()
        sched_function = self.Entry_Function.get()
        sched_year = self.Entry_Year.get()
        sched_month = self.Entry_Month.get()
        sched_day = self.Entry_Day.get()
        sched_week = self.Entry_Week.get()
        sched_day_of_week = self.Entry_Day_of_Week.get()
        sched_hour = self.Entry_Hour.get()
        sched_minute = self.Entry_Minute.get()
        sched_second = self.Entry_Second.get()
        sched_args = self.Entry_Args.get()
        sched_active = self.Entry_Active.get()

        result = db_schedule.create_XFERO_Scheduled_Task(sched_task_name,
                                                      sched_function,
                                                      sched_year, sched_month,
                                                      sched_day, sched_week,
                                                      sched_day_of_week,
                                                      sched_hour, sched_minute,
                                                      sched_second, sched_args,
                                                      sched_active)

        self.reload_tree()

    def Button_Cancel_Click(self):
        '''button cancel'''
        # print ('Button_Cancel_Click')
        root.destroy()

    def Button_Delete_Click(self):
        '''button delete'''
        # print ('Button_Delete_Click')
        # print('ID to delete %s' % self.identifier)
        # Delete Row
        result = db_schedule.delete_XFERO_Scheduled_Task(self.identifier)

        self.reload_tree()

    def Button_Update_Click(self):
        '''button update'''
        # print ('Button_Update_Click')
        # print('ID to update %s' % self.identifier)

        sched_task_name = self.Entry_Task_Name.get()
        sched_function = self.Entry_Function.get()
        sched_year = self.Entry_Year.get()
        sched_month = self.Entry_Month.get()
        sched_day = self.Entry_Day.get()
        sched_week = self.Entry_Week.get()
        sched_day_of_week = self.Entry_Day_of_Week.get()
        sched_hour = self.Entry_Hour.get()
        sched_minute = self.Entry_Minute.get()
        sched_second = self.Entry_Second.get()
        sched_args = self.Entry_Args.get()
        sched_active = self.Entry_Active.get()

        result = db_schedule.update_XFERO_Scheduled_Task(self.identifier,
                                                      sched_task_name,
                                                      sched_function,
                                                      sched_year, sched_month,
                                                      sched_day, sched_week,
                                                      sched_day_of_week,
                                                      sched_hour, sched_minute,
                                                      sched_second, sched_args,
                                                      sched_active)

        self.reload_tree()

    def reload_tree(self):
        '''reload tree'''
        # Delete treview items
        tree_list = self.tree.get_children()
        for tree in tree_list:
            self.tree.delete(tree)
        # reload treview with new row
        self._load_data()
        # self.tree.bind('<Button-1>', self.Tree_Select)

        # Clear entry fields
        self.Entry_Task_Name.delete(0, END)
        self.Entry_Function.delete(0, END)
        self.Entry_Year.delete(0, END)
        self.Entry_Month.delete(0, END)
        self.Entry_Day.delete(0, END)
        self.Entry_Week.delete(0, END)
        self.Entry_Day_of_Week.delete(0, END)
        self.Entry_Hour.delete(0, END)
        self.Entry_Minute.delete(0, END)
        self.Entry_Second.delete(0, END)
        self.Entry_Args.delete(0, END)
        self.Entry_Active.delete(0, END)

        self.Button_Delete.configure(state="disabled")
        self.Button_Update.configure(state="disabled")

    def Tree_Select(self, p1_tree):
        '''Tree_Select '''
        self.Entry_Task_Name.delete(0, END)
        self.Entry_Function.delete(0, END)
        self.Entry_Year.delete(0, END)
        self.Entry_Month.delete(0, END)
        self.Entry_Day.delete(0, END)
        self.Entry_Week.delete(0, END)
        self.Entry_Day_of_Week.delete(0, END)
        self.Entry_Hour.delete(0, END)
        self.Entry_Minute.delete(0, END)
        self.Entry_Second.delete(0, END)
        self.Entry_Args.delete(0, END)
        self.Entry_Active.delete(0, END)

        self.Button_Update.configure(state="normal")
        self.Button_Delete.configure(state="normal")

        item = self.tree.identify('item', p1_tree.x, p1_tree.y)
        values = self.tree.item(item, 'values')

        if values:
            self.identifier = values[0]
            self.Entry_Task_Name.insert(0, values[1])
            self.Entry_Function.insert(0, values[2])
            self.Entry_Year.insert(0, values[3])
            self.Entry_Month.insert(0, values[4])
            self.Entry_Day.insert(0, values[5])
            self.Entry_Week.insert(0, values[6])
            self.Entry_Day_of_Week.insert(0, values[7])
            self.Entry_Hour.insert(0, values[8])
            self.Entry_Minute.insert(0, values[9])
            self.Entry_Second.insert(0, values[10])
            self.Entry_Args.insert(0, values[11])
            self.Entry_Active.insert(0, values[12])

        sys.stdout.flush()

    def _load_data(self):
        '''load data'''
        self.data = db_schedule.list_XFERO_Scheduled_Task()

        # configure column headings
        for col in self.dataCols:
            self.tree.heading(col, text=col.title(),
                              command=lambda col=col:
                              self._column_sort(col, XFERO_Scheduler.SortDir))
            self.tree.column(col, width=Font().measure(col.title()))

        # add data to the tree
        for item in self.data:
            self.tree.insert('', 'end', values=item)
            # and adjust column widths if necessary
            for idx, val in enumerate(item):
                iwidth = Font().measure(val)
                if self.tree.column(self.dataCols[idx], 'width') < iwidth:
                    self.tree.column(self.dataCols[idx], width=iwidth)

    def _column_sort(self, col, descending=False):
        '''columns sort'''
        data = [(self.tree.set(child, col), child) for
                child in self.tree.get_children('')]
        # reorder data
        # tkinter looks after moving other items in
        # the same row
        data.sort(reverse=descending)

        for indx, item in enumerate(data):
            self.tree.move(item[1], '', indx)   # item[1] = item Identifier

        # reverse sort direction for next sort operation
        XFERO_Scheduler.SortDir = not descending

if __name__ == '__main__':

    vp_start_gui()
