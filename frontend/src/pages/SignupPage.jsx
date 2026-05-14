import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const SignupPage = () => {
    const { signup } = useAuth();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        full_name: '',
        email: '',
        phone_number: '',
        password: '',
        password_confirm: ''
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        if (formData.password !== formData.password_confirm) {
            alert("Şifreler eşleşmiyor!");
            return;
        }
        try {
            await signup(formData);
            navigate('/dashboard'); 
        } catch (err) {
            alert("Kayıt hatası: " + err.response?.data?.detail);
        }
    };

    return (
        <div className="auth-card">
            <h2>Hemen Kaydol</h2>
            <form onSubmit={handleSignup}>
                <input name="full_name" placeholder="Ad Soyad" onChange={handleChange} required />
                <input name="email" type="email" placeholder="E-posta" onChange={handleChange} required />
                <input name="phone_number" placeholder="Telefon (örn: 5554443322)" onChange={handleChange} required />
                <input name="password" type="password" placeholder="Şifre" onChange={handleChange} required />
                <input name="password_confirm" type="password" placeholder="Şifre Onay" onChange={handleChange} required />
                <button type="submit">Kayıt Ol</button>
            </form>
        </div>
    );
};