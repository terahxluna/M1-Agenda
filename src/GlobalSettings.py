__author__ = 'Mattijs Korpershoek'

GoogleCalendarSettings = {
    'calendarName': 'M1 G5.1',
    'timeZone': 'Europe/Paris',
}

CamsiWebSettings = {
    'planningUrl': 'https://celcatfsi.ups-tlse.fr/FSIpargroupes/g776.xml',
    'localFileName': 'planning.xml'
}


def printSettings():
    print GoogleCalendarSettings, CamsiWebSettings

