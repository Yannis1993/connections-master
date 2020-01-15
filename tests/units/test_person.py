from tests.factories import ConnectionFactory, PersonFactory


def test_mutual_friends(db):
    instance = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, to_person=instance, from_person=PersonFactory())
    ConnectionFactory.create_batch(5, to_person=target, from_person=PersonFactory())

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person=instance, to_person=f, connection_type='friend')
        ConnectionFactory(from_person=target, to_person=f, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=instance, to_person=decoy, connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy, connection_type='coworker')

    db.session.flush()

    expected_mutual_friend_ids = [f.id for f in mutual_friends]

    results = instance.mutual_friends(target)

    assert len(results) == 3
    for f in results:
        assert f.id in expected_mutual_friend_ids
