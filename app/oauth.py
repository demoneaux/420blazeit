import os
import webapp2

from googleapiclient import discovery
from oauth2client import client
from oauth2client.contrib import appengine

from utils import template

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


class OauthHandler(webapp2.RequestHandler):
    @decorator.oauth_aware
    def get(self):
        template.send(self, 'grant-oauth.html', {
            'title': 'Test',
            'url': decorator.authorize_url(),
            'has_credentials': decorator.has_credentials()
        })


class OauthViewerHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        try:
            spreadsheetId = '1zAZhntGqfdr8cSjZ0uunVAOQZhXhgDuiJ46gZzpyaPY'
            rangeName = 'Class Data!A2:D'
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId,
                range=rangeName
            ).execute(
                http=decorator.http()
            )
            values = result.get('values', [])

            blazers = []
            if values:
                for row in values:
                    blazer = Blazer(
                        serial_number=row[0],
                        gender=row[1],
                        size=row[2],
                        booked=True if row[3] == 'Yes' else False
                    )
                    blazers.append(blazer)
            template.send(self, 'listings.html', {
                'title': 'Blazers',
                'blazers': blazers
            })
        except client.AccessTokenRefreshError:
            self.redirect('/oauth-test')


class Blazer():
    serial_number = ''
    gender = ''
    size = ''
    booked = False

    def __init__(self, serial_number, gender, size, booked):
        self.serial_number = serial_number
        self.gender = gender
        self.size = size
        self.booked = booked

app = webapp2.WSGIApplication([
    ('/oauth-test', OauthHandler),
    ('/oauth-test-page', OauthViewerHandler),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
