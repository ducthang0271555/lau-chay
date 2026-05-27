import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import userApi from "../../api/userApi.js";
import LoadingSpinner from "../../loading-spinner/LoadingSpinner.jsx";

const Login = () => {
    const [passcode, setPasscode] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const hiddenInputRef = useRef(null);
    const navigate = useNavigate();

    const handleBoxClick = () => {
        hiddenInputRef.current.focus();
    };

    useEffect(() => {
        const userString = localStorage.getItem('user');
        if (userString) {
            const user = JSON.parse(userString);
            if (user.role === 1) navigate('/admin');
            else navigate('/order');
        }
    }, [navigate]);

    const performLogin = async (finalPasscode) => {
        setLoading(true);
        setError("");
        try {
            const response = await userApi.login(finalPasscode);
            if (response.status === "success") {
                const { user } = response;
                localStorage.setItem('user', JSON.stringify(user));
                if (user.role === 1) navigate('/admin');
                else navigate('/order');
            }
        } catch (err) {
            const msg = err.response?.data?.message || "Mật khẩu không đúng!";
            setError(msg);
            setPasscode("");
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const value = e.target.value;
        if (/^\d*$/.test(value) && value.length <= 6) {
            setPasscode(value);
            if (value.length === 6) {
                performLogin(value);
            }
        }
    };

    return (
        <div className="login-container">
            <form className="otp-Form" onClick={handleBoxClick}>
                <span className="mainHeading">Nhập mật khẩu</span>

                <input
                    ref={hiddenInputRef}
                    type="text"
                    inputMode="numeric"
                    pattern="[0-9]*"
                    value={passcode}
                    onChange={handleChange}
                    className="hidden-input"
                    autoFocus
                />

                <div className="inputContainer">
                    {[...Array(6)].map((_, index) => (
                        <div
                            key={index}
                            className={`otp-box ${passcode.length === index ? 'active' : ''}`}
                        >
                            {passcode[index] ? '●' : ''}
                        </div>
                    ))}
                </div>

                {loading ? (
                    <LoadingSpinner />
                ) : (
                    error && <p className="error-msg">{error}</p>
                )}

                <button
                    className="verifyButton"
                    type="button"
                    disabled={loading || passcode.length < 6}
                    onClick={() => performLogin(passcode)}
                >
                    {loading ? "Đang xử lý..." : "Đăng nhập"}
                </button>
            </form>
        </div>
    );
};

export default Login;