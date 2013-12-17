__author__ = 'Mattijs Korpershoek'


class CamsiCourse:
    def __init__(self):
        self.content = {'date': None, 'start': None, 'end': None, 'courseName': None, 'teacherName': None,
                        'location': None}

    def __repr__(self):
        return str(self.content['courseName']) + ' ' + \
               str(self.content['date']) + ' ' + \
               str(self.content['start']) + ' ' + \
               str(self.content['end']) + ' ' + \
               str(self.content['location']) + ' ' + \
               str(self.content['teacherName'])

    def __ne__(self, other):
        return self.content != other.content

    def updateFieldWithIndex(self, index, value):
        currentFieldName = self.getCurrentFieldNameFromIndex(index)
        self.content[currentFieldName] = value

    def getCurrentFieldNameFromIndex(self, index):
        if index == 0:
            return 'date'

        if index == 1:
            return 'start'

        if index == 2:
            return 'end'

        if index == 3:
            return 'courseName'

        if index == 4:
            return 'teacherName'

        if index == 5:
            return 'location'

        else:
            return None
