from http import HTTPStatus

from tests.factories import PersonFactory, ConnectionFactory


def test_can_update_connection(db, testapp):
    person = ConnectionFactory(from_person=PersonFactory(), to_person_id=PersonFactory(),
                               connection_type="friend")
    db.session.commit()
    payload = {
        'connection_type': 'mother'
    }
    res = testapp.patch('/connections/' + str(person.id), json=payload)

    assert res.status_code == HTTPStatus.OK
    assert 'id' in res.json
    assert res.json["connection_type"] == 'mother'

    bad_id = testapp.patch('/connections/99999444', json=payload)

    assert bad_id.status_code == HTTPStatus.BAD_REQUEST
    assert bad_id.json['description'] == 'Connection ID does not exist.'
