from app.models.budget import Budget, BudgetPeriod
from app import db
from flask_jwt_extended import get_jwt_identity

def create_budget(user_id, category, limit, period):
    if not all([category, limit, period]):
        raise ValueError("Category, limit, and period are required")
    if limit <= 0:
        raise ValueError("Limit must be positive")
    if Budget.query.filter_by(user_id=user_id, category=category).first():
        raise ValueError("Budget for this category already exists")
    budget = Budget(
        user_id=user_id,
        category=category,
        limit=limit,
        period=period
    )
    db.session.add(budget)
    db.session.commit()
    return budget

def get_user_budgets(user_id):
    return Budget.query.filter_by(user_id=user_id).all()

def get_budget(budget_id, user_id):
    budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first()
    if not budget:
        raise ValueError("Budget not found or unauthorized")
    return budget

def update_budget(budget_id, user_id, category=None, limit=None, period=None):
    budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first()
    if not budget:
        raise ValueError("Budget not found or unauthorized")
    if category and category != budget.category:
        if Budget.query.filter_by(user_id=user_id, category=category).first():
            raise ValueError("Budget for this category already exists")
        budget.category = category
    if limit is not None:
        if limit <= 0:
            raise ValueError("Limit must be positive")
        budget.limit = limit
    if period:
        budget.period = period
    db.session.commit()
    return budget

def delete_budget(budget_id, user_id):
    budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first()
    if not budget:
        raise ValueError("Budget not found or unauthorized")
    db.session.delete(budget)
    db.session.commit()