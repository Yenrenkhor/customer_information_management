from flask import Blueprint, request, jsonify, abort
from .customer_model import customer_db, Customer
from flask_jwt_extended import jwt_required

customer_blueprint = Blueprint('customer', __name__)


@customer_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_customer():
    customer_json = request.json
    required_fields = ['first_name', 'last_name', 'address', 'phone', 'email']

    for field in required_fields:
        if field not in customer_json:
            return jsonify({"error": "Bad request", "message": f"{field} is missing"}), 400
    try:
        customer = Customer(
            first_name=customer_json['first_name'],
            last_name=customer_json['last_name'],
            address=customer_json['address'],
            phone=customer_json['phone'],
            email=customer_json['email']
        )
        customer_db.session.add(customer)
        customer_db.session.commit()
        return jsonify(customer.to_dict(), 200)

    except ValueError as e:
        raise e


@customer_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_all_customers():
    customers = [customer.to_dict() for customer in Customer.query.all()]
    return jsonify(customers)


@customer_blueprint.route('/<customer_id>', methods=['GET'])
@jwt_required()
def get_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        abort(404)
    return jsonify(customer.to_dict())


@customer_blueprint.route('/update/<customer_id>', methods=['PUT'])
@jwt_required()
def update_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        abort(404)
    updated_fields = request.json
    for key, value in updated_fields.items():
        setattr(customer, key, value)

    customer_db.session.commit()
    return jsonify(customer.to_dict())


@customer_blueprint.route('/delete/<customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        abort(404)
    customer_db.session.delete(customer)
    customer_db.session.commit()
    return jsonify({"message": "Customer deleted successfully"})


# ========= Error Handler =========

@customer_blueprint.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad request", "message": str(error)}), 400


@customer_blueprint.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found", "message": str(error)}), 404


@customer_blueprint.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error", "message": str(error)}), 500
