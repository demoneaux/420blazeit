#!/usr/bin/env python

import webapp2

from utils import template, setup


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
