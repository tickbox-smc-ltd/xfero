#!/usr/bin/env python
'''

**Purpose:**

This script is the GUI Screen for managing Tickbox Information.

**Unit Test Module:** None

+------------+-------------+---------------------------------------------------+
| Date       | Author      | Change Details                                    |
+============+=============+===================================================+
| 02/07/2013 | Chris Falck | Created                                           |
+------------+-------------+---------------------------------------------------+

'''

from tkinter import Tk, Toplevel, END, SE, Text, Pack, Grid, Place
import tkinter.ttk as ttk

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global win, root
    root = Tk()
    root.title('About Tickbox SMC Limited')
    root.geometry('400x200+785+197')
    win = TickboxSMC(root)
    init()
    root.mainloop()

win = None

def create_TickboxSMC(root):
    '''Starting point when module is imported by another program.'''
    global win, w_win
    if win:  # So we have only one instance of window.
        return
    win = Toplevel(root)
    win.title('About Tickbox SMC Limited')
    win.geometry('400x200+785+197')
    w_win = TickboxSMC(win)
    init()
    return w_win

def destroy_TickboxSMC():
    '''destroy dialogue'''
    global win
    win.destroy()
    win = None

def init():
    '''init'''
    pass

def load_TickboxSMC(root):
    '''Note that the following paragraphs of the help message are each
    a single line of text. The scrolled text box is configured with
    'wrap="word"' to keep thing correct when the help window is resized.'''
    help_box = '''
Tickbox SMC Limited is an IT Company based in Lancashire, UK, 
that specialises in File Transfer Integration

Website   : http://www.tickboxconsulting.com
Email     : support@tickboxconsulting.com

'''

    root.insert(END, help_box)


def close():
    '''destroy dialogue'''
    destroy_TickboxSMC()

class TickboxSMC:
    '''Tickbox Class '''
    def __init__(self, master=None):
        '''init'''
        _compcolor = '#ffffff'  # X11 color: #ffffff
        _ana2color = '#ffffff'  # X11 color: #ffffff

        self.style = ttk.Style()
        # self.style.configure('.',background=_bgcolor)
        # self.style.configure('.',foreground=_fgcolor)
        # self.style.configure('.',font=font10)
        self.style.map(
            '.', background=[('selected', _compcolor), ('active', _ana2color)])
        # master.configure(background=_bgcolor)
        # master.configure(highlightbackground="#f5deb3")
        # master.configure(highlightcolor="black")

        self.TButton1 = ttk.Button(master)
        self.TButton1.place(relx=0.37, rely=0.87, height=31, width=101)
        self.TButton1.configure(command=close)
        self.TButton1.configure(takefocus="")
        self.TButton1.configure(text='''Close''')
        self.TButton1.configure(command=self.Button_Cancel_Click)

        self.Scrolledtext1 = ScrolledText(master)
        self.Scrolledtext1.place(
            relx=0.02, rely=0.02, relheight=0.85, relwidth=0.96)
        self.Scrolledtext1.configure(background="white")
        # self.Scrolledtext1.configure(font=font10)
        self.Scrolledtext1.configure(highlightbackground="#f5deb3")
        self.Scrolledtext1.configure(insertborderwidth="3")
        self.Scrolledtext1.configure(selectbackground="#ddc8a1")
        self.Scrolledtext1.configure(width=10)
        self.Scrolledtext1.configure(wrap="word")

        self.TSizegrip1 = ttk.Sizegrip(master)
        self.TSizegrip1.place(anchor=SE, relx=1.0, rely=1.0)

        load_TickboxSMC(self.Scrolledtext1)

    def Button_Cancel_Click(self):
        '''cancel button'''
        root.destroy()


# The following code is added to facilitate the Scrolled widgets.
class AutoScroll(object):

    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        '''init'''
        vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        self.configure(yscrollcommand=self._autoscroll(vsb),
                       xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master

        methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                | Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            '''wrapped'''
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        '''___str___'''
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        '''wrapped'''
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped


class ScrolledText(AutoScroll, Text):

    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

if __name__ == '__main__':
    vp_start_gui()
