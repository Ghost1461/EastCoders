import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './AdminNavbar.css';

export const AdminNavbar = () => {
    const { logout, user } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav className="admin-navbar">
            <div className="admin-nav-brand">
                <div className="admin-logo-icon">E</div>
                <span className="admin-logo-text">EastCoders <span className="admin-badge">Admin</span></span>
            </div>
            
            <div className="admin-nav-actions">
                <span className="admin-user-email">{user?.email}</span>
                <button onClick={handleLogout} className="admin-logout-btn">
                    Çıkış Yap
                </button>
            </div>
        </nav>
    );
};
