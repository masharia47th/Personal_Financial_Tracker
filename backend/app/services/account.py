from app.models.account import Account
from app import db
from flask_jwt_extended import get_jwt_identity

def create_account(user_id, name, account_type):
    if not name or not account_type:
        raise ValueError("Name and account type are required")
    if Account.query.filter_by(user_id=user_id, name=name).first():
        raise ValueError("Account name already exists for this user")
    account = Account(
        user_id=user_id,
        name=name,
        account_type=account_type,
        balance=0.00
    )
    db.session.add(account)
    db.session.commit()
    return account

def get_user_accounts(user_id):
    return Account.query.filter_by(user_id=user_id).all()

def get_account(account_id, user_id):
    account = Account.query.get(account_id)
    if not account or account.user_id != user_id:
        raise ValueError("Account not found or unauthorized")
    return account

def update_account(account_id, user_id, name=None, account_type=None):
    account = Account.query.get(account_id)
    if not account or account.user_id != user_id:
        raise ValueError("Account not found or unauthorized")
    if name:
        if Account.query.filter_by(user_id=user_id, name=name).first():
            raise ValueError("Account name already exists for this user")
        account.name = name
    if account_type:
        account.account_type = account_type
    db.session.commit()
    return account

def delete_account(account_id, user_id):
    account = Account.query.get(account_id)
    if not account or account.user_id != user_id:
        raise ValueError("Account not found or unauthorized")
    db.session.delete(account)
    db.session.commit()