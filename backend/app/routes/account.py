from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.account import create_account, get_user_accounts, get_account, update_account, delete_account
from app.models.account import AccountType
from http import HTTPStatus

account_bp = Blueprint('account', __name__, url_prefix='/accounts')

@account_bp.route('', methods=['POST'])
@jwt_required()
def create_account_route():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        account = create_account(
            user_id=user_id,
            name=data['name'],
            account_type=AccountType[data['account_type'].upper()]
        )
        return jsonify(account.to_dict()), HTTPStatus.CREATED
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@account_bp.route('', methods=['GET'])
@jwt_required()
def get_accounts_route():
    try:
        user_id = get_jwt_identity()
        accounts = get_user_accounts(user_id)
        return jsonify([account.to_dict() for account in accounts]), HTTPStatus.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@account_bp.route('/<account_id>', methods=['GET'])
@jwt_required()
def get_account_route(account_id):
    try:
        user_id = get_jwt_identity()
        account = get_account(account_id, user_id)
        return jsonify(account.to_dict()), HTTPStatus.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@account_bp.route('/<account_id>', methods=['PUT'])
@jwt_required()
def update_account_route(account_id):
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        account = update_account(
            account_id=account_id,
            user_id=user_id,
            name=data.get('name'),
            account_type=AccountType[data['account_type'].upper()] if data.get('account_type') else None
        )
        return jsonify(account.to_dict()), HTTPStatus.OK
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@account_bp.route('/<account_id>', methods=['DELETE'])
@jwt_required()
def delete_account_route(account_id):
    try:
        user_id = get_jwt_identity()
        delete_account(account_id, user_id)
        return jsonify({'message': 'Account deleted'}), HTTPStatus.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST