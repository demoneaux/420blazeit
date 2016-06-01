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


class AboutHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        try:
            spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
            rangeName = 'Class Data!A2:E'
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId,
                range=rangeName
            ).execute(
                http=decorator.http()
            )
            values = result.get('values', [])

            if not values:
                self.response.write('No data found.')
            else:
                self.response.write('Name, Major:')
                for row in values:
                    # Print columns A and E,
                    # which correspond to indices 0 and 4.
                    self.response.write('%s, %s' % (row[0], row[4]))
        except client.AccessTokenRefreshError:
            self.redirect('/oauth-test')

app = webapp2.WSGIApplication([
    ('/oauth-test', OauthHandler),
    ('/oauth-test-page', AboutHandler),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
