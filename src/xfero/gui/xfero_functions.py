#!/usr/bin/env python
'''

**Purpose:**

This script is the GUI Screen for managing transformation functions of XFERO.

**Unit Test Module:** None

*External dependencies*

    /xfero/
      db
        manage_function (/xfero/.gui.xfero_functions)

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+
| 11/05/2014 | Chris Falck | Added class entry field to the gui                |
+------------+-------------+---------------------------------------------------+

'''
from tkinter import Tk, Label, Entry, Button, Toplevel, sys
from tkinter import END, TOP, BOTH, Y, VERTICAL, HORIZONTAL, NSEW, NS, EW
import tkinter.ttk as ttk
from tkinter.font import Font
from /xfero/.db import manage_function as db_function


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global win, root
    root = Tk()
    root.title('Functions')
    root.geometry('607x500+128+119')
    win = XFERO_Functions(root)
    init()
    root.mainloop()

win = None

def create_XFERO_Functions(root):
    '''Starting point when module is imported by another program.'''
    global win, w_win
    if win:  # So we have only one instance of window.
        return
    win = Toplevel(root)
    win.title('Functions')
    win.geometry('607x500+128+119')
    w_win = XFERO_Functions(win)
    init()
    return w_win

def destroy_XFERO_Functions():
    '''destroy window'''
    global win
    win.destroy()
    win = None

def init():
    '''initialisation'''
    pass

class XFERO_Functions:
    '''Functions class'''
    # header sort
    SortDir = True     # descending
    
    def __init__(self, master=None):
        '''Initialise Functions class'''
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
        self.style.map(
            '.', background=[('selected', _compcolor), ('active', _ana2color)])
        master.configure(highlightcolor="black")

        self.TLabelframe1 = ttk.Labelframe(master)
        self.TLabelframe1.place(
            relx=0.07, rely=0.07, relheight=0.58, relwidth=0.86)
        self.TLabelframe1.configure(text='''Functions''')
        self.TLabelframe1.configure(width=520)

        frame = ttk.Frame(self.TLabelframe1)
        frame.pack(side=TOP, fill=BOTH, expand=Y)

        # create the tree and scrollbars
        self.dataCols = (
            'Identifier', 'Function Name', 'Class Name', 'Description',
            'Prototype')

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
        self.Label1.place(relx=0.05, rely=0.70, height=22, width=109)
        # self.Label1.configure(activebackground="#ffffff")
        # self.Label1.configure(activeforeground="black")
        # self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#bfbfbf")
        # self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#000000")
        # self.Label1.configure(highlightbackground="#ffffff")
        # self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Function Name:''')

        self.Label2 = Label(master)
        self.Label2.place(relx=0.44, rely=0.70, height=22, width=109)
        # self.Label2.configure(activebackground="#ffffff")
        # self.Label2.configure(activeforeground="black")
        # self.Label2.configure(background=_bgcolor)
        self.Label2.configure(disabledforeground="#bfbfbf")
        # self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        # self.Label2.configure(highlightbackground="#ffffff")
        # self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Description:''')

        self.Label4 = Label(master)
        self.Label4.place(relx=0.05, rely=0.77, height=22, width=109)
        # self.Label4.configure(activebackground="#ffffff")
        # self.Label4.configure(activeforeground="black")
        # self.Label4.configure(background=_bgcolor)
        self.Label4.configure(disabledforeground="#bfbfbf")
        # self.Label4.configure(font=font10)
        self.Label4.configure(foreground="#000000")
        # self.Label4.configure(highlightbackground="#ffffff")
        # self.Label$.configure(highlightcolor="black")
        self.Label4.configure(text='''Class:''')

        self.Label3 = Label(master)
        self.Label3.place(relx=0.05, rely=0.84, height=22, width=109)
        # self.Label3.configure(activebackground="#ffffff")
        # self.Label3.configure(activeforeground="black")
        # self.Label3.configure(background=_bgcolor)
        self.Label3.configure(disabledforeground="#bfbfbf")
        # self.Label3.configure(font=font10)
        self.Label3.configure(foreground="#000000")
        # self.Label3.configure(highlightbackground="#ffffff")
        # self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Prototype:''')

        self.Entry_Function_Name = Entry(master)
        self.Entry_Function_Name.place(
            relx=0.23, rely=0.69, relheight=0.07, relwidth=0.22)
        self.Entry_Function_Name.configure(background="white")
        self.Entry_Function_Name.configure(disabledforeground="#bfbfbf")
        # self.Entry_Function_Name.configure(font=font11)
        self.Entry_Function_Name.configure(foreground="#000000")
        # self.Entry_Function_Name.configure(highlightcolor="black")
        self.Entry_Function_Name.configure(insertbackground="black")
        # self.Entry_Function_Name.configure(selectbackground="#e6e6e6")
        # self.Entry_Function_Name.configure(selectforeground="black")

        self.Entry_Function_Description = Entry(master)
        self.Entry_Function_Description.place(
            relx=0.60, rely=0.69, relheight=0.07, relwidth=0.34)
        self.Entry_Function_Description.configure(background="white")
        self.Entry_Function_Description.configure(disabledforeground="#bfbfbf")
        # self.Entry_Function_Description.configure(font=font11)
        self.Entry_Function_Description.configure(foreground="#000000")
        # self.Entry_Function_Description.configure(highlightcolor="black")
        self.Entry_Function_Description.configure(insertbackground="black")
        # self.Entry_Function_Description.configure(selectbackground="#e6e6e6")
        # self.Entry_Function_Description.configure(selectforeground="black")
        self.Entry_Function_Description.configure(width=217)

        self.Entry_Function_Class = Entry(master)
        self.Entry_Function_Class.place(
            relx=0.23, rely=0.76, relheight=0.07, relwidth=0.34)
        self.Entry_Function_Class.configure(background="white")
        self.Entry_Function_Class.configure(disabledforeground="#bfbfbf")
        # self.Entry_Function_Class.configure(font=font11)
        self.Entry_Function_Class.configure(foreground="#000000")
        # self.Entry_Function_Class.configure(highlightcolor="black")
        self.Entry_Function_Class.configure(insertbackground="black")
        # self.Entry_Function_Class.configure(selectbackground="#e6e6e6")
        # self.Entry_Function_Class.configure(selectforeground="black")
        self.Entry_Function_Description.configure(width=217)

        self.Entry_Function_Prototype = Entry(master)
        self.Entry_Function_Prototype.place(
            relx=0.23, rely=0.83, relheight=0.07, relwidth=0.71)
        self.Entry_Function_Prototype.configure(background="white")
        self.Entry_Function_Prototype.configure(disabledforeground="#bfbfbf")
        # self.Entry_Function_Prototype.configure(font=font11)
        self.Entry_Function_Prototype.configure(foreground="#000000")
        # self.Entry_Function_Prototype.configure(highlightcolor="black")
        self.Entry_Function_Prototype.configure(insertbackground="black")
        # self.Entry_Function_Prototype.configure(selectbackground="#e6e6e6")
        # self.Entry_Function_Prototype.configure(selectforeground="black")
        self.Entry_Function_Prototype.configure(width=402)

        self.Button_Add = Button(master)
        self.Button_Add.place(relx=0.83, rely=0.92, height=28, width=54)
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
        self.Button_Cancel.place(relx=0.48, rely=0.92, height=28, width=70)
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
        self.Button_Update.place(relx=0.71, rely=0.92, height=28, width=73)
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
        self.Button_Delete.place(relx=0.6, rely=0.92, height=28, width=68)
        self.Button_Delete.configure(activebackground="#ffffff")
        self.Button_Delete.configure(activeforeground="#000000")
        # self.Button_Delete.configure(background=_bgcolor)
        self.Button_Delete.configure(disabledforeground="#bfbfbf")
        # sself.Button_Delete.configure(font=font10)
        self.Button_Delete.configure(foreground="#000000")
        self.Button_Delete.configure(highlightbackground="#ffffff")
        self.Button_Delete.configure(highlightcolor="black")
        self.Button_Delete.configure(state="disabled")
        self.Button_Delete.configure(text='''Delete''')
        self.Button_Delete.configure(command=self.Button_Delete_Click)

    def Button_Add_Click(self):
        '''Button add click'''
        func_name = self.Entry_Function_Name.get()
        func_description = self.Entry_Function_Description.get()
        func_class = self.Entry_Function_Class.get()
        func_prototype = self.Entry_Function_Prototype.get()

        result = db_function.create_XFERO_Function(
            func_name, func_class, func_description, func_prototype)

        self.reload_tree()

    def Button_Cancel_Click(self):
        '''Button cancel click'''
        root.destroy()

    def Button_Delete_Click(self):
        '''Button delete click'''
        result = db_function.delete_XFERO_Function(self.identifier)

        self.reload_tree()

    def Button_Update_Click(self):
        '''Button Update click'''
        func_name = self.Entry_Function_Name.get()
        func_description = self.Entry_Function_Description.get()
        func_class = self.Entry_Function_Class.get()
        func_prototype = self.Entry_Function_Prototype.get()

        result = db_function.update_XFERO_Function(
            self.identifier, func_class, func_name, func_description,
            func_prototype)

        self.reload_tree()

    def reload_tree(self):
        '''reload tree'''
        # Delete treview items
        tree_list = self.tree.get_children()
        for tree in tree_list:
            self.tree.delete(tree)
        # reload treview with new row
        self._load_data()

        # Clear entry fields
        self.Entry_Function_Name.delete(0, END)
        self.Entry_Function_Description.delete(0, END)
        self.Entry_Function_Prototype.delete(0, END)
        self.Entry_Function_Class.delete(0, END)

        self.Button_Delete.configure(state="disabled")
        self.Button_Update.configure(state="disabled")

    def Tree_Select(self, p1_tree):
        '''tree select'''
        self.Entry_Function_Name.delete(0, END)
        self.Entry_Function_Description.delete(0, END)
        self.Entry_Function_Prototype.delete(0, END)
        self.Entry_Function_Class.delete(0, END)

        self.Button_Update.configure(state="normal")
        self.Button_Delete.configure(state="normal")

        item = self.tree.identify('item', p1_tree.x, p1_tree.y)

        values = self.tree.item(item, 'values')
        if values:
            self.identifier = values[0]
            self.Entry_Function_Name.insert(0, values[1])
            self.Entry_Function_Description.insert(0, values[3])
            self.Entry_Function_Class.insert(0, values[2])
            self.Entry_Function_Prototype.insert(0, values[4])

        sys.stdout.flush()

    def _load_data(self):
        '''load data'''
        self.data = db_function.list_XFERO_Function()

        # configure column headings
        for col in self.dataCols:
            self.tree.heading(col, text=col.title(),
                              command=lambda col=col:
                              self._column_sort(col, XFERO_Functions.SortDir))
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
        '''column sorting'''
        data = [(self.tree.set(child, col), child)
                for child in self.tree.get_children('')]

        # reorder data
        # tkinter looks after moving other items in
        # the same row
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            self.tree.move(item[1], '', indx)

        # reverse sort direction for next sort operation
        XFERO_Functions.SortDir = not descending

if __name__ == '__main__':
    vp_start_gui()
