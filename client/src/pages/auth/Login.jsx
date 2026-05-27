import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import userApi from "../../api/userApi.js";
import LoadingSpinner from "../../loading-spinner/LoadingSpinner.jsx";

const Login = () => {
    const [passcode, setPasscode] = useState(new Array(6).fill(""));
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const inputRefs = useRef([]);
    const navigate = useNavigate();

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
            setPasscode(new Array(6).fill(""));
            inputRefs.current[0].focus();
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (element, index) => {
        const value = element.value;
        if (isNaN(value)) return false;

        const newPasscode = [...passcode];
        newPasscode[index] = value;
        setPasscode(newPasscode);

        if (value !== "" && index < 5) {
            inputRefs.current[index + 1].focus();
        }

        const combinedPasscode = newPasscode.join("");
        if (combinedPasscode.length === 6) {
            performLogin(combinedPasscode);
        }
    };

    const handleKeyDown = (e, index) => {
        if (e.key === "Backspace" && !passcode[index] && index > 0) {
            inputRefs.current[index - 1].focus();
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const fullPasscode = passcode.join("");
        if (fullPasscode.length === 6) {
            performLogin(fullPasscode);
        }
    };

    return (
        <div className="login-container">
            <form className="otp-Form" onSubmit={handleSubmit}>
                <span className="mainHeading">Nhập mật khẩu</span>
                <div className="inputContainer">
                    {passcode.map((data, index) => (
                        <input
                            key={index}
                            type="password"
                            className="otp-input"
                            maxLength="1"
                            value={data}
                            disabled={loading}
                            ref={(el) => (inputRefs.current[index] = el)}
                            onChange={(e) => handleChange(e.target, index)}
                            onKeyDown={(e) => handleKeyDown(e, index)}
                            required
                        />
                    ))}
                </div>

                {loading ? (
                    <LoadingSpinner/>
                ) : (
                    error && <p className="error-msg">{error}</p>
                )}

                <button
                    className="verifyButton"
                    type="submit"
                    disabled={loading || passcode.join("").length < 6}
                >
                    {loading ? "Đang xử lý..." : "Đăng nhập"}
                </button>
            </form>
        </div>
    );
};

export default Login;