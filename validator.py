def validate(data):
    errors = {}
    if data['name'] is None:
        errors['name'] = 'Cant be blank'
    if data['address'] is None:
        errors['address'] = 'Cant be blank'
    return errors