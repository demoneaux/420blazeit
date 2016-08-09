import os
import webapp2

from googleapiclient import discovery
from oauth2client import client
from oauth2client.contrib import appengine

from utils import template, spreadsheets
from utils.blazers import create_blazer

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
                'Database!A2:D',
                service,
                decorator
            )

            blazers = []
            for row in values:
                if row[3] == 'No':
                    blazers.append(create_blazer(row))

            template.send(self, 'listings.html', {
                'title': 'Available Blazers',
                'blazers': blazers
            })
        except client.AccessTokenRefreshError:
            self.redirect('/')


class LoanedBlazersHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        try:
            values = spreadsheets.get_values(
                'Database!A2:D',
                service,
                decorator
            )

            blazers = []
            for row in values:
                if row[3] == 'Yes':
                    blazers.append(create_blazer(row))

            template.send(self, 'listings.html', {
                'title': 'Loaned Blazers',
                'blazers': blazers
            })
        except client.AccessTokenRefreshError:
            self.redirect('/')


class BlazerHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self, serial_number):
        try:
            values = spreadsheets.get_values(
                'Database!A2:A',
                service,
                decorator
            )

            blazer = None
            for i, row in enumerate(values):
                if not blazer and row[0] == serial_number:
                    blazer_row = i + 2
                    blazer_range = 'A%d:H%d' % (blazer_row, blazer_row)
                    blazer_data = spreadsheets.get_values(
                        blazer_range,
                        service,
                        decorator,
                        defaultValue=None
                    )

                    if blazer_data:
                        blazer = create_blazer(blazer_data[0])

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
                'Database!A2:A',
                service,
                decorator
            )
            borrower_name = self.request.get('name')
            borrower_class = self.request.get('class')
            borrower_contact = self.request.get('contact')
            borrowed_date = self.request.get('borrowed')

            for i, row in enumerate(values):
                if row[0] == serial_number:
                    row = i + 2
                    blazer_range = 'Database!D%d:H%d' % (row, row)
                    spreadsheets.update_values(
                        blazer_range,
                        {
                            'values': [[
                                'Yes',
                                borrower_name,
                                borrower_class,
                                borrower_contact,
                                borrowed_date
                            ]]
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
                'Database!A2:A',
                service,
                decorator
            )
            id_blazer = serial_number
            returned_date = self.request.get('returned')
            record_values = spreadsheets.get_values(
                'Records!A2:A',
                service,
                decorator
            )

            row_1 = len(record_values)
            row_1 = row_1 + 2

            for i, row in enumerate(values):
                if row[0] == serial_number:
                    row = i + 2
                    blazer_range = 'Database!D%d:H%d' % (row, row)
                    logs = spreadsheets.get_values(
                        blazer_range,
                        service,
                        decorator
                    )
                    borrowed_name = logs[0][1]
                    borrowed_class = logs[0][2]
                    borrowed_contact = logs[0][3]
                    borrowed_date = logs[0][4]
                    spreadsheets.update_values(
                        blazer_range,
                        {
                            'values': [['No', '', '', '', '']]
                        },
                        service,
                        decorator
                    )
                    record_range = 'Records!A%d:F%d' % (row_1, row_1)
                    spreadsheets.update_values(
                        record_range,
                        {
                            'values': [[
                                id_blazer,
                                borrowed_name,
                                borrowed_class,
                                borrowed_contact,
                                borrowed_date,
                                returned_date
                            ]]
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
