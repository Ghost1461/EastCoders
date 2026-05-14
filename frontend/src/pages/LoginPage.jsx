import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            await login(email, password);
            window.location.href = '/dashboard'; // Başarılıysa yönlendir
        } catch (err) {
            alert("Hatalı giriş: " + err.response?.data?.detail);
        }
    };

    return (
        <form onSubmit={handleLogin}>
            <input type="email" placeholder="E-posta" onChange={e => setEmail(e.target.value)} />
            <input type="password" placeholder="Şifre" onChange={e => setPassword(e.target.value)} />
            <button type="submit">Giriş Yap</button>
        </form>
    );
};