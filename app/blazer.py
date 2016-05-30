#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb

from utils import template
from app.models import Blazer

class BlazerHandler(webapp2.RequestHandler):
    def get(self, key):
        blazer = Blazer.query(Blazer.serial_number == key).get()

        template.send(self, 'blazer.html', {
            'title': 'Blazer: ' + blazer.serial_number,
            'blazer': blazer
        })

class BlazerBookHandler(webapp2.RequestHandler):
    def post(self, key):
        blazer = Blazer.query(Blazer.serial_number == key).get()
        blazer.booked = True
        blazer.put()

        self.redirect('/blazer/' + key)

class BlazerReturnHandler(webapp2.RequestHandler):
    def post(self, key):
        blazer = Blazer.query(Blazer.serial_number == key).get()
        blazer.booked = False
        blazer.put()

        self.redirect('/blazer/' + key)

app = webapp2.WSGIApplication([
    ('/blazer/(.*?)/book', BlazerBookHandler),
    ('/blazer/(.*?)/return', BlazerReturnHandler),
    ('/blazer/(.+)', BlazerHandler)
], debug=True)
