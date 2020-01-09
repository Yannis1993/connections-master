from http import HTTPStatus

import flask
from flask import Blueprint
from webargs.flaskparser import use_args

from connections.models.person import Person
from connections.models.connection import Connection
from connections.schemas import ConnectionSchema, PersonSchema

import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    errors = {}
    if validate(person, errors):
        person.save()
        return PersonSchema().jsonify(person), HTTPStatus.CREATED
    else:
        res = {"description": "Input failed validation.", "errors": errors}
        return flask.jsonify(res), HTTPStatus.BAD_REQUEST


@blueprint.route('/connections', methods=['GET'])
def get_connection():
    connection_schema = ConnectionSchema(many=True)
    connection = Connection.query.all()
    return connection_schema.jsonify(connection), HTTPStatus.OK
# TODO: Return with peoples full details


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


def validate(person, errors):
    if person.email is None:
        errors["email"] = "Field may not be null"
    if not EMAIL_REGEX.match(person.email):
        errors["email"] = "Not a valid email address."
    if person.first_name is None:
        errors["first_name"] = "Field may not be null"
    return False if len(errors) > 0 else True
