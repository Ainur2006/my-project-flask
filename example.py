import os

from dotenv import load_dotenv
from flask import (
    Flask, 
    render_template, 
    redirect, 
    url_for,
    flash,
    get_flashed_messages,
    request,
)

from places_repository import PlacesRepository
from validator import validate

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

repo = PlacesRepository(app.config['DATABASE_URL'])

@app.get('/')
def index():
    return render_template('places/home.html')


@app.get('/places/')
def places_get():
    term = request.args.get('term', '').lower()
    places = repo.get_content()
    filtered_places = [
        place 
        for place in places 
        if term in place['name'].lower()
    ]
    return render_template(
        'places/show_all_places.html',
        places=filtered_places,
        search=term,
    )


@app.post('/places')
def places_post():
    place = request.form.to_dict()
    errors = validate(place)
    if errors:
        return render_template(
            'places/new.html',
            place=place,
            errors=errors,
        )
    repo.save(place)
    flash("Место успешно добавлено", "success")
    return redirect(url_for('places_get'))


@app.get('/places/new')
def places_new():
    place = {'name': '', 'address': ''}
    errors = {}
    return render_template(
        'places/new.html',
        place=place,
        errors=errors,
    )


@app.get('/places/<id>')
def places_show(id):
    place = repo.find(id)
    return render_template(
        'places/show.html',
        place=place,
    )


@app.get('/places/<id>/edit')
def places_edit(id):
    place = repo.find(id)
    errors = {}
    return render_template(
        'places/edit.html',
        place=place,
        errors=errors,
    ) 

@app.route('/places/<id>/patch', methods=['POST'])
def places_patch(id):
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            'places/edit.html',
            place=data,
            errors=errors,
        )
    place = repo.find(id)
    data['id'] = place['id']
    repo.save(data)
    flash('Место успешно обновлено', 'success')
    return redirect(url_for('places_get'))

@app.post('/places/<id>/delete')
def places_delete(id):
    repo.destroy(id)
    flash('Место удалено', 'success')
    return redirect(url_for('places_get'))


