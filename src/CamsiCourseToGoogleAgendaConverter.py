# coding=utf-8
import re
import datetime
import pytz
from unidecode import unidecode
from GoogleAgendaEventsBuilder import BuildGoogleAgendaEvent
import GlobalSettings

__author__ = 'Mattijs Korpershoek'


class CamsiCourseToGoogleAgendaConverter:
    def __init__(self):
        self.agendaCourses = []

    def convertCamsiCoursesToGoogleAgendaEvents(self, camsiCourses):
        for camsiCourse in camsiCourses:
            if self.isValidDate(camsiCourse):
                startDate = self.getStartDateIso(camsiCourse)
                endDate = self.getEndDateIso(camsiCourse)
                location = self.getLocation(camsiCourse)
                title = self.getTitle(camsiCourse)
                description = self.getDescription(camsiCourse)

                newCourse = BuildGoogleAgendaEvent(title, location, startDate,
                                                   endDate, description)

                self.agendaCourses.append(newCourse)

        return self.agendaCourses

    def getDateIso(self, camsiCourse):
        date = camsiCourse.content['date']
        dateArray = re.split('/', date)
        dateIso = dateArray[2] + '-' + dateArray[1] + '-' + dateArray[0]
        return dateIso

    def getStartDateIso(self, camsiCourse):
        dateIso = self.getDateIso(camsiCourse)
        utcOffset = self.getUTCOffsetFromDateIso(dateIso)
        timeIso = camsiCourse.content['start'] + ':00.000'
        startDate = dateIso + 'T' + timeIso + utcOffset
        return startDate

    def getEndDateIso(self, camsiCourse):
        dateIso = self.getDateIso(camsiCourse)
        timeIso = camsiCourse.content['end'] + ':00.000'
        utcOffset = self.getUTCOffsetFromDateIso(dateIso)
        endDate = dateIso + 'T' + timeIso + utcOffset
        return endDate

    def getUTCOffsetFromDateIso(self, dateIso):
        timeZoneLocation = GlobalSettings.GoogleCalendarSettings['timeZone']
        dateArray = re.split('-', dateIso)

        year = int(dateArray[0])
        month = int(dateArray[1])
        day = int(dateArray[2])

        return pytz.timezone(timeZoneLocation).localize(
            datetime.datetime(year, month, day)).strftime('%z')

    def getLocation(self, camsiCourse):
        return self.fixEncodingProblems(camsiCourse.content['location'])

    def getDescription(self, camsiCourse):
        return self.fixEncodingProblems(camsiCourse.content['desc'])

    def getTitle(self, camsiCourse):
        return self.fixEncodingProblems(camsiCourse.content['courseName'])

    def isValidDate(self, camsiCourse):
        return camsiCourse.content['date'] != 'Date'

    def fixEncodingProblems(self, string):
        result = re.sub('é', 'e', string)
        result = re.sub('è', 'e', result)
        result = re.sub('à', 'a', result)
        result = re.sub('â', 'a', result)
        result = re.sub('ô', 'o', result)
        result = re.sub('ç', 'c', result)
        result = unidecode(unicode(result))
        return result


