from http import HTTPStatus
from pprint import pprint

from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'id',
    'to_person',
    'to_person_id',
    'from_person',
    'from_person_id',
    'connection_type'
]


def test_can_get_connections(db, testapp):
    ConnectionFactory.create_batch(5, from_person_id=PersonFactory(), to_person_id=PersonFactory())

    db.session.commit()

    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 5
    pprint(res.json)
    for connection in res.json:
        for field in EXPECTED_FIELDS:
            assert field in connection
