import { createContext, useState, useContext, useEffect } from 'react';
import api from '../api/client';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Uygulama ilk açıldığında token'ı doğrula
    useEffect(() => {
        const verifyAuth = async () => {
            const token = localStorage.getItem('token');
            const savedUser = localStorage.getItem('user');
            
            if (token && savedUser) {
                try {
                    const response = await api.get('/authentication/me');
                    setUser(response.data);
                } catch (error) {
                    localStorage.removeItem('token');
                    localStorage.removeItem('user');
                    setUser(null);
                }
            } else {
                setUser(null);
            }
            setLoading(false);
        };
        verifyAuth();
    }, []);

    const triggerBackgroundFetches = () => {
        Promise.all([
            api.post('/news/fashion/fetch'),
            api.post('/news/commerce-finance/fetch'),
            api.post('/trends/generate/market')
        ]).catch(err => console.error("Arkaplan veri getirme hatası:", err));
    };

    const login = async (email, password) => {
        const response = await api.post('/authentication/login-json', { email, password });
        const { access_token, user: userData } = response.data;
        
        localStorage.setItem('token', access_token);
        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
        triggerBackgroundFetches();
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
    };

    const signup = async (formData) => {
        try {
            const response = await api.post('/authentication/signup', formData);
            const { access_token, user: userData } = response.data;
            
            localStorage.setItem('token', access_token);
            localStorage.setItem('user', JSON.stringify(userData));
            setUser(userData);
            triggerBackgroundFetches();
            return true;
        } catch (error) {
            throw error;
        }
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, signup, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);