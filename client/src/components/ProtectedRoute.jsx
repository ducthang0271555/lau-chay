import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children, requiredRole }) => {
    // 1. Lấy dữ liệu user từ localStorage
    const userString = localStorage.getItem('user');
    const user = userString ? JSON.parse(userString) : null;

    // 2. Nếu chưa đăng nhập (không có user) -> Đuổi về trang login (/)
    if (!user) {
        return <Navigate to="/" replace />;
    }

    // 3. Nếu có yêu cầu về Role (Admin/Staff) mà user không khớp -> Đuổi về login
    if (requiredRole !== undefined && user.role !== requiredRole) {
        return <Navigate to="/" replace />;
    }

    // 4. Nếu thỏa mãn mọi điều kiện -> Cho phép vào trang
    return children;
};

export default ProtectedRoute;