from flask import Blueprint, request, jsonify
from apps.extensions import db
from apps.models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['POST'])
def login():
    data = request.get_json()
    passcode = data.get('passcode')

    if not passcode:
        return jsonify({"message": "Vui lòng nhập mã passcode"}), 400

    user = User.query.filter_by(passcode=passcode).first()

    if not user:
        return jsonify({"status": "fail", "message": "Mã passcode không đúng!"}), 401

    if not user.is_active:
        return jsonify({
            "status": "fail",
            "message": "Tài khoản của bạn đã bị khóa hoặc ngừng hoạt động!"
        }), 403

    return jsonify({
        "status": "success",
        "user": {
            "id": user.id,
            "name": user.name,
            "role": user.role,  # 0: Staff, 1: Admin
            "is_active": user.is_active
        }
    }), 200

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "name": u.name,
        "passcode": u.passcode,
        "role": u.role,
        "is_active": u.is_active
    } for u in users]), 200


@user_bp.route('/register', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        name=data.get('name'),
        passcode=data.get('passcode'),
        role=data.get('role', 0)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Thêm nhân viên thành công"}), 201

@user_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Đã xóa nhân viên"}), 200