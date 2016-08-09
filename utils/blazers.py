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
