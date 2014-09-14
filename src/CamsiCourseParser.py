import xml.etree.ElementTree as ET
import copy
from CamsiCourse import CamsiCourse
import datetime

__author__ = 'Mattijs Korpershoek, Florian Poncabaré'


class CamsiCourseParser():
    def __init__(self, path):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.currentCourse = CamsiCourse()
        self.previousCourse = CamsiCourse()
        self.Courses = []

    def getRawWeeks(self):
        return []

    def printCourses(self):
        print self.Courses

    def currentCourseIsDifferentFromPreviousCourse(self):
        return self.currentCourse != self.previousCourse

    def parse(self):

        weeks = dict()

        for week in self.root.findall('span'):
            date = week.get('date')
            raw = week.find('alleventweeks').text
            weeks[raw] = date

        for event in self.root.findall('event'):
            raw = event.find('rawweeks').text
            day = event.find('day').text
            start = event.find('starttime').text
            end = event.find('endtime').text
            cat = event.find('category').text

            name = ''
            room = ''

            _name = event.find('resources/module/item')
            if(_name != None):
                name = _name.text.encode('ascii', 'ignore')

            if cat == 'TD' or cat == 'TP' or cat == 'COURS' or cat == 'REUNION' or cat == 'SOUTIEN':
                name += ' - ' + cat
            elif cat != None:
                name = cat

            _room = event.find('resources/room/item')
            if(_room != None):
                room = _room.text.encode('ascii', 'ignore')
            
            baseDate = weeks[raw]
            if(baseDate == None):
                continue

            dateStr = baseDate.split("/")
            date = datetime.date(int(dateStr[2]), int(dateStr[1]), int(dateStr[0]))
            offset = datetime.timedelta(int(day))
            date = date + offset


            course = CamsiCourse()
            course.content['date'] = date.strftime("%d/%m/%Y")
            course.content['start'] = start
            course.content['end'] = end
            course.content['courseName'] = name
            course.content['location'] = room
            course.content['desc'] = ""
            self.Courses.append(course)