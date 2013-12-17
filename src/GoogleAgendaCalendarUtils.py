import random
import simplejson
import time
from apiclient import errors

__author__ = 'Mattijs Korpershoek'


class GoogleAgendaCalendarUtils:
    def __init__(self, GoogleAgendaService):
        self.service = GoogleAgendaService

    def createNewCalendarFromName(self, calendarName, timeZone):
        calendar = {
            'summary': calendarName,
            'timeZone': timeZone,
        }
        created_calendar = self.service.calendars().insert(body=calendar).execute()
        return created_calendar

    def deleteAllEventsFromCalendar(self, calendar):
        numberOfItemsCleared = 0
        page_token = None
        while True:
            events = self.service.events().list(calendarId=calendar['id'], pageToken=page_token).execute()
            for event in events['items']:
                self.deleteEventFromCalendar(event, calendar)
                numberOfItemsCleared += 1
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return numberOfItemsCleared

    def deleteEventFromCalendar(self, event, calendar):
        self.executeWithBackoff('delete', event, calendar)

    def deleteCalendar(self, calendar):
        self.service.calendars().delete(calendarId=calendar['id']).execute()

    def getCalendarIfAlreadyExists(self, calendarName):
        existingCalenderId = None
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                summary = calendar_list_entry['summary']
                if summary == calendarName:
                    existingCalenderId = calendar_list_entry
                    break
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return existingCalenderId

    def addEventsToCalendar(self, events, calendar):
        assert calendar is not None
        assert events is not None

        numberOfItemsAdded = 0
        for event in events:
            self.addEventToCalendar(event, calendar)
            numberOfItemsAdded += 1

        return numberOfItemsAdded

    def isValidCalendar(self, calendar):
        return calendar is not None

    def addEventToCalendar(self, event, calendar):
        self.executeWithBackoff('insert', event, calendar)

    def executeWithBackoff(self, operationType, event, calendar):
        for n in range(0, 5):
            try:
                if operationType == 'insert':
                    self.service.events().insert(calendarId=calendar['id'], body=event).execute()
                    break
                if operationType == 'delete':
                    self.service.events().delete(calendarId=calendar['id'], eventId=event['id']).execute()
                    break
            except errors.HttpError, e:
                error = simplejson.loads(e.content)
                if error.get('code') == 403:
                    # Apply exponential backoff.
                    time.sleep((2 ** n) + random.randint(0, 1000) / 1000)

    def eventToString(self, event):
        return (event['start'])['dateTime'] + ' ' + (event['end'])['dateTime'] + ' ' + str(
            event['location']) + ' ' + str(
            event['summary'])