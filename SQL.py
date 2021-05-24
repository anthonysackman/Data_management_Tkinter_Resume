import sqlite3


# Lower level SQL class
class sql_class():
    # remove temporary value if exists, and set with new value
    def setTemp(value):
        sql_class.delTemp()
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        c.execute('INSERT INTO temp VALUES(?)', (value,))
        conn.commit()
        conn.close()

    # Get temporary value and return
    def getTemp():
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        sqlcmd = """SELECT * FROM temp"""
        c.execute(sqlcmd)
        return c.fetchall()

    # Delete temporary value
    def delTemp():
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        c.execute('DELETE FROM temp;', )
        conn.commit()
        conn.close()

    # Delete sql row based on table and ID
    def sqlDeleteItem(table, id):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        sql_delete_query = """DELETE FROM {tablec} WHERE {idt} = ?"""
        if table == "lab_report":
            sql_delete_query = sql_delete_query.format(tablec=table, idt="report_ID")
        elif table == "county" or table == "field_tech":
            sql_delete_query = sql_delete_query.format(tablec=table, idt="id")
        elif table == "herd":
            sql_delete_query = sql_delete_query.format(tablec=table, idt="herd_code")
        elif table == "lab_tech":
            sql_delete_query = sql_delete_query.format(tablec=table, idt="Lab_tech_ID")
        elif table == "test_performed":
            sql_delete_query = sql_delete_query.format(tablec=table, idt="test_performed")
        elif table == "processing_center":
            sql_delete_query = sql_delete_query.format(tablec=table, idt="processing_center")
        try:
            c.execute(sql_delete_query, (id,))
            conn.commit()
        except sqlite3.Error as error:
            print("Failed ", error)
        finally:
            if (conn):
                conn.close()
                print("the sqlite connection is closed")

    # Format data for better matching
    def formatInput(self, input):
        output = input.lower().upper()
        return output

    # SQL search DB and return matches
    def search_sql(table, column, value):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        sqlcmd = """SELECT * FROM {table1} WHERE {column1}={value}"""
        value = "'" + str(value) + "'"
        fsqlcmd = sqlcmd.format(table1=table, column1=column, value=value)
        c.execute(fsqlcmd)
        output = c.fetchall()
        if not output:
            fsqlcmd = sqlcmd.format(table1=table, column1=column, value=value.lower())
            c.execute(fsqlcmd)
            output = c.fetchall()
            if not output:
                fsqlcmd = sqlcmd.format(table1=table, column1=column, value=value.title())
                c.execute(fsqlcmd)
                output = c.fetchall()
        return output

    # Returns like values from DB that start with value or match
    def sqlSearchStartsWith(table, column, value):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        sqlCmd = """SELECT * FROM {sqlTable} WHERE {sqlColumn} LIKE '{sqlValue}%'""".format(sqlTable=table,
                                                                                            sqlColumn=column,
                                                                                            sqlValue=value)
        c.execute(sqlCmd)
        return c.fetchall()

    # Get table data and return
    def sqlData(table):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        sqlcmd = """SELECT * FROM {table1}"""
        fSqlCmd = sqlcmd.format(table1=table)
        c.execute(fSqlCmd)
        return c.fetchall()

    # Submit lab report
    def submitLabReport(self, input):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='lab_report' ''')

        if c.fetchone()[0] == 1:
            {
                c.execute(
                    "INSERT INTO lab_report(herd_code, herd_name, date_of_test, field_technician_number, field_technician_name, lab_test_date, num_samples, lab_tech_name, test_performed, processing_center, processing_fee)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        input[0], input[1], input[2], input[3], input[4], input[5], input[6], input[7], input[8],
                        input[9],
                        input[10]))
            }
        else:
            c.execute('''CREATE TABLE lab_report
                            (report_ID INTEGER PRIMARY KEY, herd_code, herd_name, date_of_test, field_technician_number, field_technician_name, lab_test_date, num_samples, lab_tech_name, test_performed, processing_center, processing_fee)''')
            c.execute("INSERT INTO lab_report(herd_code, herd_name, date_of_test, field_technician_number, field_technician_name, lab_test_date, num_samples, lab_tech_name, test_performed, processing_center, processing_fee)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                input[0], input[1], input[2], input[3], input[4], input[5], input[6], input[7], input[8], input[9],
                input[10]))

        conn.commit()
        conn.close()

    # Search for lab reports based on date, send to html report for creation and printing
    def rSearch(searchV):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM lab_report WHERE lab_test_date=?", (searchV,))
        labreportprint = create_html_report()
        output = c.fetchall()
        labreportprint.print_lab_report(output, searchV)
        return output, searchV

    # Connect to db and get column headers
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
        elif table == "lab_tech":
            c.execute("SELECT * FROM lab_tech")
            col_name_list = [tuple[0] for tuple in c.description]
        elif table == "test_performed":
            c.execute("SELECT * FROM test_performed")
            col_name_list = [tuple[0] for tuple in c.description]
        elif table == "processing_center":
            c.execute("SELECT * FROM processing_center")
            col_name_list = [tuple[0] for tuple in c.description]
        else:
            c.execute("SELECT * FROM county")
            col_name_list = [tuple[0] for tuple in c.description]

        c.close()
        return col_name_list

    # Create SQL DB and add tables if needed
    def sqlCreate(self):
        tablecreate = True
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='lab_report' ''')

        if c.fetchone()[0] == 1:
            tablecreate = True
        else:
            c.execute('''CREATE TABLE lab_report
                                        (report_ID INTEGER PRIMARY KEY, herd_code, herd_name, date_of_test, field_technician_number, field_technician_name, lab_test_date, num_samples, lab_tech_name, test_performed, processing_center, processing_fee DECIMAL)''')

        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='county' ''')

        if c.fetchone()[0] == 1:
            tablecreate = True
        else:
            c.execute('''CREATE TABLE county
                                                (id INTEGER PRIMARY KEY UNIQUE, county_name)''')

        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='field_tech' ''')

        if c.fetchone()[0] == 1:
            tablecreate = True
        else:
            c.execute('''CREATE TABLE field_tech
                                                        (id INTEGER PRIMARY KEY UNIQUE, name)''')

        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='herd' ''')

        if c.fetchone()[0] == 1:
            tablecreate = True
        else:
            c.execute('''CREATE TABLE herd
                                                        (herd_code INTEGER PRIMARY KEY UNIQUE, herd_name)''')

        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='lab_tech' ''')

        if c.fetchone()[0] == 1:
            tablecreate = True
        else:
            c.execute('''CREATE TABLE lab_tech
                                                        (Lab_tech_ID INTEGER PRIMARY KEY UNIQUE, lab_tech_name)''')

        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='test_performed' ''')

        if c.fetchone()[0] == 1:
            tablecreate = True
        else:
            c.execute('''CREATE TABLE test_performed
                                                                (test_performed UNIQUE)''')

        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='processing_center' ''')

        if c.fetchone()[0] == 1:
            tablecreate = True
        else:
            c.execute('''CREATE TABLE processing_center
                                                                        (processing_center)''')

        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='temp' ''')

        if c.fetchone()[0] == 1:
            tablecreate = True
        else:
            c.execute('''CREATE TABLE temp
                                                                (val1)''')

        conn.commit()
        c.close()

    # Add to SQL DB based on table (except for lab report)
    def addToSQLTable(input1, input2, table):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()

        if table == "herd":
            tableF = "herd"
            headerList = ["herd_name", "herd_code"]
        elif table == "ft":
            tableF = "field_tech"
            headerList = ["name", "id"]
        elif table == "tp":
            tableF = "test_performed"
            headerList = ["test_performed"]
        elif table == "pc":
            tableF = "processing_center"
            headerList = ["processing_center"]
        elif table == "lt":
            tableF = "lab_tech"
            headerList = ["lab_tech_name", "lab_tech_ID"]

        if table == "pc" or table == "tp":
            sql_query = '''INSERT INTO {tables}({header1})  VALUES (?)'''
            sql_query = sql_query.format(tables=tableF, header1=headerList[0])
        else:
            sql_query = '''INSERT INTO {tables}({header1}, {header2})  VALUES (?, ?)'''
            sql_query = sql_query.format(tables=tableF, header1=headerList[0], header2=headerList[1])

        try:
            if table != "pc" and table != "tp":
                c.execute(sql_query, (input1, input2))
            else:
                c.execute(sql_query, (input1,))

            conn.commit()
        except sqlite3.Error as error:
            print("Failed ", error)
            print("SQL Query: " + str(sql_query) + str(input1))
        finally:
            if (conn):
                conn.close()
                print("the sqlite connection is closed")

    # Update existing row based on table
    def editSQLTable(input1, input2, table):
        conn = sqlite3.connect(r'data.db')
        c = conn.cursor()

        if table == "herd":
            tableF = "herd"
            headerList = ["herd_name", "herd_code"]
        elif table == "ft":
            tableF = "field_tech"
            headerList = ["name", "id"]
        elif table == "lt":
            tableF = "lab_tech"
            headerList = ["lab_tech_name", "lab_tech_ID"]

        sql_query = '''UPDATE {tableI} SET {input} = ? WHERE {id} = ?'''
        sql_query = sql_query.format(tableI=tableF, input=headerList[0], id=headerList[1])

        c.execute(sql_query, (input1, input2))
        conn.commit()

        conn.commit()
        conn.close()

# sql_class.sqlCreate(None)
