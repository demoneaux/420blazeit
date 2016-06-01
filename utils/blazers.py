from app.models import Blazer
import logging

def loaned():
    blazers_query = Blazer.query(Blazer.booked == True).order(
        -Blazer.gender,
        Blazer.size,
        Blazer.serial_number            
    )
    blazers_list = blazers_query.fetch()
    return cleanup(blazers_list)

def available():
    blazers_query = Blazer.query(Blazer.booked == False).order(
        -Blazer.gender,
        Blazer.size,
        Blazer.serial_number            
    )
    blazers_list = blazers_query.fetch()
    return cleanup(blazers_list)

genders = ['M', 'F']
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
        'M': {},
        'F': {},
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
