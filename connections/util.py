# util.py
import re

import flask

from connections.models.person import Person
from connections.models.connection import Connection

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


# In order to fulfill requirements of unit test (test_create_person.py)
def validate(person, errors):
    if person.email is None:
        errors["email"] = "Field may not be null"
    if not EMAIL_REGEX.match(person.email):
        errors["email"] = "Not a valid email address."
    if person.first_name is None:
        errors["first_name"] = "Field may not be null"
    return False if len(errors) > 0 else True


# Manual to Json conversion as flask.jsonify is limited in this situation
# Probably need to use flask-restful for instance
# Or maybe the object Person can be returned entirely without doing a join ?
def result_connection_to_json(result):
    response = []
    for row in result:
        r_json = {}
        for r in row:
            if isinstance(r, Connection):
                r_json = {"id": str(r.id), "connection_type": r.connection_type.value,
                          "from_person_id": str(r.from_person_id),
                          "to_person_id": str(r.to_person_id)}
            elif isinstance(r, Person):
                direction = ""
                if r_json["to_person_id"] == str(r.id):
                    direction = "to"
                if r_json["from_person_id"] == str(r.id):
                    direction = "from"
                r_json[direction + "_person"] = {"id": str(r.id), "first_name": r.first_name,
                                                 "last_name": r.last_name, "email": r.email}
        response.append(r_json)
    return flask.jsonify(response)
