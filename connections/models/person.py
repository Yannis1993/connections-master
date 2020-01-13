from pprint import pprint

from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)

    connections = db.relationship('Connection', foreign_keys='Connection.from_person_id')

    def mutual_friends(self, target):
        mutual_friends = []
        for connection_target in target.connections:
            for connection_self in self.connections:
                if connection_target.connection_type == 'friend' \
                    and connection_self.connection_type == 'friend' \
                    and connection_target.to_person_id == connection_self.to_person_id:
                    mutual_friends.append(Person.query.get(connection_target.to_person_id))
        return mutual_friends
