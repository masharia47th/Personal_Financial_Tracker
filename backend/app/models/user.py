from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    currency = db.Column(db.String(3), default='USD')

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'currency': self.currency
        }