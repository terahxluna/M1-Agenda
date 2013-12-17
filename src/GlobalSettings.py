__author__ = 'Mattijs Korpershoek'

GoogleCalendarSettings = {
    'calendarName': 'Camsi',
    'timeZone': 'Europe/Paris',
}

CamsiWebSettings = {
    'planningUrl': 'http://planning.camsi.fr/ShowListeCreneaux.aspx',
    'localFileName': 'planning.xml'
}


def printSettings():
    print GoogleCalendarSettings, CamsiWebSettings

