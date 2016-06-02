genders = ['Male', 'Female']
sizes = ['XS', 'S', 'M', 'L', 'XL']


def cleanup(blazers):
    order = generate_order(blazers)
    new_blazers = []
    for gender in genders:
        for size in sizes:
            if size in order[gender]:
                start, end = order[gender][size]
                new_blazers.extend(blazers[start:end])
    return new_blazers


def generate_order(blazers):
    order = {
        'Male': {},
        'Female': {}
    }
    gender = ''
    size = ''
    start = 0
    end = 0
    for (i, blazer) in enumerate(blazers):
        if gender == blazer.gender and size == blazer.size:
            end = i + 1
        else:
            if gender and size:
                order[gender][str(size)] = (start, end)
            gender = blazer.gender
            size = blazer.size
            start = i
            end = i + 1
    return order


class Blazer():
    serial_number = ''
    gender = ''
    size = ''
    booked = False

    def __init__(self, serial_number, gender, size, booked):
        self.serial_number = serial_number
        self.gender = gender
        self.size = size
        self.booked = booked
