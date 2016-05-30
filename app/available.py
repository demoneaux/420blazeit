#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb

from utils import template
from app.models import Blazer

class AvailableBlazersHandler(webapp2.RequestHandler):
    def get(self):
    	blazers_query = Blazer.query(Blazer.booked == False).order(
            Blazer.size,
            -Blazer.gender,
            Blazer.serial_number            
        )
        blazers_list = blazers_query.fetch()

        template.send(self, 'blazers.html', {
            'title': 'Available Blazers',
            'blazers': blazers_list,
        })

app = webapp2.WSGIApplication([
    ('/available', AvailableBlazersHandler)
], debug=True)
