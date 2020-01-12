from random import randrange

from factory import Faker, Sequence, SubFactory, RelatedFactory, SelfAttribute
from factory.alchemy import SQLAlchemyModelFactory

from connections.database import db
from connections.models.connection import Connection
from connections.models.person import Person


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:

        abstract = True
        sqlalchemy_session = db.session


class PersonFactory(BaseFactory):
    """Person factory."""
    id = Sequence(lambda n: randrange(100000))

    email = Sequence(lambda n: f'person{n}@example.com')
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    class Meta:

        model = Person


class ConnectionFactory(BaseFactory):
    """Connection factory."""

    connection_type = 'friend'

    from_person_id = SubFactory(PersonFactory)
    to_person_id = SubFactory(PersonFactory)

    class Meta:

        model = Connection
