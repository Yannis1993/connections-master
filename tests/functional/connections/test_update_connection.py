from http import HTTPStatus

from tests.factories import PersonFactory, ConnectionFactory


def test_can_update_connection(db, testapp):
    ConnectionFactory(from_person_id=PersonFactory().id, to_person_id=PersonFactory().id,
                      connection_type="friend")
    db.session.commit()
    payload = {
        'connection_type': 'mother'
    }
    res = testapp.patch('/connections/1', json=payload)

    assert res.status_code == HTTPStatus.OK
    assert 'id' in res.json
    assert res.json["connection_type"] == 'mother'

    bad_id = testapp.patch('/connections/99999444', json=payload)

    assert bad_id.status_code == HTTPStatus.BAD_REQUEST
    assert bad_id.json['description'] == 'Connection ID does not exist.'
