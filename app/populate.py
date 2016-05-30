#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb

from utils import template, setup
from app.models import Blazer

class PopulateHandler(webapp2.RequestHandler):
    def get(self):
        template.send(self, 'populate.html', {
            'title': 'Populate data',
        })
    def post(self):
        setup.populate()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/populate', PopulateHandler)
], debug=True)
