import os
import webapp2

from googleapiclient import discovery
from oauth2client import client
from oauth2client.contrib import appengine

from utils import template, spreadsheets
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
            values = spreadsheets.get_values(
                'Class Data!A2:D',
                service,
                decorator
            )

            blazers = []
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
            values = spreadsheets.get_values(
                'Class Data!A2:D',
                service,
                decorator
            )

            blazers = []
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


class BlazerHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self, serial_number):
        try:
            values = spreadsheets.get_values(
                'Class Data!A2:A',
                service,
                decorator
            )

            blazer = None
            for i, row in enumerate(values):
                if not blazer and row[0] == serial_number:
                    blazer_row = i + 2
                    blazer_range = 'A%d:D%d' % (blazer_row, blazer_row)
                    blazer_data = spreadsheets.get_values(
                        blazer_range,
                        service,
                        decorator,
                        defaultValue=None
                    )

                    if blazer_data:
                        blazer_data = blazer_data[0]
                        blazer = Blazer(
                            serial_number=blazer_data[0],
                            gender=blazer_data[1],
                            size=blazer_data[2],
                            booked=True if blazer_data[3] == 'Yes' else False
                        )

            template.send(self, 'blazer.html', {
                'title': 'Blazer: ' + serial_number,
                'blazer': blazer
            })
        except client.AccessTokenRefreshError:
            self.redirect('/')


class BlazerBookHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def post(self, serial_number):
        try:
            values = spreadsheets.get_values(
                'Class Data!A2:A',
                service,
                decorator
            )

            for i, row in enumerate(values):
                if row[0] == serial_number:
                    row = i + 2
                    blazer_range = 'Class Data!D%d:D%d' % (row, row)
                    spreadsheets.update_values(
                        blazer_range,
                        {
                            'values': [['Yes']]
                        },
                        service,
                        decorator
                    )

                    self.redirect('/blazer/' + serial_number)
                    return

        except client.AccessTokenRefreshError:
            self.redirect('/blazer/' + serial_number)


class BlazerReturnHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def post(self, serial_number):
        try:
            values = spreadsheets.get_values(
                'Class Data!A2:A',
                service,
                decorator
            )

            for i, row in enumerate(values):
                if row[0] == serial_number:
                    row = i + 2
                    blazer_range = 'Class Data!D%d:D%d' % (row, row)
                    spreadsheets.update_values(
                        blazer_range,
                        {
                            'values': [['No']]
                        },
                        service,
                        decorator
                    )

                    self.redirect('/blazer/' + serial_number)
                    return

        except client.AccessTokenRefreshError:
            self.redirect('/blazer/' + serial_number)

app = webapp2.WSGIApplication([
    ('/available', AvailableBlazersHandler),
    ('/loaned', LoanedBlazersHandler),
    ('/blazer/(.*?)/return', BlazerReturnHandler),
    ('/blazer/(.*?)/book', BlazerBookHandler),
    ('/blazer/(.+)', BlazerHandler),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)