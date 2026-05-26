import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from apps.extensions import db
from apps.models.product import Product

product_bp = Blueprint('product', __name__)

UPLOAD_FOLDER = os.path.join('apps', 'static', 'images', 'product_images')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



def handle_save_image(file):
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file_full_path = os.path.join(UPLOAD_FOLDER, filename)
        image_path_db = f"static/images/product_images/{filename}"

        if not os.path.exists(file_full_path):
            file.save(file_full_path)
        return image_path_db
    return None


def delete_image_if_orphan(image_path, exclude_id):
    if not image_path:
        return

    is_used = Product.query.filter(Product.image == image_path, Product.id != exclude_id).first()

    if not is_used:
        full_path = os.path.join('apps', image_path)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
            except Exception as e:
                print(f"Lỗi khi xóa file: {e}")


@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.form
    try:
        if not all([data.get('name'), data.get('category_id'), data.get('price')]):
            return jsonify({"message": "Vui lòng điền đủ Tên, Loại, Giá!"}), 400

        img_path = handle_save_image(request.files.get('image'))

        new_product = Product(
            name=data.get('name'),
            category_id=int(data.get('category_id')),
            price=float(data.get('price')),
            is_available=data.get('is_available', '1').lower() in ['1', 'true', 'on'],
            image=img_path
        )

        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Tạo sản phẩm thành công!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Lỗi hệ thống", "error": str(e)}), 500


@product_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.form
    try:
        new_file = request.files.get('image')
        if new_file:
            filename = secure_filename(new_file.filename)
            new_path_db = f"static/images/product_images/{filename}"

            if new_path_db != product.image:
                if not os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
                    delete_image_if_orphan(product.image, id)
                    new_file.save(os.path.join(UPLOAD_FOLDER, filename))

                product.image = new_path_db

        product.name = data.get('name', product.name)
        product.category_id = int(data.get('category_id', product.category_id))
        product.price = float(data.get('price', product.price))
        product.is_available = data.get('is_available', str(product.is_available)).lower() in ['1', 'true', 'on']

        db.session.commit()
        return jsonify({"message": "Cập nhật thành công!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Lỗi cập nhật", "error": str(e)}), 500


@product_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        delete_image_if_orphan(product.image, id)

        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Xóa sản phẩm thành công!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Lỗi khi xóa", "error": str(e)}), 500