import urllib
from GoogleAgendaCalendarUtils import GoogleAgendaCalendarUtils
from GoogleAgendaServiceBuilder import BuildGoogleAgendaService
import GlobalSettings
from CamsiCourseParser import CamsiCourseParser
from CamsiCourseToGoogleAgendaConverter import CamsiCourseToGoogleAgendaConverter
import argparse
from oauth2client import tools

__author__ = 'Mattijs Korpershoek'

calendarName = GlobalSettings.GoogleCalendarSettings['calendarName']
timeZone = GlobalSettings.GoogleCalendarSettings['timeZone']
planningUrl = GlobalSettings.CamsiWebSettings['planningUrl']
localFileName = GlobalSettings.CamsiWebSettings['localFileName']

parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()

print '[*] Program started with following settings:'
GlobalSettings.printSettings()

service = BuildGoogleAgendaService(flags)
calendarUtils = GoogleAgendaCalendarUtils(service)
myCalendar = calendarUtils.getCalendarIfAlreadyExists(calendarName)

if calendarUtils.isValidCalendar(myCalendar):
    print 'Calendar', calendarName, 'already exists! Clearing it ...'
    numberOfItemsCleared = calendarUtils.deleteAllEventsFromCalendar(myCalendar)
    print '[-] Deleted', numberOfItemsCleared, 'item(s) from', calendarName, 'calendar'
else:
    newCalendar = calendarUtils.createNewCalendarFromName(calendarName, timeZone)
    print '[+] Added', calendarName, 'to Google Agenda account'
    myCalendar = newCalendar

print '[*] Downloading new planning file ...'
urllib.urlretrieve(planningUrl, localFileName)
print '[*] Planning file saved as', localFileName

print '[*] Parsing', localFileName, '...'
camsiCourseParser = CamsiCourseParser(localFileName)
camsiCourseParser.parse()
print '[*] Parsing', localFileName, ': DONE'

camsiCourses = camsiCourseParser.Courses

print '[*] Converting courses to Google Agenda Events ...'
converter = CamsiCourseToGoogleAgendaConverter()
camsiAgendaEvents = converter.convertCamsiCoursesToGoogleAgendaEvents(camsiCourses)
print '[*] Converting courses to Google Agenda Events: DONE'

print '[+] Adding Google Agenda Events to', calendarName, '...'
numberOfItemsAdded = calendarUtils.addEventsToCalendar(camsiAgendaEvents, myCalendar)
print '[+] Added', numberOfItemsAdded, 'event(s) to', calendarName, 'calendar'






