from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    level = ndb.IntegerProperty()

class Blazer(ndb.Model):
    serial_number = ndb.StringProperty()
    size = ndb.StringProperty(choices=['XS', 'S', 'M', 'L', 'XL'])
    gender = ndb.StringProperty(choices=['M', 'F'])
    booked = ndb.BooleanProperty()
    # booker

# class Booking(ndb.Model):
#     serial_number = ndb.StringProperty()
#     size = ndb.StringProperty(choices=['XS', 'S', 'M', 'L', 'XL'])
#     gender = ndb.StringProperty(choices=['M', 'F'])
#     user = ndb.