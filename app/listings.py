#!/usr/bin/env python

import os
import webapp2

from googleapiclient import discovery
from oauth2client import client
from oauth2client.contrib import appengine

from utils import template
from utils.blazers import Blazer, cleanup

discoveryServiceUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
service = discovery.build(
    'sheets',
    'v4',
    discoveryServiceUrl=discoveryServiceUrl
)
decorator = appengine.oauth2decorator_from_clientsecrets(
    os.path.join(os.path.dirname(__file__), '../client_secrets.json'),
    scope='https://www.googleapis.com/auth/spreadsheets'
)


class AvailableBlazersHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        try:
            spreadsheetId = '1zAZhntGqfdr8cSjZ0uunVAOQZhXhgDuiJ46gZzpyaPY'
            rangeName = 'Class Data!A2:D'
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId,
                range=rangeName
            ).execute(http=decorator.http())
            values = result.get('values', [])

            blazers = []
            if values:
                for row in values:
                    if row[3] == 'No':
                        blazer = Blazer(
                            serial_number=row[0],
                            gender=row[1],
                            size=row[2],
                            booked=False
                        )
                        blazers.append(blazer)

            template.send(self, 'listings.html', {
                'title': 'Available Blazers',
                'blazers': cleanup(blazers)
            })
        except client.AccessTokenRefreshError:
            self.redirect('/')


class LoanedBlazersHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        try:
            spreadsheetId = '1zAZhntGqfdr8cSjZ0uunVAOQZhXhgDuiJ46gZzpyaPY'
            rangeName = 'Class Data!A2:D'
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId,
                range=rangeName
            ).execute(http=decorator.http())
            values = result.get('values', [])

            blazers = []
            if values:
                for row in values:
                    if row[3] == 'Yes':
                        blazer = Blazer(
                            serial_number=row[0],
                            gender=row[1],
                            size=row[2],
                            booked=True
                        )
                        blazers.append(blazer)

            template.send(self, 'listings.html', {
                'title': 'Loaned Blazers',
                'blazers': cleanup(blazers)
            })
        except client.AccessTokenRefreshError:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/available', AvailableBlazersHandler),
    ('/loaned', LoanedBlazersHandler),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
