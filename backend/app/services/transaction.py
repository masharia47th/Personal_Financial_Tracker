from app.models.transaction import Transaction, TransactionType, TransactionStatus
from app.models.account import Account
from app import db
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

def create_transaction(user_id, account_id, amount, category, date, type, status, note=None):
    if not all([account_id, amount, category, date, type, status]):
        raise ValueError("All required fields must be provided")
    account = Account.query.get(account_id)
    if not account or account.user_id != user_id:
        raise ValueError("Account not found or unauthorized")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    transaction = Transaction(
        account_id=account_id,
        amount=amount,
        category=category,
        date=datetime.fromisoformat(date),
        type=type,
        status=status,
        note=note
    )
    # Update account balance
    if type == TransactionType.INCOME and status == TransactionStatus.COMPLETED:
        account.balance += amount
    elif type == TransactionType.EXPENSE and status == TransactionStatus.COMPLETED:
        account.balance -= amount
    db.session.add(transaction)
    db.session.commit()
    return transaction

def get_user_transactions(user_id, account_id=None):
    query = Transaction.query.join(Account).filter(Account.user_id == user_id)
    if account_id:
        query = query.filter(Transaction.account_id == account_id)
    return query.all()

def get_transaction(transaction_id, user_id):
    transaction = Transaction.query.join(Account).filter(
        Transaction.id == transaction_id,
        Account.user_id == user_id
    ).first()
    if not transaction:
        raise ValueError("Transaction not found or unauthorized")
    return transaction

def update_transaction(transaction_id, user_id, amount=None, category=None, date=None, type=None, status=None, note=None):
    transaction = Transaction.query.join(Account).filter(
        Transaction.id == transaction_id,
        Account.user_id == user_id
    ).first()
    if not transaction:
        raise ValueError("Transaction not found or unauthorized")
    account = transaction.account
    # Revert previous balance impact
    if transaction.status == TransactionStatus.COMPLETED:
        if transaction.type == TransactionType.INCOME:
            account.balance -= transaction.amount
        elif transaction.type == TransactionType.EXPENSE:
            account.balance += transaction.amount
    # Update fields
    if amount is not None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        transaction.amount = amount
    if category:
        transaction.category = category
    if date:
        transaction.date = datetime.fromisoformat(date)
    if type:
        transaction.type = type
    if status:
        transaction.status = status
    if note is not None:
        transaction.note = note
    # Apply new balance impact
    if transaction.status == TransactionStatus.COMPLETED:
        if transaction.type == TransactionType.INCOME:
            account.balance += transaction.amount
        elif transaction.type == TransactionType.EXPENSE:
            account.balance -= transaction.amount
    db.session.commit()
    return transaction

def delete_transaction(transaction_id, user_id):
    transaction = Transaction.query.join(Account).filter(
        Transaction.id == transaction_id,
        Account.user_id == user_id
    ).first()
    if not transaction:
        raise ValueError("Transaction not found or unauthorized")
    account = transaction.account
    if transaction.status == TransactionStatus.COMPLETED:
        if transaction.type == TransactionType.INCOME:
            account.balance -= transaction.amount
        elif transaction.type == TransactionType.EXPENSE:
            account.balance += transaction.amount
    db.session.delete(transaction)
    db.session.commit()