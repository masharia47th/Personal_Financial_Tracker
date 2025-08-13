from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.budget import create_budget, get_user_budgets, get_budget, update_budget, delete_budget
from app.models.budget import BudgetPeriod
from http import HTTPStatus

budget_bp = Blueprint('budget', __name__, url_prefix='/budgets')

@budget_bp.route('', methods=['POST'])
@jwt_required()
def create_budget_route():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        budget = create_budget(
            user_id=user_id,
            category=data['category'],
            limit=data['limit'],
            period=BudgetPeriod[data['period'].replace(' ', '_').upper()]
        )
        return jsonify(budget.to_dict()), HTTPStatus.CREATED
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@budget_bp.route('', methods=['GET'])
@jwt_required()
def get_budgets_route():
    try:
        user_id = get_jwt_identity()
        budgets = get_user_budgets(user_id)
        return jsonify([b.to_dict() for b in budgets]), HTTPStatus.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@budget_bp.route('/<budget_id>', methods=['GET'])
@jwt_required()
def get_budget_route(budget_id):
    try:
        user_id = get_jwt_identity()
        budget = get_budget(budget_id, user_id)
        return jsonify(budget.to_dict()), HTTPStatus.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@budget_bp.route('/<budget_id>', methods=['PUT'])
@jwt_required()
def update_budget_route(budget_id):
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        budget = update_budget(
            budget_id=budget_id,
            user_id=user_id,
            category=data.get('category'),
            limit=data.get('limit'),
            period=BudgetPeriod[data['period'].replace(' ', '_').upper()] if data.get('period') else None
        )
        return jsonify(budget.to_dict()), HTTPStatus.OK
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@budget_bp.route('/<budget_id>', methods=['DELETE'])
@jwt_required()
def delete_budget_route(budget_id):
    try:
        user_id = get_jwt_identity()
        delete_budget(budget_id, user_id)
        return jsonify({'message': 'Budget deleted'}), HTTPStatus.OK
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST