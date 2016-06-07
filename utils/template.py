import jinja2
import os

from . import user


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), '../')
    ),
    extensions=['jinja2.ext.autoescape']
)


def send(app, name, options):
    template = JINJA_ENVIRONMENT.get_template('templates/' + name)
    app.response.out.write(
        template.render(
            configure(options, app.request)
        )
    )


def configure(options, request):
    curr_user = user.get_user()
    options['user'] = curr_user

    if not curr_user:
        options['loginUrl'] = user.create_login_url(request.path)
    else:
        options['logoutUrl'] = user.create_logout_url()

    return options
