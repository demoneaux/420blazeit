import webapp2
import logging

from utils import user, template


class MainHandler(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()

        if not curr_user:
            # exit early if logged out
            template.send(self, 'logout.html', {
                'title': 'Home',
                'user': None
            })
            return
        elif curr_user.level == 0:
            # not a vjc email
            template.send(self, 'logout.html', {
                'title': 'Unauthorised'
            })
        else:
            template.send(self, 'home.html', {
                'title': 'Home'
            })


def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)


def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(500)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
