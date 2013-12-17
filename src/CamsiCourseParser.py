from HTMLParser import HTMLParser
import copy
from CamsiCourse import CamsiCourse

__author__ = 'Mattijs Korpershoek'


class CamsiCourseParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.currentCourse = CamsiCourse()
        self.previousCourse = CamsiCourse()
        self.Courses = []
        self.fieldIndex = 0
        self.contentToParse = ''

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    # Warning: this may be changed if the calendars layout changes
    def FoundEventField(self):
        return self.lasttag == 'font'

    def ReinitialiseFieldIndex(self):
        self.fieldIndex = 0

    def handle_data(self, data):
        #print data, self.lasttag
        if self.FoundEventField():
            if self.isEndingEventField(data):
                if self.currentCourseIsDifferentFromPreviousCourse():
                    newCourse = copy.deepcopy(self.currentCourse)
                    self.Courses.append(newCourse)
                    self.previousCourse = copy.deepcopy(self.currentCourse)

                self.ReinitialiseFieldIndex()

            else:
                self.currentCourse.updateFieldWithIndex(self.fieldIndex, data)
                self.fieldIndex += 1

    def isEndingEventField(self, field):
        return str(field).isspace() and self.fieldIndex >= 5

    def printCourses(self):
        print self.Courses

    def currentCourseIsDifferentFromPreviousCourse(self):
        return self.currentCourse != self.previousCourse

    def setParseContent(self, pathFileToParse):
        global downloadedCamsiCalendarFile, line
        downloadedCamsiCalendarFile = open(pathFileToParse, 'r')
        for line in downloadedCamsiCalendarFile:
            self.contentToParse += line

    def parse(self):
        self.feed(self.contentToParse)