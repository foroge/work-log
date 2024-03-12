import flask
from . import db_session
from flask import jsonify, make_response, request, url_for, render_template
from .users import User
from requests import post, get
import os


blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('surname', 'name', 'age', "position", "speciality",
                                    "address", "email", "hashed_password", "dep_id", "city_from"))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'users':
                users.to_dict(only=('surname', 'name', 'age', "position", "speciality",
                                    "address", "email", "hashed_password", "dep_id", "city_from"))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', "position", "speciality",
                  "address", "email", "hashed_password", "dep_id", "city_from"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    users = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        address=request.json['address'],
        speciality=request.json['speciality'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password'],
        dep_id=request.json['dep_id'],
        city_from=request.json["city_from"]
    )
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'id': users.id})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def edit_users(users_id):
    char = ['surname', 'name', 'age', "position", "speciality",
            "address", "email", "hashed_password", "dep_id", "city_from"]
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in char for key in request.json):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(users_id)
    for key in request.json:
        setattr(user, key, request.json[key])
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/users_show/<int:id>', methods=['GET'])
def users_show(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    city = user.city_from
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={city}&format=json"
    response = get(geocoder_request)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = ",".join(toponym["Point"]["pos"].split())
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={toponym_coodrinates}&spn=0.06,0.06&l=sat"
    response_next = get(map_request)
    abs_path = os.path.abspath("static/img")
    map_file = os.path.join(abs_path, f"city_{id}.png")
    with open(map_file, "wb") as file:
        file.write(response_next.content)
    path = url_for("static", filename=f"img/city_{id}.png")
    name = user.name
    surname = user.surname
    return render_template('city_image.html', title='Изображение города', path=path, name=name,
                           surname=surname, city=city)