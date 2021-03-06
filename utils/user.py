from google.appengine.api import users
from app.models import User


def get_user():
    current_user = users.get_current_user()
    if current_user:
        email = current_user.email()
        user = User.query(User.email == email).get()

        if user:
            return user

        user = User(email=email, level=0)
        if email == 'loans.vjc@gmail.com':
            user.level = 1

        return user


def create_login_url(path):
    return users.create_login_url(path)


def create_logout_url():
    return users.create_logout_url('/')
