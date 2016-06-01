#!/usr/bin/env python

import webapp2

from utils import template, blazers

class AvailableBlazersHandler(webapp2.RequestHandler):
    def get(self):
        template.send(self, 'listings.html', {
            'title': 'Available Blazers',
            'blazers': blazers.available(),
        })

class LoanedBlazersHandler(webapp2.RequestHandler):
    def get(self):
        template.send(self, 'listings.html', {
            'title': 'Loaned Blazers',
            'blazers': blazers.loaned(),
        })

app = webapp2.WSGIApplication([
    ('/loaned', LoanedBlazersHandler),
    ('/available', AvailableBlazersHandler)
], debug=True)
