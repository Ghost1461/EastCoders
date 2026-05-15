import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export const SignupPage = () => {
    const { signup } = useAuth();
    const navigate = useNavigate();
    const [error, setError] = useState('');
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
        setError('');
        if (formData.password !== formData.password_confirm) {
            setError("Şifreler eşleşmiyor!");
            return;
        }
        try {
            await signup(formData);
            navigate('/dashboard'); 
        } catch (err) {
            setError(err.response?.data?.detail || "Kayıt işlemi başarısız.");
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h2>Hesap Oluştur</h2>
                    <p>Aramıza katılmak için formu doldurun</p>
                </div>
                {error && <div className="auth-error">{error}</div>}
                <form className="auth-form" onSubmit={handleSignup}>
                    <div className="input-group">
                        <label>Ad Soyad</label>
                        <input name="full_name" placeholder="John Doe" onChange={handleChange} required />
                    </div>
                    <div className="input-group">
                        <label>E-posta</label>
                        <input name="email" type="email" placeholder="ornek@email.com" onChange={handleChange} required />
                    </div>
                    <div className="input-group">
                        <label>Telefon</label>
                        <input name="phone_number" placeholder="555 444 33 22" onChange={handleChange} required />
                    </div>
                    <div className="input-row">
                        <div className="input-group">
                            <label>Şifre</label>
                            <input name="password" type="password" placeholder="••••••••" onChange={handleChange} required />
                        </div>
                        <div className="input-group">
                            <label>Şifre Onayı</label>
                            <input name="password_confirm" type="password" placeholder="••••••••" onChange={handleChange} required />
                        </div>
                    </div>
                    <button className="auth-button" type="submit">Kayıt Ol</button>
                </form>
                <div className="auth-footer">
                    <p>Zaten bir hesabınız var mı? <Link to="/login">Giriş Yap</Link></p>
                </div>
            </div>
        </div>
    );
};