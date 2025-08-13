from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.models.account import Account
from enum import Enum

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey('accounts.id'), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Enum(TransactionType), nullable=False, default=TransactionType.EXPENSE)
    status = db.Column(db.Enum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING)
    note = db.Column(db.String(255))

    def __repr__(self):
        return f'<Transaction {self.type.value} {self.amount} ({self.account_id})>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'account_id': str(self.account_id),
            'amount': float(self.amount),
            'category': self.category,
            'date': self.date.isoformat(),
            'type': self.type.value,
            'status': self.status.value,
            'note': self.note
        }