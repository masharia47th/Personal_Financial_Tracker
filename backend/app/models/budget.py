from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.models.user import User
from enum import Enum

class BudgetPeriod(Enum):
    ONE_DAY = "1 day"
    TWO_DAYS = "2 days"
    ONE_WEEK = "1 week"
    ONE_MONTH = "1 month"
    THREE_MONTHS = "3 months"
    SIX_MONTHS = "6 months"
    ONE_YEAR = "1 year"

class Budget(db.Model):
    __tablename__ = 'budgets'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    limit = db.Column(db.Numeric(15, 2), nullable=False)
    period = db.Column(db.Enum(BudgetPeriod), nullable=False, default=BudgetPeriod.ONE_MONTH)

    def __repr__(self):
        return f'<Budget {self.category} {self.limit} ({self.user_id})>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'category': self.category,
            'limit': float(self.limit),
            'period': self.period.value
        }