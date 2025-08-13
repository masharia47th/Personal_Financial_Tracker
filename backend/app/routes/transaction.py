from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.transaction import create_transaction, get_user_transactions, get_transaction, update_transaction, delete_transaction
from app.models.transaction import TransactionType, TransactionStatus
from http import HTTPStatus

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transactions')

@transaction_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction_route():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        transaction = create_transaction(
            user_id=user_id,
            account_id=data['account_id'],
            amount=data['amount'],
            category=data['category'],
            date=data['date'],
            type=TransactionType[data['type'].upper()],
            status=TransactionStatus[data['status'].upper()],
            note=data.get('note')
        )
        return jsonify(transaction.to_dict()), HTTPStatus.CREATED
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@transaction_bp.route('', methods=['GET'])
@jwt_required()
def get_transactions_route():
    try:
        user_id = get_jwt_identity()
        account_id = request.args.get('account_id')
        transactions = get_user_transactions(user_id, account_id)
        return jsonify([t.to_dict() for t in transactions]), HTTPStatus.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@transaction_bp.route('/<transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction_route(transaction_id):
    try:
        user_id = get_jwt_identity()
        transaction = get_transaction(transaction_id, user_id)
        return jsonify(transaction.to_dict()), HTTPStatus.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@transaction_bp.route('/<transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction_route(transaction_id):
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        transaction = update_transaction(
            transaction_id=transaction_id,
            user_id=user_id,
            amount=data.get('amount'),
            category=data.get('category'),
            date=data.get('date'),
            type=TransactionType[data['type'].upper()] if data.get('type') else None,
            status=TransactionStatus[data['status'].upper()] if data.get('status') else None,
            note=data.get('note')
        )
        return jsonify(transaction.to_dict()), HTTPStatus.OK
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@transaction_bp.route('/<transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction_route(transaction_id):
    try:
        user_id = get_jwt_identity()
        delete_transaction(transaction_id, user_id)
        return jsonify({'message': 'Transaction deleted'}), HTTPStatus.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST