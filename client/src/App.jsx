import {BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';
import Login from './pages/auth/Login';
import ProtectedRoute from './components/ProtectedRoute'; // Import gác cổng

const AdminDashboard = () => <div className="p-10">Chào Admin!</div>;
const OrderScreen = () => <div className="p-10">Chào Nhân Viên!</div>;

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login/>}/>

                <Route
                    path="/admin"
                    element={
                        <ProtectedRoute requiredRole={1}>
                            <AdminDashboard/>
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/order"
                    element={
                        <ProtectedRoute requiredRole={0}>
                            <OrderScreen/>
                        </ProtectedRoute>
                    }
                />

                <Route path="*" element={<Navigate to="/" replace/>}/>
            </Routes>
        </Router>
    );
}

export default App;