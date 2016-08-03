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
    # todo: remove repetition and cleanup code
    if size not in order[gender]:
        order[gender][str(size)] = (start, end)
    return order


def create_blazer(row):
    borrower = {
        'name': '',
        'class': '',
        'contact': '',
        'date_borrowed': ''
    }
    if len(row) > 4:
        borrower['name'] = row[4]
        borrower['class'] = row[5]
        borrower['contact'] = row[6]
        borrower['date_borrowed'] = row[7]

    return Blazer(
        serial_number=row[0],
        gender=row[1],
        size=row[2],
        booked=True if row[3] == 'Yes' else False,
        borrower=borrower
    )


class Blazer():
    def __init__(self, serial_number, gender, size, booked, borrower):
        self.serial_number = serial_number
        self.gender = gender
        self.size = size
        self.booked = booked
        self.borrower = borrower

    def __str__(self):
        return '<Blazer %s %s:%s%s>' % (
            self.serial_number,
            self.gender,
            self.size,
            ' Booked' if self.booked else ''
        )
