#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb

from utils import template
from app.models import Blazer

class LoanedBlazersHandler(webapp2.RequestHandler):
    def get(self):
    	blazers_query = Blazer.query(Blazer.booked == True).order(
            Blazer.size,
            -Blazer.gender,
            Blazer.serial_number            
        )
        blazers_list = blazers_query.fetch()

        template.send(self, 'blazers.html', {
            'title': 'Loaned Blazers',
            'blazers': blazers_list,
        })

app = webapp2.WSGIApplication([
    ('/loaned', LoanedBlazersHandler)
], debug=True)
