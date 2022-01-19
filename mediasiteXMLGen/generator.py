import pandas as pd
import xml.dom.minidom
import sys


def generate(fileName):
    classesDf = pd.read_csv(fileName, sep='\t', header=1)

    classesDf.rename(columns={'Start Time': 'startTime', 'End Time': 'endTime', 'Schedule #': 'Schedule'}, inplace=True)
    arrValues = classesDf[classesDf['Days'] == 'ARR'].index
    classesDf.drop(arrValues, inplace=True)
    classesDf.dropna(subset=['Days'], inplace=True)

    # Days of the week

    Sunday = 'false'
    Monday = 'false'
    Tuesday = 'false'
    Wednesday = 'false'
    Thursday = 'false'
    Friday = 'false'
    Saturday = 'false'

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
        schedule = row.Schedule
        subject = row.Subject
        days = row.Days
        startTime = row.startTime
        endTime = row.endTime

        duration = str(int(endTime - startTime))
        timeInMinutes = convertTime(duration)
        beginDateTime = convertStartTime(startTime)

        if days == 'MWF':
            Sunday = 'false'
            Monday = 'true'
            Tuesday = 'false'
            Wednesday = 'true'
            Thursday = 'false'
            Friday = 'true'
            Saturday = 'false'

        if days == 'TTH':
            Sunday = 'false'
            Monday = 'false'
            Tuesday = 'true'
            Wednesday = 'false'
            Thursday = 'true'
            Friday = 'false'
            Saturday = 'false'

        if days == 'TTHF':
            Sunday = 'false'
            Monday = 'false'
            Tuesday = 'true'
            Wednesday = 'false'
            Thursday = 'true'
            Friday = 'true'
            Saturday = 'false'

        if days == 'M':
            Sunday = 'false'
            Monday = 'true'
            Tuesday = 'false'
            Wednesday = 'false'
            Thursday = 'false'
            Friday = 'false'
            Saturday = 'false'

        if days == 'T':
            Sunday = 'false'
            Monday = 'false'
            Tuesday = 'true'
            Wednesday = 'false'
            Thursday = 'false'
            Friday = 'false'
            Saturday = 'false'

        if days == 'W':
            Sunday = 'false'
            Monday = 'false'
            Tuesday = 'false'
            Wednesday = 'true'
            Thursday = 'false'
            Friday = 'false'
            Saturday = 'false'

        if days == 'Th':
            Sunday = 'false'
            Monday = 'false'
            Tuesday = 'false'
            Wednesday = 'false'
            Thursday = 'true'
            Friday = 'false'
            Saturday = 'false'

        if days == 'F':
            Sunday = 'false'
            Monday = 'false'
            Tuesday = 'false'
            Wednesday = 'false'
            Thursday = 'false'
            Friday = 'true'
            Saturday = 'false'

        recurrences = '<?xml version="1.0" encoding="utf-8" ?><RecorderScheduleImport xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><RecorderSchedules><RecorderSchedule><RecorderName>My Recorder</RecorderName><PresentationNamingFormat>ScheduleNameAndNumber</PresentationNamingFormat><AdvanceCreationTimeInMinutes>60</AdvanceCreationTimeInMinutes><AdvanceLoadTimeInMinutes>5</AdvanceLoadTimeInMinutes><ScheduledOperations>None</ScheduledOperations><NotifyPresenters>true</NotifyPresenters><NotificationEmailAddresses><NotificationEmailAddress>notification_1@example.com</NotificationEmailAddress><NotificationEmailAddress>notification_2@example.com</NotificationEmailAddress></NotificationEmailAddresses><DeleteInactive>true</DeleteInactive><Modules><ModuleOverride><ModuleId>test::module::1</ModuleId><ModuleName>Test Module From Import</ModuleName></ModuleOverride><ModuleOverride><ModuleId>test::module::2</ModuleId><Permissions><AceEntry><DirectoryEntry>schedule::import::role</DirectoryEntry><Permission>3</Permission></AceEntry></Permissions></ModuleOverride></Modules><Recurrences><Recurrence><BeginDateTime>2022-01-01T{}:00:00</BeginDateTime><EndDateTime>2022-05-30T18:00:00</EndDateTime><RecordingDurationInMinutes>{}</RecordingDurationInMinutes><AlwaysExcludeHolidays>true</AlwaysExcludeHolidays><WeeklySchedule><RecurrenceFrequency>1</RecurrenceFrequency><Sunday>{}</Sunday><Monday>{}</Monday><Tuesday>{}</Tuesday><Wednesday>{}</Wednesday><Thursday>{}</Thursday><Friday>{}</Friday><Saturday>{}</Saturday></WeeklySchedule></Recurrence></Recurrences></RecorderSchedule></RecorderSchedules></RecorderScheduleImport>'.format(beginDateTime, timeInMinutes, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday)
        myXML = xml.dom.minidom.parseString(recurrences)
        recurrencData = myXML.toprettyxml()
        print(recurrencData)


        original_stdout = sys.stdout

        print(recurrencData)

        original_stdout = sys.stdout

        with open('{}_{}.xml'.format(subject, schedule), 'w') as f:
            sys.stdout = f
            print(recurrencData)
            sys.stdout = original_stdout
