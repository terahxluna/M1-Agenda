__author__ = 'Mattijs Korpershoek'

# usage: newEvent = BuildGoogleAgendaEvent(myName, myLocation, datetime.today(), datetime.tomorrow())
#
# example:
# date = datetime.datetime
# myBirthday = datetime.datetime(2013, 11, 1, 12, 30, 45)
# myEvent = BuildGoogleAgendaEvent("DescriptionDeOuf", "Paris", date.today().isoformat(), date.today().isoformat())
# myBirthdayEvent = BuildGoogleAgendaEvent("Mon 23e Anniversaire", "secret", myBirthday.isoformat(),
# myBirthday.isoformat())


def BuildGoogleAgendaEvent(summary, location, startDateTime, endDateTime, description):
    event = {
        'start': {
            'dateTime': startDateTime
        },
        'end': {
            'dateTime': endDateTime
        },
        'summary': summary,
        'location': location,
        'description': description,
        'reminders': {
            'useDefault': 'true'
        },

    }
    return event