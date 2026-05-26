from flask import Blueprint, request, jsonify
from apps.extensions import db
from apps.models.category import Category

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"message": "Vui lòng nhập tên loại!"}), 400

    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Tạo loại thành công!"}), 201

@category_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({"message": "Không tồn tại loại này!"}), 404

    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"message": "Vui lòng nhập tên loại!"}), 400

    category.name = name
    db.session.commit()

    return jsonify({"message": "Thay đổi tên thành công!"}), 200

@category_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({"message": "Không tồn tại loại này!"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Xoá loại thành công!"}), 200

@category_bp.route('/', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()
    category_list = [{"id": c.id, "name": c.name} for c in categories]

    return jsonify(category_list), 200