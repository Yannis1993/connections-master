from tests.factories import ConnectionFactory, PersonFactory


def test_mutual_friends(db):
    instance = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    for x in range(5):
        ConnectionFactory(to_person_id=instance.id, from_person_id=PersonFactory().id)
        ConnectionFactory(to_person_id=target.id, from_person_id=PersonFactory().id)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person_id=instance.id, to_person_id=f.id, connection_type='friend')
        ConnectionFactory(from_person_id=target.id, to_person_id=f.id, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person_id=instance.id, to_person_id=decoy.id, connection_type='coworker')
    ConnectionFactory(from_person_id=target.id, to_person_id=decoy.id, connection_type='coworker')

    db.session.flush()

    expected_mutual_friend_ids = [f.id for f in mutual_friends]

    results = instance.mutual_friends(target)

    assert len(results) == 3
    for f in results:
        assert f.id in expected_mutual_friend_ids
