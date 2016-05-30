from app.models import Blazer

genders = ['M', 'F']
sizes = ['XS', 'S', 'M', 'L', 'XL']

def populate():
    for (_, gender) in enumerate(genders):
        for (_, size) in enumerate(sizes):
            for i in range(10):
                serial_number = gender + str(i) + size
                blazer = Blazer.query(Blazer.serial_number == serial_number).fetch(1)
                if not blazer:
                    blazer = Blazer(
                        serial_number=serial_number,
                        size=size,
                        gender=gender,
                        booked=False
                    )
                    blazer.put()
