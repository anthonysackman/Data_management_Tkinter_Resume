import datetime
import os
import webbrowser

from pynput.keyboard import Key, Controller


# Create HTML report for printing and open
class create_html_report():
    # Print lab report (Main Report)
    def print_lab_report(self, input, date, dir):
        htmlPrintFileString = """{Directory}\%s-LabReport.html"""
        htmlPrintFileString = htmlPrintFileString.format(Directory=dir)
        nDate = None
        dateRangeList = None
        dateObjectList = []

        # Check if date is a date range, create list based on range and prepare for datetime object creation
        if '-' in date:
            dateRangeList = date.split('-')
            dateRangeList = [dateIndex.replace('/', '-') for dateIndex in dateRangeList]
        else:
            nDate = str(date).replace("/", "-")

        # HTML header and CSS to be formatted based on report
        unfHeaderHtml = """<body><h1 class="labreport-header"> Lab Report - {fDate}</h1><button type="button" class="button" onclick="window.print()">Print</button><table class="labreport-table" cellspacing="0"><thead><tr><td class="labreport-header-cell">Herdcode</td><td class="labreport-header-cell">Herd Name</td><td class="labreport-header-cell">Date Of Test</td><td class="labreport-header-cell">Date Of Lab Test</td><td class="labreport-header-cell">Number Of Samples</td><td class="labreport-header-cell">Lab Test Performed</td><td class="labreport-header-cell">Processing center</td><td class="labreport-header-cell">Processing Center Fee</td><td class="labreport-header-cell">☐</td></tr></thead><tbody>"""
        headerCss = (
            r"""<html><head><title> Lab Report</title><style type="text/css">.labreport-table { border: 1px solid black; width: 800px; }.labreport-header-cell {white-space: nowrap; border-bottom: 1px solid black;border-right: 1px solid black; text-align: center;padding-top: 5px;padding-right: 5px;padding-bottom: 5px;padding-left: 5px; }.labreport-cell {white-space: nowrap; font-size: 16; border-bottom: 1px solid gray;text-align: center;padding-top: 1px;padding-right: 1px;padding-left: 1px; }.button { border: 1px solid black; color: black; padding: 4px 8px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;}</style></head>""")

        # Based on singular date or date range, create date time objects and format into HTML header
        if nDate:
            htmlPrintFile = open(htmlPrintFileString % (nDate), "w+", encoding='utf-8')
            dateObject = datetime.datetime(int(date[6:10]), int(date[0:2]), int(date[3:5]))
            headerHtml = unfHeaderHtml.format(fDate=dateObject.strftime("%A %b %d, %Y"))
        else:
            htmlPrintFile = open(htmlPrintFileString % (dateRangeList[0] + '-' + dateRangeList[1]), "w+", encoding='utf-8')
            dateObjectList = [dateObjectList.append(datetime.datetime(int(x[6:10]), int(x[0:2]), int(x[3:5]))) for x in dateRangeList]
            dateObjectStart = datetime.datetime(int(dateRangeList[0][6:10]), int(dateRangeList[0][0:2]), int(dateRangeList[0][3:5])).strftime("%A %b %d, %Y")
            dateObjectEnd = datetime.datetime(int(dateRangeList[1][6:10]), int(dateRangeList[1][0:2]), int(dateRangeList[1][3:5])).strftime("%A %b %d, %Y")
            headerHtml = unfHeaderHtml.format(fDate=str(dateObjectStart + " - " + dateObjectEnd))

        # Sort tuple list using herdcode
        def getHerdKey(inputList):
            return inputList[1]

        # Sort input on herdcode, build final HTML header
        sortedInput = sorted(input, key=getHerdKey)
        fHeaderHtml = headerCss + headerHtml
        stringEnd = """</tbody></table><p><br /><br /></p><h1>Whatcom ___</h1></body></html>"""

        # For each record create HTML table row and append to header HTML
        for i in sortedInput:
            # format fee
            fee = '${:,.2f}'.format(i[11])
            stringHtmlTable = """<tr class="labreport-table"><td class="labreport-cell">{herdcode}</td><td class="labreport-cell">{herdname}</td><td class="labreport-cell">{date_of_test}</td><td class="labreport-cell">{lab_test_date}</td><td class="labreport-cell">{num_samples}</td><td class="labreport-cell">{test_performed}</td><td class="labreport-cell">{processing_center}</td><td class="labreport-cell">{processing_fee}</td><td class="labreport-cell">☐</td></tr>"""
            newStringHtmlTable = stringHtmlTable.format(herdcode=i[1], herdname=i[2], date_of_test=i[3], lab_test_date=i[6], num_samples=i[7], test_performed=i[9], processing_center=i[10], processing_fee=fee)
            fHeaderHtml = fHeaderHtml + newStringHtmlTable

        # Close HTML document and write document to save dir
        stringPrintFile = fHeaderHtml + stringEnd
        htmlPrintFile.write(stringPrintFile)
        htmlPrintFile.close()

        # Select file and open using default browser
        filePath = htmlPrintFile.name
        webbrowser.open('file://' + os.path.realpath(filePath))

        # Set keyboard control, allow ctrl + P print
        keyboard = Controller()
        keyboard.press(Key.ctrl)
        keyboard.press('p')
        keyboard.release(Key.ctrl)
        keyboard.release('p')

    # Print Monthly report
    def print_month_report(self, month, year, input, dir):
        # Get full directory and create file
        htmlMonthPrintFileString = """{Directory}\%s-MonthReport.html"""
        htmlMonthPrintFileString = htmlMonthPrintFileString.format(Directory=dir)
        htmlMonthPrintFile = open(htmlMonthPrintFileString % (str(month) + "-" + str(year)), "w+")

        # Create HTML to be formatted, and format, set current month as int
        stringPrintFile = """<html><head><title>{month_name} Data For National DHIA Report </title><style type="text/css"> .labreport-table {{ border: 1px solid black; width: 800px; }} .labreport-header-cell {{ border-bottom: 1px solid black;border-right: 1px solid black; background-color: silver;text-align: center;padding-top: 5px;padding-right: 5px;padding-bottom: 5px;padding-left: 5px; }} .labreport-cell {{ border-bottom: 1px solid gray;border-right: 1px solid black;text-align: center;padding-top: 5px;padding-right: 5px;padding-bottom: 5px;padding-left: 5px; }} .button {{ border: 1px solid black; color: black; padding: 4px 8px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;}} </style></head><body><h1 class="labreport-header"> Data For National DHIA Report </h1><button type="button" class="button" onclick="window.print()">Print</button><table class="labreport-table" cellspacing="0"><tbody>"""
        newStringPrintFile = stringPrintFile.format(month_name=(str(month) + "-" + str(year)))
        stringEnd = """</tbody></table></body></html>"""
        date = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
        for index, curmonth in enumerate(date):
            if month == curmonth:
                month = index + 1

        monthDataList = []
        processingCenterList = []
        herdList = []
        herdNum = 0
        totalSamples = 0
        finalMonthReport = newStringPrintFile

        # For each report filter reports that have matching month and year
        for report in input:
            if str(int(str(report[6])[:2])) == str(month) and str(int(str(report[6])[6:])) == str(year):
                monthDataList.append(report)

        # Get list of processing center and herds, and sum of total samples from filtered results
        for report in monthDataList:
            if str(report[10]) not in processingCenterList:
                processingCenterList.append(report[10])
            if str(report[1]) not in herdList:
                herdList.append(report[1])
            totalSamples += int(report[7])

        # Get number of herds
        herdNum = len(herdList)

        # Create HTML table and format fields and data, and append to HTML report
        tableTSString = """<tr class="labreport-table"><td class="labreport-cell">{processC}</td><td class="labreport-cell">{curData}</td></tr>"""
        pTableTSString = tableTSString.format(processC=("Total Samples"), curData=totalSamples)

        finalMonthReport += pTableTSString

        tableTHString = """<tr class="labreport-table"><td class="labreport-cell">{processC}</td><td class="labreport-cell">{curData}</td></tr>"""
        pTableTHString = tableTHString.format(processC=("Total Herds"), curData=herdNum)

        finalMonthReport += pTableTHString

        # Check filtered data for unique herds and sample count per processing center, create table row for each processing center that exists
        pHerdList = []
        processingCenterList = list(dict.fromkeys(processingCenterList))
        processDataList = []
        for center in processingCenterList:
            processHerdNum = 0
            processSampleNum = 0
            tableHString = """<tr class="labreport-table"><td class="labreport-cell">{processC}</td><td class="labreport-cell">{curData}</td></tr>"""
            tableSString = """<tr class="labreport-table"><td class="labreport-cell">{processC}</td><td class="labreport-cell">{curData}</td></tr>"""
            for report in monthDataList:
                if str(report[10]) == str(center):
                    if str(report[1]) not in str(pHerdList):
                        pHerdList.append(report[1])
                        processHerdNum += 1
                    processSampleNum += int(report[7])
            pTableHString = tableHString.format(processC=(str(center) + " Herds"), curData=processHerdNum)
            pTableSString = tableSString.format(processC=(str(center) + " Samples"), curData=processSampleNum)
            finalMonthReport = finalMonthReport + pTableHString + pTableSString

        finalMonthReport += stringEnd

        # Write report to file
        htmlMonthPrintFile.write(finalMonthReport)
        filePath = htmlMonthPrintFile.name
        htmlMonthPrintFile.close()

        # Open file based on file dir in default browser
        webbrowser.open('file://' + os.path.realpath(filePath))

        # Setup Ctrl + P print ability
        keyboard = Controller()
        keyboard.press(Key.ctrl)
        keyboard.press('p')
        keyboard.release(Key.ctrl)
        keyboard.release('p')
