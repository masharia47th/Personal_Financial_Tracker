from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.models.user import User
from enum import Enum

class AccountType(Enum):
    SAVINGS = "savings"
    CHECKING = "checking"
    CASH = "cash"
    INVESTMENT = "investment"

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Numeric(15, 2), default=0.00)
    account_type = db.Column(db.Enum(AccountType), nullable=False, default=AccountType.SAVINGS)

    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def __repr__(self):
        return f'<Account {self.name} ({self.user_id})>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'name': self.name,
            'balance': float(self.balance),
            'account_type': self.account_type.value
        }