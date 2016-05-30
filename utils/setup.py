from app.models import Blazer

genders = ['M', 'F']
sizes = ['XS', 'S', 'M', 'L', 'XL']

for (_, gender) in enumerate(genders):
    for (_, size) in enumerate(sizes):
        for i in range(10):
            serial_number = gender + str(i) + size
            blazer = Blazer(
                serial_number=serial_number,
                size=size,
                gender=gender,
                booked=False
            )
            blazer.put()
