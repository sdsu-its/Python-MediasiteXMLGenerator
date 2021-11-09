import pandas as pd
import xml.dom.minidom
import sys







def generate(fileName):

    classesDf = pd.read_csv(fileName, sep='\t', header=1)

    classesDf.rename(columns={'Start Time': 'startTime', 'End Time': 'endTime', 'Schedule #': 'Schedule'}, inplace=True)
    arrValues = classesDf[classesDf['Days'] == 'ARR'].index
    classesDf.drop(arrValues, inplace=True)
    classesDf.dropna(subset=['Days'], inplace=True)

    daysList      = classesDf['Days'].to_list()
    startTimeList = classesDf['startTime'].to_list()
    endTimeList   = classesDf['endTime'].to_list()

    row1 = classesDf.loc[0]
    row2 = classesDf.loc[1]
    
    # Days of the week

    Sunday    = 'false'
    Monday    = 'false'
    Tuesday   = 'false'
    Wednesday = 'false'
    Thursday  = 'false'
    Friday    = 'false'
    Saturday  = 'false'



    def convertStartTime(x):

        xToInt = int(float(x))
        xToStr = str(xToInt)
        splitStr = xToStr.split('0')
        extractTime = splitStr[0]
        if len(extractTime) == 1:

            extractTime = '0' + extractTime
            return extractTime

        else:
            return extractTime

    def convertTime(x):

        hour = int(x[0])
        minutes = hour * 60
        totalTime = minutes + int(x[1:])
        return totalTime



    recurenceArray = []
    scheduleArray = []
    subjectArray = []

    for row in classesDf.itertuples():
        schedule    = row.Schedule
        subject     = row.Subject
        days        = row.Days
        startTime   = row.startTime
        endTime     = row.endTime

        duration      = str(int(endTime - startTime))
        timeInMinutes = convertTime(duration)
        beginDateTime = convertStartTime(startTime)

        if days == 'MWF':
            Sunday     = 'false'
            Monday     = 'true'
            Tuesday    = 'false'
            Wednesday  = 'true'
            Thursday   = 'false'
            Friday     = 'true'
            Saturday   = 'false'

        if days == 'TTH':
            Sunday    = 'false'
            Monday    = 'false'
            Tuesday   = 'true'
            Wednesday = 'false'
            Thursday  = 'true'
            Friday    = 'false'
            Saturday  = 'false'

        if days == 'TTHF':
            Sunday    = 'false'
            Monday    = 'false'
            Tuesday   = 'true'
            Wednesday = 'false'
            Thursday  = 'true'
            Friday    = 'true'
            Saturday  = 'false'

        if days == 'M':
            Sunday    = 'false'
            Monday    = 'true'
            Tuesday   = 'false'
            Wednesday = 'false'
            Thursday  = 'false'
            Friday    = 'false'
            Saturday  = 'false'

        if days == 'T':
            Sunday    = 'false'
            Monday    = 'false'
            Tuesday   = 'true'
            Wednesday = 'false'
            Thursday  = 'false'
            Friday    = 'false'
            Saturday  = 'false'

        if days == 'W':
            Sunday    = 'false'
            Monday    = 'false'
            Tuesday   = 'false'
            Wednesday = 'true'
            Thursday  = 'false'
            Friday    = 'false'
            Saturday  = 'false'

        if days == 'Th':
            Sunday    = 'false'
            Monday    = 'false'
            Tuesday   = 'false'
            Wednesday = 'false'
            Thursday  = 'true'
            Friday    = 'false'
            Saturday  = 'false'

        if days == 'F':
            Sunday    = 'false'
            Monday    = 'false'
            Tuesday   = 'false'
            Wednesday = 'false'
            Thursday  = 'false'
            Friday    = 'true'
            Saturday  = 'false'

        recurrences = '<RecorderSchedule xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><Recurrences><Recurrence><BeginDateTime>2022-01-01T{}:00:00</BeginDateTime><EndDateTime>2022-05-30T18:00:00</EndDateTime><RecordingDurationInMinutes>{}</RecordingDurationInMinutes><AlwaysExcludeHolidays>true</AlwaysExcludeHolidays><WeeklySchedule><RecurrenceFrequency>1</RecurrenceFrequency><Sunday>{}</Sunday><Monday>{}</Monday><Tuesday>{}</Tuesday><Wednesday>{}</Wednesday><Thursday>{}</Thursday><Friday>{}</Friday><Saturday>{}</Saturday></WeeklySchedule></Recurrence></Recurrences></RecorderSchedule>'.format(
            beginDateTime,
            timeInMinutes, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday)
        myXML = xml.dom.minidom.parseString(recurrences)
        recurrencData = myXML.toprettyxml()
        print(recurrencData)


        original_stdout = sys.stdout

        with open('{}_{}.xml'.format(subject, schedule), 'w') as f:
            sys.stdout = f
            print(recurrencData)
            sys.stdout = original_stdout










