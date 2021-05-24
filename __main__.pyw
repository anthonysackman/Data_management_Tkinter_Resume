import sqlite3
import tkinter
import tkinter as Tk
import tkinter.ttk as ttk
from datetime import *
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox

import pandas as pd
# Import custom libraries
from SQL import sql_class
from create_html_report import *
from csv_import_export_tool import *


class main:
    def mainWindow(self):
        master = tkinter.Tk()
        master.geometry(main.center(self, master))
        master.title('Washington DHIA Lab Report')

        # Create SQL DB if none exists
        sqlClass = sql_class()
        sqlClass.sqlCreate()

        # Setup top menu bar, pack to master
        menuBar = Menu(master)
        fileMenu = Menu(menuBar, tearoff=0)

        fileMenu.add_command(label="New Report", command=lambda: report.newLabReport(self, "new", None, None))
        fileMenu.add_command(label="Exit", command=lambda: master.destroy())

        optionMenu = Menu(menuBar, tearoff=0)
        optionMenu.add_command(label="Import/Export", command=lambda: csvGui.importExport(self))

        menuBar.add_cascade(label="File", menu=fileMenu)
        menuBar.add_cascade(label="Options", menu=optionMenu)

        master.config(menu=menuBar)

        # Configure main screen frame with buttons
        mainframe = tkinter.Frame(master)
        mainframe.grid()

        mainframe.columnconfigure(0, minsize=200)

        new_report = tkinter.Button(mainframe, text="New Report", command=lambda: report.newLabReport(self, "new", None, None))
        new_report.grid(row=0, column=0, sticky=EW, padx=10, pady=2)

        search_report = tkinter.Button(mainframe, text="Print Lab Report", command=lambda: report.printLabReport(self))
        search_report.grid(row=1, column=0, sticky=EW, padx=10, pady=2)

        add_herd = tkinter.Button(mainframe, width=20, text="Add/View Herds", command=lambda: treeview.treeAddFindMenu(self, "herd"))
        add_herd.grid(row=2, column=0, sticky=EW, padx=10, pady=2)

        add_ft = tkinter.Button(mainframe, width=20, text="Add/View Field Technician", command=lambda: treeview.treeAddFindMenu(self, "ft"))
        add_ft.grid(row=3, column=0, sticky=EW, padx=10, pady=2)

        add_lt = tkinter.Button(mainframe, width=20, text="Add/View Lab Technician", command=lambda: treeview.treeAddFindMenu(self, "lt"))
        add_lt.grid(row=4, column=0, sticky=EW, padx=10, pady=2)

        # csv_tool = tkinter.Button(mainframe, text="Import/Export", command=lambda: csvGui.importExport(self))
        # csv_tool.grid(row=0, column=4, sticky=N)

        labreports = tkinter.Button(mainframe, text="Lab Reports", command=lambda: lab_report_table.labReportTable(self)).grid(row=5, column=0,
                                                                                                                               sticky=EW, padx=10, pady=2)

        master.mainloop()

    # Function to calculate center of screen position based on screen size
    def center(self, root):
        wWidth = root.winfo_reqwidth()
        wHeight = root.winfo_reqheight()

        posRight = int(root.winfo_screenwidth() / 2 - wWidth / 2)
        posDown = int(root.winfo_screenheight() / 2 - wHeight / 2)

        root.geometry("+{}+{}".format(posRight, posDown))


# Class for common button actions
class btnAction():
    # Delete current frame
    def destroy(self):
        self.destroy()

    # Cancel popup dialog
    def cancel(self):
        master_c = tkinter.Toplevel()
        master_c.title("Exit?")
        master_c.geometry(main.center(self, master_c))
        cFrame = tkinter.Frame(master_c)
        cFrame.pack()
        cLabel = tkinter.Label(master=cFrame, text="Are you sure you want to exit without saving?")
        cLabel.pack(fill=tkinter.BOTH)
        yButton = tkinter.Button(master_c, text="Yes", command=lambda: [btnAction.destroy(self), btnAction.destroy(master_c)])
        yButton.pack()
        cButton = tkinter.Button(master_c, text="Cancel", command=lambda: btnAction.destroy(master_c))
        cButton.pack()


# Print various reports
class report():
    # Print Report Screen
    def printLabReport(self):
        master_pl = tkinter.Toplevel()
        master_pl.title("Print Report")
        master_pl.geometry(main.center(self, master_pl))
        master_pl.resizable(width=False, height=False)

        # Get today's date and the day before for automatic filling
        today = date.today()
        d1 = today.strftime("%m/%d/%Y")
        yesterday = (today - timedelta(days=1)).strftime("%m/%d/%Y")

        # Set main print screen frame and add labels, entry fields, and buttons
        plFrame = tkinter.Frame(master_pl)
        plFrame.grid()
        tLabel = tkinter.Label(plFrame, text="Search by Lab Test Date")
        tLabel.grid(row=0, column=0, sticky=N, columnspan=6)

        pdlLabel = tkinter.Label(plFrame, text="Date:", width=6)
        pdlLabel.grid(row=1, column=0, sticky=W, padx=1, pady=1)

        entry_text = StringVar()

        pdlEntry = tkinter.Entry(plFrame, width=10, textvariable=entry_text)
        pdlEntry.grid(row=1, column=1, sticky=W)

        tdybtn = tkinter.Button(plFrame, text="Ystdy", command=lambda: pdlEntry.insert("0", yesterday)).grid(row=1, column=3, sticky=W)
        tdybtn = tkinter.Button(plFrame, text="Tdy", command=lambda: pdlEntry.insert("0", d1)).grid(row=1, column=3, sticky=E)

        dReportBtn = tkinter.Button(plFrame, text="Print Report", command=lambda: sql.rSearch(pdlEntry.get(), None, master_pl))
        dReportBtn.grid(row=1, column=4, sticky=E)

        drange1 = StringVar()
        drange2 = StringVar()

        year = StringVar()

        drange_lbl = tkinter.Label(plFrame, text="Search By Date Range").grid(row=2, column=0, columnspan=6)
        drange_lbl_1 = tkinter.Label(plFrame, text="From:", width=6).grid(row=3, column=0, padx=1, pady=1, sticky=W)

        drange_ent_1 = tkinter.Entry(plFrame, width=10, textvariable=drange1)
        drange_ent_1.grid(row=3, column=1)

        drange_lbl_2 = tkinter.Label(plFrame, text="To:", width=3).grid(row=3, column=2, padx=1, pady=1, sticky=W)
        drange_ent_2 = tkinter.Entry(plFrame, width=10, textvariable=drange2)
        drange_ent_2.grid(row=3, column=3)

        drReportBtn = tkinter.Button(plFrame, text="Print Report", command=lambda: dateRangePrint())
        drReportBtn.grid(row=3, column=4, sticky=E)

        month_lbl = tkinter.Label(plFrame, text="Print Month Report").grid(row=4, column=0, columnspan=6)
        month_lbl_text = tkinter.Label(plFrame, text="Select Month:").grid(row=5, column=0)

        year_lbl = tkinter.Label(plFrame, text="Year:").grid(row=5, column=3, sticky=tkinter.W)
        year_ent = tkinter.Entry(plFrame, width=5, textvariable=year).grid(row=5, column=3, sticky=tkinter.E)

        # Build combobox for months
        data = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
        cb = Combobox(plFrame, values=data)
        cb.grid(row=5, column=1, columnspan=1)
        cb.state(['readonly'])
        # setting combobox default
        cb.set("January")

        # Get data for lab report
        month_print = create_html_report()
        outputData = sql_class.sqlData("lab_report")

        month_btn = tkinter.Button(plFrame, text="Print Report", command=lambda: monthPrint())
        month_btn.grid(row=5, column=4)

        def monthPrint():
            # validate year
            if len(str(year.get())) != 4:
                master = tkinter.Toplevel()
                master.title("Error")
                master.geometry(main.center(self, master))
                ErrorLabel = tkinter.Label(master, text="Error: Year has to be 4 digits. Ex. 2020.", fg="red").grid(row=0, column=0)
                return None
            # validate digits
            elif not year.get().isdigit():
                master = tkinter.Toplevel()
                master.title("Error")
                master.geometry(main.center(self, master))
                ErrorLabel = tkinter.Label(master, text="Error: Year must be digits. Ex. 2020.", fg="red").grid(row=0, column=0)
                return None
            else:
                saveDir = fileExplore.choose_folder(master_pl)
                month_print.print_month_report(cb.get(), year.get(), outputData, str(saveDir))

        # Get daterange and send to SQL libary to get data and push to Create html report
        def dateRangePrint():
            dates = pd.date_range(drange_ent_1.get(), drange_ent_2.get())
            fdatelist = dates.format(formatter=lambda x: x.strftime('%m/%d/%Y'))
            sql.rSearch(None, fdatelist, master_pl)

        # Auto Date Format as printing
        def handle_keypress_datebox(event):
            if pdlEntry.get():
                eventS = pdlEntry.get()
                try:
                    if eventS[2] != "/":
                        pdlEntry.insert("2", "/")
                except:
                    return None
                try:
                    if eventS[5] != "/":
                        pdlEntry.insert("5", "/")
                except:
                    return None

            if drange_ent_1.get():
                event1 = drange_ent_1.get()
                try:
                    if event1[2] != "/" and event1[2] != "":
                        drange_ent_1.insert("2", "/")
                except:
                    return None
                try:
                    if event1[5] != "/" and event1[2] != "":
                        drange_ent_1.insert("5", "/")
                except:
                    return None

            if drange_ent_2.get():
                event2 = drange_ent_2.get()
                try:
                    if event2[2] != "/" and event2[2] != "":
                        drange_ent_2.insert("2", "/")
                except:
                    return None
                try:
                    if event2[5] != "/" and event2[2] != "":
                        drange_ent_2.insert("5", "/")
                except:
                    return None

        # Set character limit
        def character_limit(entry_text):
            if len(entry_text.get()) > 0:
                entry_text.set(entry_text.get()[:10])

        entry_text.trace("w", lambda *args: character_limit(entry_text))
        drange1.trace("w", lambda *args: character_limit(drange1))
        drange2.trace("w", lambda *args: character_limit(drange2))

        # Bind enter key to select
        def handleReturn(event):
            sql.rSearch(pdlEntry.get(), None, master_pl)

        pdlEntry.bind("<Return>", handleReturn)

        pdlEntry.focus()

        # Bind keypress to date auto format
        pdlEntry.bind("<KeyPress>", handle_keypress_datebox)
        drange_ent_1.bind("<KeyPress>", handle_keypress_datebox)
        drange_ent_2.bind("<KeyPress>", handle_keypress_datebox)

    # Create new lab report (main report)
    def newLabReport(self, type, editImport, id):
        sql_class.delTemp()
        var_list = ["output1", "output2", "output3", "output4", "output5", "output6", "output7", "output8",
                    "output9",
                    "output10", "output11"]

        # Validate data and submit report
        def submitReport():
            sqlClass = sql_class()
            global output1, empty
            global output2
            global output3
            global output4
            global output5
            global output6
            global output7
            global output8
            global output9
            global output10
            global output11

            output1 = entry1.get()
            output2 = entry2.get()
            output3 = entry3.get()
            output4 = entry4.get()
            output5 = entry5.get()
            output6 = entry6.get()
            output7 = entry7.get()
            output8 = entry8.get()
            output9 = entry9.get()
            output10 = entry10.get()
            output11 = entry11.get()

            global empty
            empty = False

            # Validate all fields are filled
            for i in var_list:
                if not eval(i):
                    empty = True

            # Error message
            if empty == True:
                master = tkinter.Toplevel()
                master.title("Error")
                # master.geometry("1200x600")
                master.geometry(main.center(self, master))
                ErrorLabel = tkinter.Label(master, text="Error: Cannot leave any field blank.", fg="red").grid(row=0,
                                                                                                               column=0)
                return None

            # Format output11 for fee to decimal type
            output11 = float(output11.replace('$', '').replace(',', ''))

            global export_list
            export_list = []

            for i in var_list:
                export_list.append(eval(i))

            # Check if we are updating a record or creating a new one, if new pop-up asking to enter another report
            if type == "new":
                # submit report to db
                sqlClass.submitLabReport(export_list)
                master = tkinter.Toplevel()
                master.title("New Report")
                master.geometry(main.center(self, master))
                label = tkinter.Label(master, text="Create another report?").grid(row=0, column=0)
                master.focus()

                # Delete entry fields for reset of new report
                def emptyReport():
                    entry1.delete(0, 'end')
                    entry2.delete(0, 'end')
                    entry3.delete(0, 'end')
                    entry4.delete(0, 'end')
                    entry5.delete(0, 'end')
                    # entry6.insert(0, d1) Keep current date
                    entry7.delete(0, 'end')
                    entry8.delete(0, 'end')
                    entry9.delete(0, 'end')
                    entry10.delete(0, 'end')
                    entry11.delete(0, 'end')

                # Set yes and no buttons, destroy if no, otherwise empty the report fields
                yBtn = tkinter.Button(master, text="[Y]es", command=lambda: [emptyReport(), btnAction.destroy(master)]).grid(row=1, column=1)
                nBtn = tkinter.Button(master, text="[N]o", command=lambda: [btnAction.destroy(master_r), btnAction.destroy(master)]).grid(row=1, column=2)

                def yesBtn(event):
                    emptyReport()
                    btnAction.destroy(master)
                    entry1.focus()

                def noBtn(event):
                    btnAction.destroy(master_r)
                    btnAction.destroy(master)

                master.bind('<Return>', yesBtn)
                master.bind('y', yesBtn)
                master.bind('n', noBtn)

            else:
                # If updating record, destroy window and subit db edit
                btnAction.destroy(master_r)
                lab_report_table.editItem(None, export_list, editImport, id)
                return export_list

        # Set title
        master_r = tkinter.Toplevel()
        if type == "new":
            master_r.title("New Report")
        else:
            master_r.title("Edit Report")

        master_r.geometry(main.center(self, master_r))
        # Set main frame
        mframe = tkinter.Frame(master_r)
        mframe.pack()

        # Set text variables
        entry_text1 = StringVar()
        entry_text2 = StringVar()
        entry_text3 = StringVar()
        entry_text4 = StringVar()
        fee_Var = StringVar()
        lt_Var = StringVar()
        ft_Var = StringVar()
        ft_Name_Var = StringVar()
        tp_Var = StringVar()
        pc_Var = StringVar()

        # Set entry fields and corrosponding labels
        entry1 = tkinter.Entry(master=mframe, width=50, textvariable=entry_text3)
        entry_label = tkinter.Label(master=mframe, text="Herd Code")
        entry2 = tkinter.Entry(master=mframe, width=50, textvariable=entry_text4)
        entry_labe2 = tkinter.Label(master=mframe, text="Herd Name")
        entry3 = tkinter.Entry(master=mframe, width=50, textvariable=entry_text1)
        entry_labe3 = tkinter.Label(master=mframe, text="Date Of Test")
        entry4 = tkinter.Entry(master=mframe, width=50, textvariable=ft_Var)
        entry_labe4 = tkinter.Label(master=mframe, text="Field Technician Number")
        entry5 = tkinter.Entry(master=mframe, width=50, textvariable=ft_Name_Var)
        entry_labe5 = tkinter.Label(master=mframe, text="Field Technician Name")
        entry6 = tkinter.Entry(master=mframe, width=50, textvariable=entry_text2)
        entry_labe6 = tkinter.Label(master=mframe, text="Lab Test Date")
        entry7 = tkinter.Entry(master=mframe, width=50)
        entry_labe7 = tkinter.Label(master=mframe, text="Number Of Samples")
        entry8 = tkinter.Entry(master=mframe, width=50, textvariable=lt_Var)
        entry_labe8 = tkinter.Label(master=mframe, text="Lab Tech Name")
        entry9 = tkinter.Entry(master=mframe, width=50, textvariable=tp_Var)
        entry_labe9 = tkinter.Label(master=mframe, text="Test Performed")
        entry10 = tkinter.Entry(master=mframe, width=50, textvariable=pc_Var)
        entry_labell0 = tkinter.Label(master=mframe, text="Processing Center")
        entry11 = tkinter.Entry(master=mframe, width=50, textvariable=fee_Var)
        entry_label11 = tkinter.Label(master=mframe, text="Processing Fee")

        # Set Entry and label fields to ui grid
        entry1.grid(row=0, column=1)
        entry_label.grid(row=0, column=0)
        entry2.grid(row=1, column=1)
        entry_labe2.grid(row=1, column=0)
        entry3.grid(row=2, column=1)
        entry_labe3.grid(row=2, column=0)
        entry4.grid(row=3, column=1)
        entry_labe4.grid(row=3, column=0)
        entry5.grid(row=4, column=1)
        entry_labe5.grid(row=4, column=0)
        entry6.grid(row=5, column=1)
        entry_labe6.grid(row=5, column=0)
        entry7.grid(row=6, column=1)
        entry_labe7.grid(row=6, column=0)
        entry8.grid(row=7, column=1)
        entry_labe8.grid(row=7, column=0)
        entry9.grid(row=8, column=1)
        entry_labe9.grid(row=8, column=0)
        entry10.grid(row=9, column=1)
        entry_labell0.grid(row=9, column=0)
        entry10.grid(row=10, column=1)
        entry_labell0.grid(row=10, column=0)
        entry11.grid(row=11, column=1)
        entry_label11.grid(row=11, column=0)

        # Fill report if editing record
        if type == "edit":
            entry1.insert(0, editImport[0])
            entry2.insert(0, editImport[1])
            entry3.insert(0, editImport[2])
            entry4.insert(0, editImport[3])
            entry5.insert(0, editImport[4])
            entry6.insert(0, editImport[5])
            entry7.insert(0, editImport[6])
            entry8.insert(0, editImport[7])
            entry9.insert(0, editImport[8])
            entry10.insert(0, editImport[9])
            entry11.insert(0, editImport[10])

        # Insert todays date
        if type == "new":
            today = date.today()
            d1 = today.strftime("%m/%d/%Y")
            entry6.insert(0, d1)

        # Date autoformatting verifying every keypress
        def handle_keypress_datebox1(event):
            eventS1 = entry3.get()
            try:
                if eventS1[2] != "/":
                    entry3.insert("2", "/")
            except:
                return None
            try:
                if eventS1[5] != "/":
                    entry3.insert("5", "/")
            except:
                return None

        def handle_keypress_datebox2(event):
            eventS2 = entry6.get()
            try:
                if eventS2[2] != "/":
                    entry6.insert("2", "/")
            except:
                return None
            try:
                if eventS2[5] != "/":
                    entry6.insert("5", "/")
            except:
                return None

        # Character limit checks every keypress
        def character_limit1(entry_text1):
            if len(entry_text1.get()) > 0:
                entry_text1.set(entry_text1.get()[:10])

        def character_limit2(entry_text2):
            if len(entry_text2.get()) > 0:
                entry_text2.set(entry_text2.get()[:10])

        # Autofill herdname based on herdcode as it is typed out
        def herdAuto():
            herdList = sql.tableOutputList("herd")
            sortedHerdList = sorted(herdList)
            herdCodeEntry = entry_text3.get()
            outputList = []
            fHerdCodeEntry = [int(s) for s in herdCodeEntry.split() if s.isdigit()]
            for i in sortedHerdList:
                if str(i[0]).startswith(herdCodeEntry) and herdCodeEntry != "":
                    outputList.append(i[1])

            try:
                result = outputList[0]

                entry2.delete(0, 'end')
                entry2.insert("0", str(result))
            except:
                entry2.delete(0, 'end')

        # Autofill herdcode based on herdname
        def herdCodeComplete(event):
            curHerd = entry2.get()
            herdCode = sql_class.search_sql("herd", "herd_name", curHerd)
            fHerdCode = [item[0] for item in herdCode]
            try:
                entry_text3.set(fHerdCode[0])
            except:
                return

        # Autoformat fee to USD
        def feeFormat(event):
            fee = fee_Var.get()
            if fee.replace('.', '').isdigit():
                output = "${:,.2f}".format(float(fee))
                fee_Var.set(output)

        # Key Bindings and focus bindings to trigger autofill and formatting functions
        entry11.bind("<FocusOut>", feeFormat)

        entry_text3.trace("w", lambda *args: herdAuto())
        entry1.bind("<FocusOut>", herdCodeComplete)

        # Handle temp db field being passed from SQL file, used to hand data from one module to another (not optimal)
        def handleReturn(event):
            try:
                returnVal = sql_class.getTemp()
                if returnVal != "":
                    if returnVal[0][0].startswith("lt"):
                        lt_Var.set(returnVal[0][0][2:])
                    elif returnVal[0][0].startswith("ft"):
                        ft_Var.set(returnVal[0][0][2:])
                    elif returnVal[0][0].startswith("tp"):
                        tp_Var.set(returnVal[0][0][2:])
                    elif returnVal[0][0].startswith("pc"):
                        pc_Var.set(str(returnVal[0][0][2:]))
                    else:
                        entry_text3.set(returnVal[0][0][4:])

                sql_class.delTemp()
            except:
                return None

        # Autofill lab technician based on entry each keypress
        def ltAuto():
            curInput = lt_Var.get()[:int(entry8.index(INSERT))]
            if curInput != "":
                sortedltList = sorted(sql_class.sqlSearchStartsWith("lab_tech", "Lab_tech_name", curInput))
                for i in sortedltList:
                    lt_Var.set(str(i[1]))
                if len(sortedltList) < 1:
                    lt_Var.set("")

        # Autofill field technician based on user entry every keypress
        def fTechAuto():
            ftEntry = ft_Var.get()
            if not ftEntry:
                ft_Name_Var.set("")
                return None
            ftList = sql_class.sqlData("field_tech")
            sortedftList = sorted(ftList)
            outList = []

            for i in sortedftList:
                if str(i[0]).startswith(str(ftEntry)):
                    outList.append(i[1])

            try:
                if outList[0]:
                    ft_Name_Var.set(outList[0])
            except:
                ft_Name_Var.set("")

        # Autofill field tech name based on number
        def fTechComplete(event):
            curft = ft_Name_Var.get()
            ft = sql_class.search_sql("field_tech", "name", curft)
            ftCode = [item[0] for item in ft]
            try:
                ft_Var.set(ftCode[0])
            except:
                return

        # Autofill Test type based on entry every keypress
        def testTypeAuto():
            curInput = tp_Var.get()[:int(entry9.index(INSERT))]
            if curInput != "":
                sortedList = sorted(sql_class.sqlSearchStartsWith("test_performed", "test_performed", curInput))
                print(sortedList)
                for i in sortedList:
                    tp_Var.set(str(i[0]))
                if len(sortedList) < 1:
                    tp_Var.set("")

        # Autofill process center based on entry every keypress
        def processCenterAuto():
            curInput = pc_Var.get()[:int(entry10.index(INSERT))]
            if curInput != "":
                sortedList = sorted(sql_class.sqlSearchStartsWith("processing_center", "processing_center", curInput))
                for i in sortedList:
                    pc_Var.set(str(i[0]))
                if len(sortedList) < 1:
                    pc_Var.set("")

        # Key and focus bindings
        def enter(event):
            submitReport()

        master_r.bind('<Return>', enter)
        entry4.bind("<FocusOut>", fTechComplete)
        master_r.bind("<FocusIn>", handleReturn)
        lt_Var.trace("w", lambda *args: ltAuto())
        ft_Var.trace("w", lambda *args: fTechAuto())
        tp_Var.trace("w", lambda *args: testTypeAuto())
        pc_Var.trace("w", lambda *args: processCenterAuto())
        entry_text1.trace("w", lambda *args: character_limit1(entry_text1))
        entry_text2.trace("w", lambda *args: character_limit2(entry_text2))
        entry3.bind("<Key>", handle_keypress_datebox1)
        entry6.bind("<Key>", handle_keypress_datebox2)

        # Set focus on first field
        entry1.focus()

        # Create button field
        bframe = tkinter.Frame(master_r)
        bframe.pack()

        # Handle when add button is used top open popup treeview
        def handleTempReturn(self, table):
            if table == "ft":
                treeview.treeAddFindMenu(self, table)
            elif table == "lt":
                treeview.treeAddFindMenu(self, table)
            elif table == "tp":
                treeview.treeAddFindMenu(self, table)
            elif table == "pc":
                treeview.treeAddFindMenu(self, table)
            else:
                treeview.treeAddFindMenu(self, table)

        # Final button creation
        add_herd_button = tkinter.Button(mframe, text="Add/Find", command=lambda: handleTempReturn(self, "herd")).grid(row=0, column=1, sticky=tkinter.E)
        add_tech_button = tkinter.Button(mframe, text="Add/Find", command=lambda: handleTempReturn(self, "ft")).grid(row=3, column=1, sticky=tkinter.E)
        add_lTech_button = tkinter.Button(mframe, text="Add/Find", command=lambda: handleTempReturn(self, "lt")).grid(row=7, column=1, sticky=tkinter.E)
        add_process_button = tkinter.Button(mframe, text="Add/Find", command=lambda: handleTempReturn(self, "tp")).grid(row=8, column=1, sticky=tkinter.E)
        add_testp_button = tkinter.Button(mframe, text="Add/Find", command=lambda: handleTempReturn(self, "pc")).grid(row=10, column=1, sticky=tkinter.E)

        submit_button = tkinter.Button(master=bframe, text="Submit", command=submitReport)
        submit_button.grid(row=17, column=0, sticky='E')

        cancel_button = tkinter.Button(master=bframe, text="Cancel", command=lambda: btnAction.cancel(master_r))
        cancel_button.grid(row=17, column=1, sticky='w')


# Choose file and folder methods and return paths
class fileExplore():
    def choose_file(self):
        root = Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        # Print (root.filename)
        self.focus()
        root.destroy()
        return str(root.filename)

    def choose_folder(self):
        root = Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory()
        root.destroy()
        self.focus()
        return folder_selected


# Treeview/Table methods
class treeview():
    # Generates popup based on table being edited
    def treeAddFindMenu(self, tableType):
        master = tkinter.Toplevel()
        master.geometry(main.center(self, master))
        if tableType == "ft":
            master.title("Field Technician List")
        elif tableType == "lt":
            master.title("Lab Technician List")
        elif tableType == "tp":
            master.title("Test Performed List")
        elif tableType == "pc":
            master.title("Processing Center List")
        else:
            master.title("Herd List")

        entry_text1 = StringVar()

        # Buttons and bindings
        if tableType == "ft":
            data = ("Field Technician Number", "Field Technician Name")
        elif tableType == "lt":
            data = ("Lab Technician ID", "Lab Technician Name")
        elif tableType == "tp":
            data = ("Test Performed Name", "")
        elif tableType == "pc":
            data = ("Processing Center", "")
        else:
            data = ("Herd Code", "Herd Name")
        # Set combobox
        cb = Combobox(master, values=data, width=25)
        cb.grid(row=0, column=0, sticky=W)
        cb.state(['readonly'])
        # Setting combobox default
        if tableType == "ft":
            cb.set("Field Technician Number")
        elif tableType == "lt":
            cb.set("Lab Technician ID")
        elif tableType == "tp":
            cb.set("Test Performed Name")
        elif tableType == "pc":
            cb.set("Processing Center")
        else:
            cb.set("Herd Code")

        # Set entry box
        dEntry = tkinter.Entry(master, width=20, textvariable=entry_text1)
        dEntry.grid(row=0, column=1, sticky=W)

        # Set button
        newHerdBtn = tkinter.Button(master, text="Add", command=lambda: addToTable.addToTable(self, tableType)).grid(row=0, column=1, sticky=E)

        # Set focus
        dEntry.focus_set()

        # Set tree
        if tableType == "ft":
            tree = ttk.Treeview(master, columns=("Field Technician Number", "Field Technician Name"), show=["headings"])
        elif tableType == "lt":
            tree = ttk.Treeview(master, columns=("Lab Technician ID", "Lab Technician Name"), show=["headings"])
        elif tableType == "tp":
            tree = ttk.Treeview(master, columns=("Test Performed ID", "Test Performed Name"), show=["headings"])
        elif tableType == "pc":
            tree = ttk.Treeview(master, columns=("Processing Center"), show=["headings"])
        else:
            tree = ttk.Treeview(master, columns=("Herd Code", "Herd Name"), show=["headings"])

        # Set headings and columns
        if tableType == "ft":
            tree.heading('#1', text='Field Technician Number')
            tree.heading('#2', text='Field Technician Name')
        elif tableType == "lt":
            tree.heading('#1', text='Lab Technician ID')
            tree.heading('#2', text='Lab Technician Name')
        elif tableType == "tp":
            tree.heading('#1', text='Test Performed Name')
        elif tableType == "pc":
            tree.heading('#1', text='Processing Center')
        else:
            tree.heading('#1', text='Herd Code')
            tree.heading('#2', text='Herd Name')

        if tableType == "pc":
            tree.column('#1', minwidth=0, width=140, stretch=YES)
        else:
            tree.column('#1', minwidth=0, width=140, stretch=YES)
            tree.column('#2', minwidth=0, width=130, stretch=YES)

        # Set tree to grid
        tree.grid(row=1, column=0, columnspan=2, sticky=tkinter.NSEW)
        treeview = tree

        # Style options for Treeview Table
        style = ttk.Style()
        hStyle = ttk.Style()
        style.configure("Treeview",
                        background="#8BD8BD",
                        foreground="#8BD8BD",
                        rowheight=25,
                        fieldbackground="#8BD8BD"
                        )
        style.configure("Treeview.Heading",
                        background="#8BD8BD",
                        foreground="#243665",
                        rowheight=25,
                        fieldbackground="#8BD8BD"
                        )
        style.map('Treeview', background=[('selected', '#243665')])
        hStyle.map('Treeview.Heading', background=[('selected', '#243665')])

        # Setup scrollbar and set to frame
        verscrlbar = ttk.Scrollbar(master, orient="vertical", command=tree.yview)
        verscrlbar.grid(row=0, column=2, rowspan=4, sticky='nsw')
        tree.configure(yscrollcommand=verscrlbar.set)

        # Populate default db tree
        def populate_list():
            tree.delete(*tree.get_children())
            idList = []

            if tableType == "ft":
                table = sql_class.sqlData("field_tech")
            elif tableType == "lt":
                table = sql_class.sqlData("lab_tech")
            elif tableType == "tp":
                table = sql_class.sqlData("test_performed")
            elif tableType == "pc":
                table = sql_class.sqlData("processing_center")
            else:
                table = sql_class.sqlData("herd")

            sortedFTList = sorted(table)
            # Lab tech needs to be reversed, and reversal logic isn't working
            for i in sortedFTList:
                id = i[0]
                idList.append(id)
            for i in sortedFTList:
                treeview.insert('', 'end', iid=i[0], text=i[0], values=(i))

        # Pupulate entry based on input, run populate list if no entry
        def populateEntry():
            oList = []
            # Get table information from db
            if tableType == "ft":
                oList = sql.tableOutputList("field_tech")
            elif tableType == "lt":
                oList = sql.tableOutputList("lab_tech")
            elif tableType == "tp":
                oList = sql.tableOutputList("test_performed")
            elif tableType == "pc":
                oList = sql.tableOutputList("processing_center")
            else:
                oList = sql.tableOutputList("herd")

            # Sort DB data
            sortedFTList = sorted(oList)
            ftEntry = entry_text1.get()
            outputList = []
            idList = []

            # Based on DB content check if entry is not null and if entry matches, adding to output list to be shown in table
            if tableType == "ft":
                for i in sortedFTList:
                    if cb.get() == "Field Technician Number":
                        if str(i[0]).startswith(ftEntry) and ftEntry != "":
                            outputList.append(i)
                    else:
                        if str(i[1].upper().lower()).startswith(ftEntry.upper().lower()) and ftEntry != "":
                            outputList.append(i)
            elif tableType == "lt":
                for i in sortedFTList:
                    if cb.get() == "Lab Technician ID":
                        if str(i[1]).startswith(ftEntry) and ftEntry != "":
                            outputList.append(i)
                    else:
                        if str(i[0].upper().lower()).startswith(ftEntry.upper().lower()) and ftEntry != "":
                            outputList.append(i)
            elif tableType == "tp":
                for i in sortedFTList:
                    if cb.get() == "Test Performed Name":
                        if str(i[0].upper().lower()).startswith(ftEntry.upper().lower()) and ftEntry != "":
                            outputList.append(i)
                    else:
                        if str(i[1].upper().lower()).startswith(ftEntry.upper().lower()) and ftEntry != "":
                            outputList.append(i)
            elif tableType == "pc":
                for i in sortedFTList:
                    if cb.get() == "Processing Center":
                        if str(i[1]).startswith(ftEntry) and ftEntry != "":
                            outputList.append(i)
                    else:
                        if str(i[0].upper().lower()).startswith(ftEntry.upper().lower()) and ftEntry != "":
                            outputList.append(i)
            else:
                for i in sortedFTList:
                    if cb.get() == "Herd Code":
                        if str(i[0]).startswith(ftEntry) and ftEntry != "":
                            outputList.append(i)
                    else:
                        if str(i[1].upper().lower()).startswith(ftEntry.upper().lower()) and ftEntry != "":
                            outputList.append(i)

            # If nothing in entry field again, populate default list based on current combobox table otherwise output list created above by matching entry with DB values
            if ftEntry == "":
                tree.delete(*tree.get_children())
                populate_list()
            else:
                tree.delete(*tree.get_children())
                if outputList and tableType:
                    for i in outputList:
                        treeview.insert('', 'end', iid=i[0], text=i[0], values=(i))

        # Trace every keypress to check for table updates
        entry_text1.trace("w", lambda *args: populateEntry())

        # When table is in focus method checks if table needs to be updated
        def handle_focus(event):
            if event.widget == master:
                if entry_text1.get():
                    populateEntry()
                else:
                    populate_list()

        master.bind("<FocusIn>", handle_focus)

        # Bind double click to open current selection
        def OnDoubleClick(event):
            curItem = tree.focus()
            outputItem = tree.item(curItem)
            fOutputItem = outputItem['values']
            if fOutputItem:
                edit = addToTable.editTable(self, tableType, fOutputItem, outputItem['text'], master)

        tree.bind("<Double-1>", OnDoubleClick)
        populate_list()


# csv import, export, UI front end
class csvGui():
    # Create window
    def importExport(self):
        sqlClass = sql_class()
        folder = StringVar()
        file = StringVar()
        fileNameVar = StringVar()
        master = tkinter.Toplevel()
        master.title("Import/Export Tool")
        master.resizable(width=True, height=True)

        # Select folder or file path
        def importExport(type):
            if type == "export":
                folder = fileExplore.choose_folder(master)
                browseExp.insert(0, folder)
            else:
                file = fileExplore.choose_file(master)
                browseImp.insert(0, file)

        # Close window
        def closeW():
            btnAction.destroy(master)

        # Submit table name and path to csv tool
        def dSubmit(type):
            datatype = cb.get()
            if datatype == "Herd List":
                datatype = "herd"
            elif datatype == "Field Tech":
                datatype = "field_tech"
            elif datatype == "County":
                datatype = "county"
            elif datatype == "Type of Test":
                datatype = "test_performed"
            else:
                datatype = "lab_report"
            if type == "export":
                folderPath = browseExp.get()
                fFileName = fileNameVar.get()
                sql.csv_tool(self, "export", datatype, folderPath, fFileName)
            else:
                filePath = browseImp.get()
                sql.csv_tool(None, "import", datatype, filePath, None)

        # Import/Export btn and entry creation
        plFrame = tkinter.Frame(master)
        plFrame.grid()

        v0 = IntVar()
        v0.set(1)
        impLabel = Label(plFrame, text="Import Select File").grid(row=1, column=0)
        browseImp = Entry(master=plFrame, width=80, textvariable=file)
        browseImp.grid(row=1, column=1)
        browseButtonImp = Button(plFrame, text="Browse...", command=lambda: importExport("import")).grid(row=1, column=2)

        expLabel = Label(plFrame, text="Export Select Folder").grid(row=2, column=0)
        browseExp = Entry(master=plFrame, width=80, textvariable=folder)
        browseExp.grid(row=2, column=1)
        browseButtonExp = Button(plFrame, text="Browse...", command=lambda: importExport("export")).grid(row=2, column=2)

        impButton = Button(plFrame, text="Import", command=lambda: [dSubmit("import"), btnAction.destroy(master)]).grid(row=3, column=1, sticky=E)
        expButton = Button(plFrame, text="Export", command=lambda: [dSubmit("export"), btnAction.destroy(master)]).grid(row=3, column=2, sticky=W)
        closeButton = Button(plFrame, text="Close", command=lambda: closeW()).grid(row=3, column=3, sticky=W)

        fileNameLabel = Label(plFrame, text="File Name:").place(x=280, y=54)

        fileName = Entry(plFrame, width=20, textvariable=fileNameVar)
        fileName.place(x=350, y=54)

        # set focus
        browseImp.focus_set()

        dataLabel = Label(plFrame, text="Data Type").grid(row=3, column=0)
        # Set combobox
        data = ("Herd List", "Field Tech", "County", "Lab Report", "Type of Test")
        cb = Combobox(plFrame, values=data)
        cb.grid(row=3, column=1, sticky=W)
        cb.state(['readonly'])
        cb.set("Herd List")


# Lab Report Search and modify
class lab_report_table():
    def labReportTable(self):
        # Configure variables and set UI
        entry_text1 = StringVar()
        error_text = StringVar()
        masterT = tkinter.Toplevel()
        masterT.resizable(width=True, height=True)
        # Configure the root object for the Application
        masterT.title("Lab Reports")
        masterT.grid_rowconfigure(3, weight=1)
        masterT.grid_rowconfigure(0, minsize=1)
        masterT.grid_columnconfigure(3, weight=1)
        masterT.configure(background='#8BD8BD')
        text = tkinter.Text(masterT).configure(font=("Symbol", 12, "bold"))

        masterT['background'] = '#243665'

        # Define the different UI widgets
        column_label = tkinter.Label(masterT, text="Search", width=6, bg='#243665', fg="#8BD8BD", font="Calibri").grid(row=0, column=0)
        # Buttons and bindings
        data = ("Herd Code", "Herd Name", "Date of Test", "Field Technician Number", "Field Technician Name", "Lab Test Date", "Number of Samples", "Lab Technician", "Test Performed", "Processing Center", "Processing Fee")
        cb = Combobox(masterT, values=data, width=25)
        cb.grid(row=0, column=1, sticky=W)
        cb.state(['readonly'])
        cb.set("Herd Code")
        dEntry = tkinter.Entry(masterT, width=20, textvariable=entry_text1)
        dEntry.grid(row=0, column=2)

        delete_button = tkinter.Button(masterT, text="Delete", command=lambda: selectItem(self, "delete"), width=10, fg="#8BD8BD", bg='#243665', font="Calibri", padx=0, pady=0, activebackground="#8BD8BD")
        delete_button.grid(row=0, column=3, sticky=tkinter.E)
        refresh_button = tkinter.Button(masterT, text="Refresh", command=lambda: populate_list(), width=10, fg="#8BD8BD", bg='#243665', font="Calibri", padx=0, pady=0, activebackground="#8BD8BD")
        refresh_button.grid(row=0, column=4, sticky=tkinter.E)
        edit_button = tkinter.Button(masterT, text="Edit", command=lambda: selectItem(self, "edit"), width=10, fg="#8BD8BD", bg='#243665', font="Calibri", padx=0, pady=0, activebackground="#8BD8BD")
        edit_button.grid(row=0, column=5, sticky=tkinter.E)
        submit_button = tkinter.Button(masterT, text="Search", command=lambda: search_table(self, cb.get()), width=10, fg="#8BD8BD", bg='#243665', font="Calibri", padx=0, pady=0, activebackground="#8BD8BD")
        submit_button.grid(row=0, column=6, sticky=tkinter.E)

        exit_button = tkinter.Button(masterT, text="X", command=lambda: btnAction.destroy(masterT), width=1, fg="#8BD8BD", bg='#243665', font="Calibri", padx=0, pady=0, activebackground="#8BD8BD")
        exit_button.grid(row=0, column=7, sticky=tkinter.E)

        errorPrint = tkinter.Label(masterT, textvariable=error_text, fg="red", width=50, bg='#243665', font=("Calibri", 11)).grid(row=0, column=3, sticky=tkinter.W)

        # Set the treeview

        tree = ttk.Treeview(masterT, columns=("Herd Code", "Herd Name", "Date of Test", "Field Technician Number", "Field Technician Name", "Lab Test Date", "Number of Samples", "Lab Technician", "Test Performed", "Processing Center", "Processing Fee"))

        # Set the heading
        tree.heading('#0', text='Report ID')
        tree.heading('#1', text='Herd Code')
        tree.heading('#2', text='Herd Name')
        tree.heading('#3', text='Date of Test')
        tree.heading('#4', text='Field Technician Number')
        tree.heading('#5', text='Field Technician Name')
        tree.heading('#6', text='Lab Test Date')
        tree.heading('#7', text='Number of Samples')
        tree.heading('#8', text='Lab Technician')
        tree.heading('#9', text='Test Performed')
        tree.heading('#10', text='Processing Center')
        tree.heading('#11', text='Processing Fee')

        # Specify attributes of the columns
        tree.column('#0', minwidth=0, width=60, stretch=YES)
        tree.column('#1', minwidth=0, width=75, stretch=YES)
        tree.column('#2', minwidth=0, width=75, stretch=YES)
        tree.column('#3', minwidth=0, width=75, stretch=YES)
        tree.column('#4', minwidth=0, width=140, stretch=YES)
        tree.column('#5', minwidth=0, width=135, stretch=YES)
        tree.column('#6', minwidth=0, width=85, stretch=YES)
        tree.column('#7', minwidth=0, width=120, stretch=YES)
        tree.column('#8', minwidth=0, width=100, stretch=YES)
        tree.column('#9', minwidth=0, width=90, stretch=YES)
        tree.column('#10', minwidth=0, width=120, stretch=YES)
        tree.column('#11', minwidth=0, width=95, stretch=YES)

        tree.grid(row=3, column=0, columnspan=7, sticky=tkinter.NSEW)
        treeview = tree

        # Insert today's date
        def date_input_set(self):
            if cb.get() == 'Date of Test' or cb.get() == 'Lab Test Date':
                dEntry.delete(0, 'end')
                today = date.today()
                d1 = today.strftime("%m/%d/%Y")
                dEntry.insert(0, d1)

        # Date auto-formatting
        def handle_keypress_datebox1(event):
            if cb.get() == 'Date of Test' or cb.get() == 'Lab Test Date':
                eventS1 = dEntry.get()
                try:
                    if eventS1[2] != "/":
                        dEntry.insert("2", "/")
                except:
                    return None
                try:
                    if eventS1[5] != "/":
                        dEntry.insert("5", "/")
                except:
                    return None

        # Character limit checked every keypress
        def character_limit(entry_text2):
            if cb.get() == 'Date of Test' or cb.get() == 'Lab Test Date':
                if len(entry_text2.get()) > 0:
                    entry_text2.set(entry_text2.get()[:10])

        # Select text for easy delete when reselected
        def selectText(event):
            dEntry.selection_range(0, END)

        # Key and event bindings
        dEntry.bind("<FocusIn>", selectText)
        entry_text1.trace("w", lambda *args: character_limit(entry_text1))
        dEntry.bind("<Key>", handle_keypress_datebox1)
        cb.bind("<<ComboboxSelected>>", date_input_set)

        # Set table style
        style = ttk.Style()
        hStyle = ttk.Style()
        style.configure("Treeview",
                        background="#8BD8BD",
                        foreground="#8BD8BD",
                        rowheight=25,
                        fieldbackground="#8BD8BD"
                        )
        style.configure("Treeview.Heading",
                        background="#8BD8BD",
                        foreground="#243665",
                        rowheight=25,
                        fieldbackground="#8BD8BD"
                        )
        style.map('Treeview', background=[('selected', '#243665')])
        hStyle.map('Treeview.Heading', background=[('selected', '#243665')])

        # Set scroll bar
        verscrlbar = ttk.Scrollbar(masterT, orient="vertical", command=tree.yview)
        verscrlbar.grid(row=3, column=7, rowspan=4, sticky='nsw')

        # Configuring treeview
        tree.configure(yscrollcommand=verscrlbar.set)

        # Search table and set results or error
        def search_table(self, column):
            tree.delete(*tree.get_children())
            idList = []
            if column == "Herd Code":
                columnf = "herd_code"
            elif column == "Herd Name":
                columnf = "herd_name"
            elif column == "Date of Test":
                columnf = "date_of_test"
            elif column == "Field Technician Number":
                columnf = "field_technician_number"
            elif column == "Field Technician Name":
                columnf = "field_technician_name"
            elif column == "Lab Test Date":
                columnf = "lab_test_date"
            elif column == "Number of Samples":
                columnf = "num_samples"
            elif column == "Lab Technician":
                columnf = "lab_tech_name"
            elif column == "Test Performed":
                columnf = "test_performed"
            elif column == "Processing Center":
                columnf = "processing_center"
            elif column == "Processing Fee":
                columnf = "processing_fee"

            # Populates default list if empty entry return, otherwise returnFNs search or error message
            if dEntry.get() == "":
                populate_list()
                error_text.set("")
            else:
                table = sorted(sql_class.sqlSearchStartsWith("lab_report", columnf, dEntry.get()))
                if table:
                    for i in table:
                        id = i[0]
                        idList.append(id)
                    for i in table:
                        treeview.insert('', 'end', iid=i[0], text=i[0], values=(i[1:]))
                        error_text.set("")
                else:

                    error_text.set("Error: \"" + str(dEntry.get()) + "\" did not match any records.")

        # Default list
        def populate_list():
            tree.delete(*tree.get_children())
            idList = []
            table = sql_class.sqlData("lab_report")
            for i in table:
                id = i[0]
                idList.append(id)
            idNum = max(idList) + 1
            for i in table:
                treeview.insert('', 'end', iid=i[0], text=i[0], values=(i[1:]))
                idNum += 1

        # Takes item focus after selected and opens edit window
        def selectItem(self, type):
            curItem = tree.focus()
            outputItem = tree.item(curItem)
            fOutputItem = outputItem['values']
            if fOutputItem and type == "edit":
                editOutput = report.newLabReport(self, type, fOutputItem, outputItem['text'])
            elif fOutputItem and type == "delete":
                sql.deleteItem("lab_report", outputItem['text'])
                populate_list()

        # Select current item from doubleclick and send to edit
        def editItemK(self):
            curItem = tree.focus()
            outputItem = tree.item(curItem)
            fOutputItem = outputItem['values']
            if fOutputItem:
                editOutput = report.newLabReport(self, "edit", fOutputItem, outputItem['text'])

        # Bind search table to enter key
        def handleReturn(event):
            search_table(self, cb.get())

        dEntry.bind("<Return>", handleReturn)
        tree.bind("<Return>", handleReturn)
        cb.bind("<Return>", handleReturn)
        tree.bind('<Double-Button-1>', editItemK)

        dEntry.focus()
        populate_list()

    # Check return from edit, if change update all fields based on primary key
    def editItem(self, input, orgInput, id):
        columnList = ["herd_code", "herd_name", "date_of_test", "field_technician_number", "field_technician_name", "lab_test_date", "num_samples", "lab_tech_name", "test_performed", "processing_center", "processing_fee"]
        nSqlCmd = """UPDATE {table} SET {column} = {value} WHERE report_id={idValue}"""
        n = 0
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        for i in input:
            if str(input[n]) != str(orgInput[n]):
                value = "'" + str(input[n]) + "'"
                fSqlCmd = nSqlCmd.format(table="lab_report", column=columnList[n], value=value, idValue=id)
                c.execute(fSqlCmd)
                conn.commit()
                n += 1
            else:
                n += 1
        conn.close()


# SQL class in main (Needs to be condensed in SQL file)
class sql():
    # Takes search value, date or date list, and gets directory to send to create_html_report for either single report or date range
    def rSearch(searchV, date_list, master):
        saveDir = fileExplore.choose_folder(master)
        output_list = []
        labreportprint = create_html_report()
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        # Check if date range is to be printed
        if date_list:
            # get data in date range into output list
            for i in date_list:
                c.execute("SELECT * FROM lab_report WHERE lab_test_date=?", (i,))
                output = c.fetchall()
                output_list.append(output)
            # remove empty lists from tuple
            res = [ele for ele in output_list if ele != []]
            # convert tuple into list
            fres = []
            for i in res:
                for f in i:
                    fres.append(f)
            # submit list to print
            labreportprint.print_lab_report(fres, (str(date_list[0]) + "-" + str(date_list[-1])), saveDir)
        elif not date_list:
            # Get single date from search value and submit to print report
            c.execute("SELECT * FROM lab_report WHERE lab_test_date=?", (searchV,))
            output = c.fetchall()
            labreportprint.print_lab_report(output, searchV, saveDir)
            return output, searchV

    # Get SQL data from SQL file and return in list
    def tableOutputList(table):
        returnValue = sql_class.sqlData(table)
        return returnValue

    # Takes directory, table, path and filename and sends to csv_import_export_tool to be processed
    def csv_tool(self, eDir, table, path, fileName):
        csvTool = csv_import_export_tool()

        if eDir == "export":
            # folderPath = fileExplore.choose_folder(self)
            csvTool.csvCreate(fileName, table, path)

        if eDir == "import":
            # filePath = fileExplore.choose_file(self)
            csvTool.csvImport(path, table)

    # Delete SQL row based on table and ID
    def deleteItem(table, id):
        sql_class.sqlDeleteItem(table, id)


# Table edits for all but Lab Report
class addToTable():
    # Creates UI and fills will called table values (not for lab report) for editing unit
    def editTable(self, table, values, id, masterObj):
        master = tkinter.Toplevel()
        # master.geometry("1200x600")
        master.geometry(main.center(self, master))
        master.resizable(width=True, height=True)
        # Configure the root object for the Application
        if table == "ft":
            label = ["Edit Field Technician", "Name", "ID"]
        elif table == "lt":
            label = ["Edit Lab Technician", "Name", "ID"]
        elif table == "tp":
            label = ["Edit Test Performed", "Name"]
        elif table == "pc":
            label = ["Edit Processing Center", "Name"]
        else:
            label = ["Edit Herd Code", "Name", "ID"]

        # Set title
        master.title(label[0])

        # Set StringVar
        entry1Var = StringVar()
        entry2Var = StringVar()

        # Set stringvar values from tree
        if table != "pc" and table != "tp":
            entry1Var.set(values[1])
            entry2Var.set(values[0])
        else:
            entry1Var.set(values[0])

        # set Labels and Entry Box's for input
        lbl1 = tkinter.Label(master, text=label[0]).grid(row=0, column=0)
        ent1 = tkinter.Entry(master, width=20, textvariable=entry1Var)
        ent1.grid(row=1, column=1)
        lbl2 = tkinter.Label(master, text=label[1]).grid(row=1, column=0)
        if table != "pc" and table != "tp":
            ent2 = tkinter.Entry(master, width=20, textvariable=entry2Var).grid(row=2, column=1)
            lbl3 = tkinter.Label(master, text=label[2]).grid(row=2, column=0)

        addBtn = tkinter.Button(master, text="Edit", command=lambda: dataValidation(master, id, None)).grid(row=3, column=1, sticky=tkinter.E)
        closeBtn = tkinter.Button(master, text="Cancel", command=lambda: master.destroy()).grid(row=3, column=2, sticky=tkinter.W)
        delBtn = tkinter.Button(master, text="Delete", command=lambda: handleDelete(master)).grid(row=3, column=1, sticky=tkinter.W)

        selectBtn = tkinter.Button(master, text="Select", command=lambda: handleSelect(master, masterObj)).grid(row=3, column=0, sticky=tkinter.W)

        # Set focus
        ent1.focus_set()

        # Transfer selected data to corresponding fields
        def handleSelect(self, masterObj):
            input1 = str(entry1Var.get())
            input2 = str(entry2Var.get())
            if table == "lt" or table == "pc" or table == "tp":
                sql_class.setTemp(table + input1)
                dataValidation(master, id, masterObj)
            else:
                sql_class.setTemp(table + input2)
                dataValidation(master, id, masterObj)

        # Handle table item delete
        def handleDelete(self):
            if table == "ft":
                tableOut = "field_tech"
            elif table == "lt":
                tableOut = "lab_tech"
            elif table == "tp":
                tableOut = "test_performed"
            elif table == "pc":
                tableOut = "processing_center"
            else:
                tableOut = "herd"
            sql_class.sqlDeleteItem(tableOut, id)
            self.destroy()

        # Checks Data for change and validates it before submitting (for Select edit)
        def dataValidation(self, id, masterObj):
            print(masterObj)
            input1 = entry1Var.get()
            if table != "pc" and table != "tp":
                input2 = entry2Var.get()
            # If no change it just closes
            if table != "pc" and table != "tp":
                if str(input1) == str(values[0]) and str(input2) == str(values[1]):
                    masterObj.destroy()
                    self.destroy()
                    return None
            else:
                if str(input1) == str(values[0]):
                    masterObj.destroy()
                    self.destroy()
                    return None
            # Data validation, throwing popup error if blank or invalid type
            if table == "pc" or table == "tp":
                input2 = str(0)

            if input1 == "" or input2 == "":
                master = tkinter.Toplevel()
                master.title("Error")
                # master.geometry("1200x600")
                master.geometry(main.center(self, master))
                ErrorLabel = tkinter.Label(master, text="Error: Cannot leave any field blank.", fg="red").grid(row=0, column=0)
            elif input2.isdigit() != True:
                master = tkinter.Toplevel()
                master.title("Error")
                # master.geometry("1200x600")
                master.geometry(main.center(self, master))
                ErrorLabel = tkinter.Label(master, text="Error: ID must be a number.", fg="red").grid(row=0, column=0)
            else:
                # If data is valid get table name and get data
                if table == "ft":
                    tableOut = "field_tech"
                    data = sql_class.sqlData(tableOut)
                elif table == "lt":
                    tableOut = "lab_tech"
                    data = sql_class.sqlData(tableOut)
                elif table == "tp":
                    tableOut = "test_performed"
                    data = sql_class.sqlData(tableOut)
                elif table == "pc":
                    tableOut = "processing_center"
                    data = sql_class.sqlData(tableOut)
                else:
                    tableOut = "herd"
                    data = sql_class.sqlData(tableOut)

                # If data has changed, deletes original row and populates replacement
                sql_class.sqlDeleteItem(tableOut, id)
                if table != "pc" and table != "tp":
                    sql_class.addToSQLTable(input1, input2, table)
                    masterObj.destroy()
                    self.destroy()
                else:
                    sql_class.addToSQLTable(input1, "", table)
                    masterObj.destroy()
                    self.destroy()

    # Adds New row to table
    def addToTable(self, table):
        master = tkinter.Toplevel()
        master.geometry(main.center(self, master))
        master.resizable(width=True, height=True)
        # Configure the root object for the Application
        if table == "ft":
            label = ["Add Field Technician", "Name", "ID"]
        elif table == "lt":
            label = ["Add Lab Technician", "Name", "ID"]
        elif table == "tp":
            label = ["Add Test Performed", "Name"]
        elif table == "pc":
            label = ["Add Processing Center", "Name"]
        else:
            label = ["Add Herd Code", "Name", "ID"]

        master.title(label[0])

        # Set StringVar
        entry1Var = StringVar()
        entry2Var = StringVar()

        # Set Labels and Entry Box's for input
        lbl1 = tkinter.Label(master, text=label[0]).grid(row=0, column=0)
        ent1 = tkinter.Entry(master, width=20, textvariable=entry1Var)
        ent1.grid(row=1, column=1)
        lbl2 = tkinter.Label(master, text=label[1]).grid(row=1, column=0)
        if table != "pc" and table != "tp":
            ent2 = tkinter.Entry(master, width=20, textvariable=entry2Var).grid(row=2, column=1)
            lbl3 = tkinter.Label(master, text=label[2]).grid(row=2, column=0)

        addBtn = tkinter.Button(master, text="Add", command=lambda: dataValidation(master)).grid(row=3, column=1, sticky=tkinter.E)
        closeBtn = tkinter.Button(master, text="Cancel", command=lambda: master.destroy()).grid(row=3, column=2, sticky=tkinter.W)

        def enter(event):
            dataValidation(master)

        master.bind('<Return>', enter)

        # set focus
        ent1.focus_set()

        # Validate data and verify unique before submitting
        def dataValidation(self):
            input1 = entry1Var.get()
            input2 = entry2Var.get()

            if table == "ft":
                data = sql_class.sqlData("field_tech")
            elif table == "lt":
                data = sql_class.sqlData("lab_tech")
            elif table == "tp":
                data = sql_class.sqlData("test_performed")
            elif table == "pc":
                data = sql_class.sqlData("processing_center")
            else:
                data = sql_class.sqlData("herd")

            unique = False
            for i in data:
                if str(i[0]) == input2:
                    unique = True

            if table == "pc" or table == "tp":
                input2 = str(0)

            if input1 == "" or input2 == "":
                master = tkinter.Toplevel()
                master.title("Error")
                # master.geometry("1200x600")
                master.geometry(main.center(self, master))
                ErrorLabel = tkinter.Label(master, text="Error: Cannot leave any field blank.", fg="red").grid(row=0, column=0)
            elif input2.isdigit() != True:
                master = tkinter.Toplevel()
                master.title("Error")
                # master.geometry("1200x600")
                master.geometry(main.center(self, master))
                ErrorLabel = tkinter.Label(master, text="Error: ID must be a number.", fg="red").grid(row=0, column=0)
            elif unique:
                master = tkinter.Toplevel()
                master.title("Error")
                # master.geometry("1200x600")
                master.geometry(main.center(self, master))
                ErrorLabel = tkinter.Label(master, text="Error: ID already in use.", fg="red").grid(row=0, column=0)
            else:
                sql_class.addToSQLTable(input1, input2, table)
                self.destroy()


m = main.mainWindow(None)
