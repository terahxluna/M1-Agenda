__author__ = 'Mattijs Korpershoek'


class CamsiCourse:
    def __init__(self):
        self.content = {'date': None, 'start': None, 'end': None, 'courseName': None, 'location': None, 'desc': None}

    def __repr__(self):
        return str(self.content['courseName']) + ' ' + \
               str(self.content['date']) + ' ' + \
               str(self.content['start']) + ' ' + \
               str(self.content['end']) + ' ' + \
               str(self.content['desc']) + ' ' + \
               str(self.content['location'])

    def __ne__(self, other):
        return self.content != other.content


