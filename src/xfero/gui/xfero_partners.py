#!/usr/bin/env python
'''

**Purpose:**

This script is the GUI Screen for managing File transfer Partners.

**Unit Test Module:** None

*External dependencies*

    /xfero/
      db
        manage_partner (/xfero/.gui.xfero_partners)

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
from /xfero/.db import manage_partner as db_partner

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global win, root
    root = Tk()
    root.title('XFERO_Partners')
    root.geometry('800x610+128+119')
    # root.geometry('607x518+128+119')
    win = XFERO_Partners(root)
    init()
    root.mainloop()

win = None

def create_XFERO_Partners(root):
    '''Starting point when module is imported by another program.'''
    global win, w_win
    if win:  # So we have only one instance of window.
        return
    win = Toplevel(root)
    win.title('XFERO_Partners')
    win.geometry('800x610+128+119')
    w_win = XFERO_Partners(win)
    init()
    return w_win

def destroy_XFERO_Partners():
    ''' Destroy dialogue '''
    global win
    win.destroy()
    win = None

def init():
    ''' init '''
    pass

class XFERO_Partners:
    ''' Partnets class '''
    def __init__(self, master=None):
        ''' init '''
        _compcolor = '#ffffff'  # X11 color: #ffffff
        _ana2color = '#ffffff'  # X11 color: #ffffff
        self.style = ttk.Style()
        self.data = ''
        self.identifier = ''
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
            relx=0.05, rely=0.03, relheight=0.39, relwidth=0.91)
        self.TLabelframe1.configure(text='''Partner Sites''')
        self.TLabelframe1.configure(width=540)

        frame = ttk.Frame(self.TLabelframe1)
        frame.pack(side=TOP, fill=BOTH, expand=Y)

        # create the tree and scrollbars
        self.dataCols = ('Identifier', 'Service Name', 'Description',
                         'COTS Type', 'Remote System ID', 'Code', 'Mode',
                         'Local Username', 'Local Password', 'Remote Username',
                         'Remote Password', 'CA Certificate', 'Cert Bundle',
                         'Control Port', 'IDF', 'Parm', 'PGP Public Key',
                         'LQM', 'DQM', 'OQM', 'CQ', 'Exit', 'Exit DLL',
                         'Exit Entry', 'Exit Data', 'OFile', 'Receiving App',
                         'Target App', 'Action', 'Post Xfer Hook',
                         'Post Xfer Comp Hook', 'Retain File', 'Priority')

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
        self.Label1.place(relx=0.05, rely=0.45, height=22, width=123)
        self.Label1.configure(activebackground="#ffffff")
        self.Label1.configure(activeforeground="black")
        # self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#bfbfbf")
        # self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#ffffff")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Service Name:''')

        self.Label3 = Label(master)
        self.Label3.place(relx=0.05, rely=0.50, height=22, width=123)
        self.Label3.configure(activebackground="#ffffff")
        self.Label3.configure(activeforeground="black")
        # self.Label3.configure(background=_bgcolor)
        self.Label3.configure(disabledforeground="#bfbfbf")
        # self.Label3.configure(font=font10)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#ffffff")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Description:''')
        self.Label3.configure(width=89)

        self.Label2 = Label(master)
        self.Label2.place(relx=0.05, rely=0.55, height=22, width=123)
        # self.Label2.configure(background=_bgcolor)
        self.Label2.configure(disabledforeground="#bfbfbf")
        # self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''COTS Product:''')

        self.Label4 = Label(master)
        self.Label4.place(relx=0.38, rely=0.55, height=22, width=123)
        # self.Label4.configure(background=_bgcolor)
        self.Label4.configure(disabledforeground="#bfbfbf")
        # self.Label4.configure(font=font10)
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''System ID:''')

        self.Label5 = Label(master)
        self.Label5.place(relx=0.68, rely=0.55, height=22, width=123)
        # self.Label5.configure(background=_bgcolor)
        self.Label5.configure(disabledforeground="#bfbfbf")
        # self.Label5.configure(font=font10)
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(text='''Code:''')

        self.Label6 = Label(master)
        self.Label6.place(relx=0.5, rely=0.60, height=22, width=123)
        # self.Label6.configure(background=_bgcolor)
        self.Label6.configure(disabledforeground="#bfbfbf")
        # self.Label6.configure(font=font10)
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(text='''Mode:''')

        self.Label7 = Label(master)
        self.Label7.place(relx=0.05, rely=0.65, height=22, width=123)
        # self.Label7.configure(background=_bgcolor)
        self.Label7.configure(disabledforeground="#bfbfbf")
        # self.Label7.configure(font=font10)
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(text='''XFERO Username:''')

        self.Label8 = Label(master)
        self.Label8.place(relx=0.5, rely=0.65, height=22, width=123)
        # self.Label8.configure(background=_bgcolor)
        self.Label8.configure(disabledforeground="#bfbfbf")
        # self.Label8.configure(font=font10)
        self.Label8.configure(foreground="#000000")
        self.Label8.configure(text='''XFERO Password:''')

        self.Label9 = Label(master)
        self.Label9.place(relx=0.05, rely=0.70, height=22, width=123)
        # self.Label9.configure(background=_bgcolor)
        self.Label9.configure(disabledforeground="#bfbfbf")
        # self.Label9.configure(font=font10)
        self.Label9.configure(foreground="#000000")
        self.Label9.configure(text='''Partner Username:''')

        self.Label10 = Label(master)
        self.Label10.place(relx=0.5, rely=0.70, height=22, width=123)
        # self.Label10.configure(background=_bgcolor)
        self.Label10.configure(disabledforeground="#bfbfbf")
        # self.Label10.configure(font=font10)
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(text='''Partner Password:''')

        self.Label11 = Label(master)
        self.Label11.place(relx=0.05, rely=0.75, height=22, width=123)
        # self.Label11.configure(background=_bgcolor)
        self.Label11.configure(disabledforeground="#bfbfbf")
        # self.Label11.configure(font=font10)
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(text='''CA Certificate:''')

        self.Label12 = Label(master)
        self.Label12.place(relx=0.5, rely=0.75, height=22, width=123)
        # self.Label12.configure(background=_bgcolor)
        self.Label12.configure(disabledforeground="#bfbfbf")
        # self.Label12.configure(font=font10)
        self.Label12.configure(foreground="#000000")
        self.Label12.configure(text='''Certificate Bundle:''')

        self.Label13 = Label(master)
        self.Label13.place(relx=0.05, rely=0.80, height=22, width=123)
        # self.Label13.configure(background=_bgcolor)
        self.Label13.configure(disabledforeground="#bfbfbf")
        # self.Label13.configure(font=font10)
        self.Label13.configure(foreground="#000000")
        self.Label13.configure(text='''Control Port:''')

        self.Label14 = Label(master)
        self.Label14.place(relx=0.5, rely=0.80, height=22, width=123)
        # self.Label14.configure(background=_bgcolor)
        self.Label14.configure(disabledforeground="#bfbfbf")
        # self.Label14.configure(font=font10)
        self.Label14.configure(foreground="#000000")
        self.Label14.configure(text='''IDF:''')

        self.Label15 = Label(master)
        self.Label15.place(relx=0.05, rely=0.85, height=22, width=123)
        # self.Label15.configure(background=_bgcolor)
        self.Label15.configure(disabledforeground="#bfbfbf")
        # self.Label15.configure(font=font10)
        self.Label15.configure(foreground="#000000")
        self.Label15.configure(text='''Parm:''')

        self.Label16 = Label(master)
        self.Label16.place(relx=0.5, rely=0.85, height=22, width=123)
        # self.Label16.configure(background=_bgcolor)
        self.Label16.configure(disabledforeground="#bfbfbf")
        # self.Label16.configure(font=font10)
        self.Label16.configure(foreground="#000000")
        self.Label16.configure(text='''PGP Pub Key:''')

        self.Entry_Service_Name = Entry(master)
        self.Entry_Service_Name.place(
            relx=0.25, rely=0.44, relheight=0.05, relwidth=0.71)
        self.Entry_Service_Name.configure(background="white")
        self.Entry_Service_Name.configure(disabledforeground="#bfbfbf")
        # self.Entry_Service_Name.configure(font=font11)
        self.Entry_Service_Name.configure(foreground="#000000")
        self.Entry_Service_Name.configure(highlightcolor="black")
        self.Entry_Service_Name.configure(insertbackground="black")
        self.Entry_Service_Name.configure(selectbackground="#e6e6e6")
        self.Entry_Service_Name.configure(selectforeground="black")
        self.Entry_Service_Name.configure(width=392)

        self.Entry_Description = Entry(master)
        self.Entry_Description.place(
            relx=0.25, rely=0.49, relheight=0.05, relwidth=0.71)
        self.Entry_Description.configure(background="white")
        self.Entry_Description.configure(disabledforeground="#bfbfbf")
        # self.Entry_Description.configure(font=font11)
        self.Entry_Description.configure(foreground="#000000")
        self.Entry_Description.configure(highlightcolor="black")
        self.Entry_Description.configure(insertbackground="black")
        self.Entry_Description.configure(selectbackground="#e6e6e6")
        self.Entry_Description.configure(selectforeground="black")
        self.Entry_Description.configure(width=392)

        self.Entry_COTS_Product = Entry(master)
        self.Entry_COTS_Product.place(
            relx=0.25, rely=0.54, relheight=0.05, relwidth=0.15)
        self.Entry_COTS_Product.configure(background="white")
        self.Entry_COTS_Product.configure(disabledforeground="#bfbfbf")
        # self.Entry_COTS_Product.configure(font=font11)
        self.Entry_COTS_Product.configure(foreground="#000000")
        self.Entry_COTS_Product.configure(insertbackground="black")
        #self.Entry_COTS_Product.configure(width=100)

        self.Entry_System_ID = Entry(master)
        self.Entry_System_ID.place(
            relx=0.53, rely=0.54, relheight=0.05, relwidth=0.15)
        self.Entry_System_ID.configure(background="white")
        self.Entry_System_ID.configure(disabledforeground="#bfbfbf")
        # self.Entry_System_ID.configure(font=font11)
        self.Entry_System_ID.configure(foreground="#000000")
        self.Entry_System_ID.configure(insertbackground="black")
        #self.Entry_System_ID.configure(width=100)

        self.Entry_Code = Entry(master)
        self.Entry_Code.place(
            relx=0.81, rely=0.54, relheight=0.05, relwidth=0.15)
        self.Entry_Code.configure(background="white")
        self.Entry_Code.configure(disabledforeground="#bfbfbf")
        # self.Entry_Code.configure(font=font11)
        self.Entry_Code.configure(foreground="#000000")
        self.Entry_Code.configure(insertbackground="black")

        self.Entry_Mode = Entry(master)
        self.Entry_Mode.place(
            relx=0.71, rely=0.59, relheight=0.05, relwidth=0.25)
        self.Entry_Mode.configure(background="white")
        self.Entry_Mode.configure(disabledforeground="#bfbfbf")
        # self.Entry_Mode.configure(font=font11)
        self.Entry_Mode.configure(foreground="#000000")
        self.Entry_Mode.configure(insertbackground="black")
        self.Entry_Mode.configure(width=142)

        self.Entry_XFERO_Username = Entry(master)
        self.Entry_XFERO_Username.place(
            relx=0.25, rely=0.64, relheight=0.05, relwidth=0.25)
        self.Entry_XFERO_Username.configure(background="white")
        self.Entry_XFERO_Username.configure(disabledforeground="#bfbfbf")
        # self.Entry_XFERO_Username.configure(font=font11)
        self.Entry_XFERO_Username.configure(foreground="#000000")
        self.Entry_XFERO_Username.configure(insertbackground="black")
        self.Entry_XFERO_Username.configure(width=122)

        self.Entry_XFERO_Password = Entry(master)
        self.Entry_XFERO_Password.place(
            relx=0.71, rely=0.64, relheight=0.05, relwidth=0.25)
        self.Entry_XFERO_Password.configure(background="white")
        self.Entry_XFERO_Password.configure(disabledforeground="#bfbfbf")
        # self.Entry_XFERO_Password.configure(font=font11)
        self.Entry_XFERO_Password.configure(foreground="#000000")
        self.Entry_XFERO_Password.configure(insertbackground="black")
        self.Entry_XFERO_Password.configure(width=142)

        self.Entry_Partner_Username = Entry(master)
        self.Entry_Partner_Username.place(
            relx=0.25, rely=0.69, relheight=0.05, relwidth=0.25)
        self.Entry_Partner_Username.configure(background="white")
        self.Entry_Partner_Username.configure(disabledforeground="#bfbfbf")
        # self.Entry_Partner_Username.configure(font=font11)
        self.Entry_Partner_Username.configure(foreground="#000000")
        self.Entry_Partner_Username.configure(insertbackground="black")
        self.Entry_Partner_Username.configure(width=132)

        self.Entry_Partner_Password = Entry(master)
        self.Entry_Partner_Password.place(
            relx=0.71, rely=0.69, relheight=0.05, relwidth=0.25)
        self.Entry_Partner_Password.configure(background="white")
        self.Entry_Partner_Password.configure(disabledforeground="#bfbfbf")
        # self.Entry_Partner_Password.configure(font=font11)
        self.Entry_Partner_Password.configure(foreground="#000000")
        self.Entry_Partner_Password.configure(insertbackground="black")
        self.Entry_Partner_Password.configure(width=122)

        self.Entry_CA_Cert = Entry(master)
        self.Entry_CA_Cert.place(
            relx=0.25, rely=0.74, relheight=0.05, relwidth=0.25)
        self.Entry_CA_Cert.configure(background="white")
        self.Entry_CA_Cert.configure(disabledforeground="#bfbfbf")
        # self.Entry_CA_Cert.configure(font=font11)
        self.Entry_CA_Cert.configure(foreground="#000000")
        self.Entry_CA_Cert.configure(insertbackground="black")
        self.Entry_CA_Cert.configure(width=120)

        self.Entry_Cert_Bundle = Entry(master)
        self.Entry_Cert_Bundle.place(
            relx=0.71, rely=0.74, relheight=0.05, relwidth=0.25)
        self.Entry_Cert_Bundle.configure(background="white")
        self.Entry_Cert_Bundle.configure(disabledforeground="#bfbfbf")
        # self.Entry_Cert_Bundle.configure(font=font11)
        self.Entry_Cert_Bundle.configure(foreground="#000000")
        self.Entry_Cert_Bundle.configure(insertbackground="black")

        self.Entry_Control_Port = Entry(master)
        self.Entry_Control_Port.place(
            relx=0.25, rely=0.79, relheight=0.05, relwidth=0.25)
        self.Entry_Control_Port.configure(background="white")
        self.Entry_Control_Port.configure(disabledforeground="#bfbfbf")
        # self.Entry_Control_Port.configure(font=font11)
        self.Entry_Control_Port.configure(foreground="#000000")
        self.Entry_Control_Port.configure(insertbackground="black")
        self.Entry_Control_Port.configure(width=132)

        self.Entry_IDF = Entry(master)
        self.Entry_IDF.place(
            relx=0.71, rely=0.79, relheight=0.05, relwidth=0.25)
        self.Entry_IDF.configure(background="white")
        self.Entry_IDF.configure(disabledforeground="#bfbfbf")
        # self.Entry_IDF.configure(font=font11)
        self.Entry_IDF.configure(foreground="#000000")
        self.Entry_IDF.configure(insertbackground="black")

        self.Entry_Parm = Entry(master)
        self.Entry_Parm.place(
            relx=0.25, rely=0.84, relheight=0.05, relwidth=0.25)
        self.Entry_Parm.configure(background="white")
        self.Entry_Parm.configure(disabledforeground="#bfbfbf")
        # self.Entry_Parm.configure(font=font11)
        self.Entry_Parm.configure(foreground="#000000")
        self.Entry_Parm.configure(insertbackground="black")
        self.Entry_Parm.configure(width=122)

        self.Entry_Key = Entry(master)
        self.Entry_Key.place(
            relx=0.71, rely=0.84, relheight=0.05, relwidth=0.25)
        self.Entry_Key.configure(background="white")
        self.Entry_Key.configure(disabledforeground="#bfbfbf")
        # self.Entry_Key.configure(font=font11)
        self.Entry_Key.configure(foreground="#000000")
        self.Entry_Key.configure(insertbackground="black")

        self.Button_Update = Button(master)
        self.Button_Update.place(relx=0.71, rely=0.91, height=28, width=73)
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
        self.Button_Delete.place(relx=0.6, rely=0.91, height=28, width=68)
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

        self.Button_Add = Button(master)
        self.Button_Add.place(relx=0.83, rely=0.91, height=28, width=54)
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
        self.Button_Cancel.place(relx=0.48, rely=0.91, height=28, width=70)
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

    def Button_Add_Click(self):
        ''' Button Add '''
        partner_service_name = self.Entry_Service_Name.get()
        partner_description = self.Entry_Description.get()
        partner_system_id = self.Entry_System_ID.get()
        partner_cots_product = self.Entry_COTS_Product.get()
        partner_code = self.Entry_Code.get()
        partner_xfero_user = self.Entry_XFERO_Username.get()
        partner_remote_user = self.Entry_Partner_Username.get()
        partner_ca_cert = self.Entry_CA_Cert.get()
        partner_control_port = self.Entry_Control_Port.get()
        partner_parm = self.Entry_Parm.get()
        partner_mode = self.Entry_Mode.get()
        partner_xfero_password = self.Entry_XFERO_Password.get()
        partner_remote_password = self.Entry_Partner_Password.get()
        partner_cert_bundle = self.Entry_Cert_Bundle.get()
        partner_idf = self.Entry_IDF.get()
        partner_pub_key = self.Entry_Key.get()

        #partner_lqm, partner_dqm, partner_oqm, partner_cq, partner_exit, partner_exitdll, partner_exitentry, partner_exitdata, partner_ofile, partner_receiving_app,partner_target_app, partner_action,partner_post_xfer_hook, partner_post_xfer_comp_hook,partner_retain_file, partner_priority
        result = db_partner.create_XFERO_Partner(partner_service_name,
                                              partner_description,
                                              partner_cots_product,
                                              partner_system_id,
                                              partner_code, partner_mode,
                                              partner_xfero_user,
                                              partner_xfero_password,
                                              partner_remote_user,
                                              partner_remote_password,
                                              partner_ca_cert,
                                              partner_cert_bundle,
                                              partner_control_port,
                                              partner_idf, partner_parm,
                                              partner_pub_key, '', '', '' ,'', 
                                              '', '', '' ,'', '', '', '' ,'', 
                                              '', '', '' ,'' )

        self.reload_tree()

    def Button_Cancel_Click(self):
        ''' Button Cancel '''
        root.destroy()

    def Button_Delete_Click(self):
        ''' Button Delete '''
        result = db_partner.delete_XFERO_Partner(self.identifier)

        self.reload_tree()

    def Button_Update_Click(self):
        ''' Button Update '''
        partner_service_name = self.Entry_Service_Name.get()
        partner_description = self.Entry_Description.get()
        partner_system_id = self.Entry_System_ID.get()
        partner_cots_product = self.Entry_COTS_Product.get()
        partner_code = self.Entry_Code.get()
        partner_xfero_user = self.Entry_XFERO_Username.get()
        partner_remote_user = self.Entry_Partner_Username.get()
        partner_ca_cert = self.Entry_CA_Cert.get()
        partner_control_port = self.Entry_Control_Port.get()
        partner_parm = self.Entry_Parm.get()
        partner_mode = self.Entry_Mode.get()
        partner_xfero_password = self.Entry_XFERO_Password.get()
        partner_remote_password = self.Entry_Partner_Password.get()
        partner_cert_bundle = self.Entry_Cert_Bundle.get()
        partner_idf = self.Entry_IDF.get()
        partner_pub_key = self.Entry_Key.get()

        result = db_partner.update_XFERO_Partner(self.identifier,
                                              partner_service_name,
                                              partner_description,
                                              partner_cots_product,
                                              partner_system_id, partner_code,
                                              partner_mode, partner_xfero_user,
                                              partner_xfero_password,
                                              partner_remote_user,
                                              partner_remote_password,
                                              partner_ca_cert,
                                              partner_cert_bundle,
                                              partner_control_port, partner_idf,
                                              partner_parm, partner_pub_key, '', 
                                              '', '' ,'', '', '', '' ,'', '', 
                                              '', '' ,'', '', '', '' ,'' )

        self.reload_tree()

    def reload_tree(self):
        ''' reload tree '''
        tree_list = self.tree.get_children()
        for tree in tree_list:
            self.tree.delete(tree)

        # reload treview with new row
        self._load_data()

        # Clear entry fields
        self.Entry_Service_Name.delete(0, END)
        self.Entry_Description.delete(0, END)
        self.Entry_System_ID.delete(0, END)
        self.Entry_COTS_Product.delete(0, END)
        self.Entry_Code.delete(0, END)
        self.Entry_XFERO_Username.delete(0, END)
        self.Entry_Partner_Username.delete(0, END)
        self.Entry_CA_Cert.delete(0, END)
        self.Entry_Mode.delete(0, END)
        self.Entry_XFERO_Password.delete(0, END)
        self.Entry_Partner_Password.delete(0, END)
        self.Entry_Cert_Bundle.delete(0, END)
        self.Entry_Control_Port.delete(0, END)
        self.Entry_Parm.delete(0, END)
        self.Entry_IDF.delete(0, END)
        self.Entry_Key.delete(0, END)

        self.Button_Delete.configure(state="disabled")
        self.Button_Update.configure(state="disabled")

    def Tree_Select(self, p1_tree):
        ''' tree select '''
        self.Entry_Service_Name.delete(0, END)
        self.Entry_Description.delete(0, END)
        self.Entry_System_ID.delete(0, END)
        self.Entry_COTS_Product.delete(0, END)
        self.Entry_Code.delete(0, END)
        self.Entry_XFERO_Username.delete(0, END)
        self.Entry_Partner_Username.delete(0, END)
        self.Entry_CA_Cert.delete(0, END)
        self.Entry_Mode.delete(0, END)
        self.Entry_XFERO_Password.delete(0, END)
        self.Entry_Partner_Password.delete(0, END)
        self.Entry_Cert_Bundle.delete(0, END)
        self.Entry_Control_Port.delete(0, END)
        self.Entry_Parm.delete(0, END)
        self.Entry_IDF.delete(0, END)
        self.Entry_Key.delete(0, END)

        self.Button_Update.configure(state="normal")
        self.Button_Delete.configure(state="normal")

        item = self.tree.identify('item', p1_tree.x, p1_tree.y)

        values = self.tree.item(item, 'values')
        if values:
            self.identifier = values[0]
            self.Entry_Service_Name.insert(0, values[1])
            self.Entry_Description.insert(0, values[2])
            self.Entry_COTS_Product.insert(0, values[3])
            self.Entry_System_ID.insert(0, values[4])
            self.Entry_Code.insert(0, values[5])
            self.Entry_Mode.insert(0, values[6])
            self.Entry_XFERO_Username.insert(0, values[7])
            self.Entry_XFERO_Password.insert(0, values[8])
            self.Entry_Partner_Username.insert(0, values[9])
            self.Entry_Partner_Password.insert(0, values[10])
            self.Entry_CA_Cert.insert(0, values[11])
            self.Entry_Cert_Bundle.insert(0, values[12])
            self.Entry_Control_Port.insert(0, values[13])
            self.Entry_IDF.insert(0, values[14])
            self.Entry_Parm.insert(0, values[15])
            self.Entry_Key.insert(0, values[16])

        sys.stdout.flush()

    def _load_data(self):
        '''load data'''
        self.data = db_partner.list_XFERO_Partner()

        # configure column headings
        for col in self.dataCols:
            self.tree.heading(
                col, text=col.title(),
                command=lambda col=col:
                self._column_sort(col, XFERO_Partners.SortDir))
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
        '''column sort'''
        data = [(self.tree.set(child, col), child)
                for child in self.tree.get_children('')]

        # reorder data
        # tkinter looks after moving other items in
        # the same row
        data.sort(reverse=descending)

        for indx, item in enumerate(data):
            self.tree.move(item[1], '', indx)   # item[1] = item Identifier

        # reverse sort direction for next sort operation

        XFERO_Partners.SortDir = not descending

if __name__ == '__main__':

    vp_start_gui()
