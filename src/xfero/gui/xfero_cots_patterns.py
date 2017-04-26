#!/usr/bin/env python
'''

**Purpose:**

This script is the GUI Screen for managing COTS prototypes.

**Unit Test Module:** None

*External dependencies*

    /xfero/
      db
        manage_cots_pattern (/xfero/.gui.xfero_cots_patterns)

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+

'''
from tkinter import Tk, Label, Entry, Button, Toplevel, sys
from tkinter import END, TOP, BOTH, Y, VERTICAL, HORIZONTAL, NSEW, NS, EW
import tkinter.ttk as ttk
from tkinter.font import Font
from /xfero/.db import manage_cots_pattern as db_cots_pattern


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global win, root
    root = Tk()
    root.title('XFERO_COTS_Patterns')
    root.geometry('607x407+128+119')
    win = XFERO_COTS_Patterns(root)
    init()
    root.mainloop()

win = None

def create_XFERO_COTS_Patterns(root):
    '''Starting point when module is imported by another program.'''
    global win, w_win
    if win:  # So we have only one instance of window.
        return
    win = Toplevel(root)
    win.title('XFERO_COTS_Patterns')
    win.geometry('607x407+128+119')
    w_win = XFERO_COTS_Patterns(win)
    init()
    return w_win

def destroy_XFERO_COTS_Patterns():
    '''destroy COTS Patterns'''
    global win
    win.destroy()
    win = None
    return

def init():
    '''Inititalise'''
    pass

class XFERO_COTS_Patterns:
    '''COTS Pattern class'''
    # class variable to track direction of column
    # header sort
    SortDir = True     # descending

    def __init__(self, master=None):
        ''' Class initialisation'''
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
        self.TLabelframe1.configure(text='''COTS Pattern Prototypes''')
        self.TLabelframe1.configure(width=520)

        f = ttk.Frame(self.TLabelframe1)
        f.pack(side=TOP, fill=BOTH, expand=Y)

        # create the tree and scrollbars
        self.dataCols = ('Identifier', 'COTS Product', 'Pattern', 'Parameters')

        self.tree = ttk.Treeview(self.TLabelframe1)
        self.tree.configure(columns=self.dataCols)
        self.tree.configure(show='headings')

        ysb = ttk.Scrollbar(self.TLabelframe1)
        ysb.configure(orient=VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(self.TLabelframe1)
        xsb.configure(orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

        # add tree and scrollbars to frame
        self.tree.grid(in_=f, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=NS)
        xsb.grid(in_=f, row=1, column=0, sticky=EW)

        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)

        # load tree data
        self._load_data()
        # Bind selection
        self.tree.bind('<Button-1>', self.Tree_Select)

        # Configure window objects
        self.Label1 = Label(master)
        self.Label1.place(relx=0.06, rely=0.72, height=22, width=97)
        self.Label1.configure(activebackground="#ffffff")
        self.Label1.configure(activeforeground="black")
        # self.Label1.configure(background=_bgcolor)
        # self.Label1.configure(disabledforeground="#bfbfbf")
        # self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#000000")
        # self.Label1.configure(highlightbackground="#ffffff")
        # self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''COTS Product:''')

        self.Label2 = Label(master)
        self.Label2.place(relx=0.44, rely=0.72, height=22, width=104)
        self.Label2.configure(activebackground="#ffffff")
        self.Label2.configure(activeforeground="black")
        # self.Label2.configure(background=_bgcolor)
        # self.Label2.configure(disabledforeground="#bfbfbf")
        # self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        # self.Label2.configure(highlightbackground="#ffffff")
        # self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Pattern Name:''')

        self.Label3 = Label(master)
        self.Label3.place(relx=0.06, rely=0.81, height=22, width=109)
        self.Label3.configure(activebackground="#ffffff")
        self.Label3.configure(activeforeground="black")
        # self.Label3.configure(background=_bgcolor)
        self.Label3.configure(disabledforeground="#bfbfbf")
        # self.Label3.configure(font=font10)
        self.Label3.configure(foreground="#000000")
        # self.Label3.configure(highlightbackground="#ffffff")
        # self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''COTS Prototype:''')

        self.Entry_Product = Entry(master)
        self.Entry_Product.place(
            relx=0.25, rely=0.71, relheight=0.07, relwidth=0.17)
        self.Entry_Product.configure(background="white")
        self.Entry_Product.configure(disabledforeground="#bfbfbf")
        # self.Entry_Product.configure(font=font11)
        self.Entry_Product.configure(foreground="#000000")
        # self.Entry_Product.configure(highlightcolor="black")
        self.Entry_Product.configure(insertbackground="black")
        # self.Entry_Product.configure(selectbackground="#e6e6e6")
        # self.Entry_Product.configure(selectforeground="black")

        self.Entry_Pattern_Name = Entry(master)
        self.Entry_Pattern_Name.place(
            relx=0.63, rely=0.71, relheight=0.07, relwidth=0.30)
        self.Entry_Pattern_Name.configure(background="white")
        self.Entry_Pattern_Name.configure(disabledforeground="#bfbfbf")
        # self.Entry_Pattern_Name.configure(font=font11)
        self.Entry_Pattern_Name.configure(foreground="#000000")
        # self.Entry_Pattern_Name.configure(highlightcolor="black")
        self.Entry_Pattern_Name.configure(insertbackground="black")
        # self.Entry_Pattern_Name.configure(selectbackground="#e6e6e6")
        # self.Entry_Pattern_Name.configure(selectforeground="black")

        self.Entry_Prototype = Entry(master)
        self.Entry_Prototype.place(
            relx=0.25, rely=0.8, relheight=0.07, relwidth=0.68)
        self.Entry_Prototype.configure(background="white")
        self.Entry_Prototype.configure(disabledforeground="#bfbfbf")
        # self.Entry_Prototype.configure(font=font11)
        self.Entry_Prototype.configure(foreground="#000000")
        # self.Entry_Prototype.configure(highlightcolor="black")
        self.Entry_Prototype.configure(insertbackground="black")
        # self.Entry_Prototype.configure(selectbackground="#e6e6e6")
        # self.Entry_Prototype.configure(selectforeground="black")

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

    def Button_Cancel_Click(self):
        ''' Button Cancel Click'''
        root.destroy()

    def Button_Add_Click(self):
        ''' Button Add Click'''
        cotspattern_product = self.Entry_Product.get()
        cotspattern_pattern_name = self.Entry_Pattern_Name.get()
        cotspattern_params = self.Entry_Prototype.get()

        result = db_cots_pattern.create_XFERO_COTS_Pattern(
            cotspattern_product, cotspattern_pattern_name, cotspattern_params)

        self.reload_tree()

    def Button_Delete_Click(self):
        ''' Button Delete Click'''
        # Delete Row
        result = db_cots_pattern.delete_XFERO_COTS_Pattern(self.identifier)

        self.reload_tree()

    def Button_Update_Click(self):
        ''' Button Update Click'''
        cotspattern_product = self.Entry_Product.get()
        cotspattern_pattern_name = self.Entry_Pattern_Name.get()
        cotspattern_params = self.Entry_Prototype.get()

        result = db_cots_pattern.update_XFERO_COTS_Pattern(
            self.identifier, cotspattern_product, cotspattern_pattern_name,
            cotspattern_params)

        self.reload_tree()

    def reload_tree(self):
        ''' reload tree'''
        # Delete treview items
        tree_list = self.tree.get_children()
        for tree in tree_list:
            self.tree.delete(tree)
        # reload treview with new row
        self._load_data()

        # Clear entry fields
        self.Entry_Product.delete(0, END)
        self.Entry_Pattern_Name.delete(0, END)
        self.Entry_Prototype.delete(0, END)

        self.Button_Delete.configure(state="disabled")
        self.Button_Update.configure(state="disabled")

    def Tree_Select(self, p1_tree):
        ''' Tree select'''
        self.Entry_Product.delete(0, END)
        self.Entry_Pattern_Name.delete(0, END)
        self.Entry_Prototype.delete(0, END)
        self.Button_Update.configure(state="normal")
        self.Button_Delete.configure(state="normal")

        item = self.tree.identify('item', p1_tree.x, p1_tree.y)

        values = self.tree.item(item, 'values')
        if values:
            self.identifier = values[0]
            self.Entry_Product.insert(0, values[1])
            self.Entry_Pattern_Name.insert(0, values[2])
            self.Entry_Prototype.insert(0, values[3])

        sys.stdout.flush()

    def _load_data(self):
        '''load data'''
        self.data = db_cots_pattern.list_XFERO_COTS_Pattern()

        # configure column headings
        for col in self.dataCols:
            self.tree.heading(col, text=col.title(),
                              command=lambda col=col:
                              self._column_sort(col, XFERO_COTS_Patterns.SortDir))
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
        XFERO_COTS_Patterns.SortDir = not descending

if __name__ == '__main__':
    vp_start_gui()
