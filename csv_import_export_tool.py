import sqlite3

from SQL import *


# Tool for inputting CSV data export from machine output and export data from the db in a CSV format
class csv_import_export_tool():
    # Return csv input from file path
    def fileInput(csv):
        fFileInputr = []
        fileInput = open("%s" % (csv), "r")
        fileInputr = fileInput.readlines()
        for i in fileInputr:
            f = i.rstrip()
            fFileInputr.append(f)
        return fFileInputr

    # Get SQL data and return
    def sqlData(table):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        sqlcmd = """SELECT * FROM {table1}"""
        fSqlCmd = sqlcmd.format(table1=table)
        c.execute(fSqlCmd)
        return c.fetchall()

    # Create csv file and header
    def csvCreate(self, fileName, table, filePath):
        sqlClass = sql_class()
        newFile = open("%s.csv" % (filePath + '/' + fileName), 'w+')
        for i in csv_import_export_tool.columnList(table):
            if ',' in i:
                i = i.replace(',', '|comma|')
            newFile.write(i + ",")
        newFile.write("\n")

        # Create body of csv
        list = csv_import_export_tool.sqlData(table)
        for i in list:
            for f in i:
                if ',' in str(f):
                    f = str(f).replace(',', '|comma|')
                newFile.write(str(f) + ',')
            newFile.write("\n")

        # print(list)

    # Import CSV Tool
    def csvImport(self, filePath, table):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        fileInputr = csv_import_export_tool.fileInput(filePath)
        header = fileInputr[0].split('\n')
        headerF = header[0].split(',')
        herdCodeList = []
        for i in fileInputr[1:]:
            fLineList = []
            lineList = i.split(',')
            for field in lineList:
                if '|comma|' in str(field):
                    field = field.replace('|comma|', ',')
                fLineList.append(field)

            # Input data from list, create or replace if needed
            if table == "lab_report":
                c.execute("INSERT OR REPLACE INTO lab_report(report_ID, herd_code, herd_name, date_of_test, field_technician_number, field_technician_name, lab_test_date, num_samples, lab_tech_name, test_performed, processing_center, processing_fee) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                    fLineList[0], fLineList[1], fLineList[2], fLineList[3], fLineList[4], fLineList[5], fLineList[6], fLineList[7], fLineList[8], fLineList[9],
                    fLineList[10], fLineList[11]))
            elif table == "herd":
                c.execute("INSERT OR REPLACE INTO herd(herd_code, herd_name) VALUES (?, ?)", (
                    fLineList[0], fLineList[1]))
            elif table == "field_tech":
                c.execute("INSERT OR REPLACE INTO field_tech(id, name) VALUES (?, ?)", (
                    fLineList[0], fLineList[1]))
            elif table == "test_performed":
                c.execute("INSERT OR REPLACE INTO test_performed(test_performed) VALUES (?)", (
                    fLineList[0]))
            else:
                c.execute("INSERT OR REPLACE INTO county(id, county_name) VALUES (?, ?)", (
                    fLineList[0], fLineList[1]))
        conn.commit()
        conn.close()

    # Get list of column id's
    def columnList(table):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        if table == "lab_report":
            c.execute("SELECT * FROM lab_report")
            col_name_list = [tuple[0] for tuple in c.description]
        elif table == "herd":
            c.execute("SELECT * FROM herd")
            col_name_list = [tuple[0] for tuple in c.description]
        elif table == "field_tech":
            c.execute("SELECT * FROM field_tech")
            col_name_list = [tuple[0] for tuple in c.description]
        elif table == "test_performed":
            c.execute("SELECT * FROM test_performed")
            col_name_list = [tuple[0] for tuple in c.description]
        else:
            c.execute("SELECT * FROM county")
            col_name_list = [tuple[0] for tuple in c.description]

        c.close()
        return col_name_list
