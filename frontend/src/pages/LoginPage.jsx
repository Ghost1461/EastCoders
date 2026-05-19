import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await login(email, password);
            const loggedInUser = JSON.parse(localStorage.getItem('user'));
            if (loggedInUser && loggedInUser.role === 'admin') {
                window.location.href = '/admin';
            } else {
                window.location.href = '/dashboard'; 
            }
        } catch (err) {
            setError(err.response?.data?.detail || "Giriş işlemi başarısız.");
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h2>Hoş Geldiniz</h2>
                    <p>Devam etmek için hesabınıza giriş yapın</p>
                </div>
                {error && <div className="auth-error">{error}</div>}
                <form className="auth-form" onSubmit={handleLogin}>
                    <div className="input-group">
                        <label>E-posta</label>
                        <input type="email" placeholder="ornek@email.com" value={email} onChange={e => setEmail(e.target.value)} required />
                    </div>
                    <div className="input-group">
                        <label>Şifre</label>
                        <input type="password" placeholder="••••••••" value={password} onChange={e => setPassword(e.target.value)} required />
                    </div>
                    <button className="auth-button" type="submit">Giriş Yap</button>
                </form>
                <div className="auth-footer">
                    <p>Hesabınız yok mu? <Link to="/signup">Kayıt Ol</Link></p>
                </div>
            </div>
        </div>
    );
};