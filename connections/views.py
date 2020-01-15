from http import HTTPStatus

import flask
from flask import Blueprint
from sqlalchemy.orm import aliased
from webargs.flaskparser import use_args

from connections.extensions import db
from connections.models.person import Person
from connections.models.connection import Connection, ConnectionType
from connections.schemas import ConnectionSchema, PersonSchema

from connections.util import result_connection_to_json, validate

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
    a_person = aliased(Person)
    result = db.session.query(Connection, Person, a_person) \
        .join(Person, Connection.to_person_id == Person.id) \
        .join(a_person, Connection.from_person_id == a_person.id).all()
    return result_connection_to_json(result), HTTPStatus.OK


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections/<int:connection_id>', methods=['PATCH'])
@use_args(ConnectionSchema(), locations=('json',))
def update_connection(connection_data, connection_id):
    connection = Connection.query.get(connection_id)
    if connection is not None:
        connection.connection_type = connection_data.connection_type
        connection.save()
        return ConnectionSchema().jsonify(connection), HTTPStatus.OK
    else:
        res = {"description": "Connection ID does not exist."}
        return flask.jsonify(res), HTTPStatus.BAD_REQUEST
