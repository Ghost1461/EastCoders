import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import './Navbar.css';

export const Navbar = () => {
    const { user, logout } = useAuth();
    const location = useLocation();
    
    const [unreadCount, setUnreadCount] = useState(0);
    const [showNotifications, setShowNotifications] = useState(false);
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchUnreadCount = async () => {
            try {
                const res = await api.get('/notifications/unread-count');
                setUnreadCount(res.data.unread_count);
            } catch (err) {
                console.error("Unread count fetch error:", err);
            }
        };
        fetchUnreadCount();
        
        // Polling every 60s
        const interval = setInterval(fetchUnreadCount, 60000);
        return () => clearInterval(interval);
    }, []);

    const handleBellClick = async () => {
        setShowNotifications(!showNotifications);
        if (!showNotifications) {
            setLoading(true);
            try {
                const res = await api.get('/notifications/');
                setNotifications(res.data);
            } catch (err) {
                console.error("Notifications fetch error:", err);
            } finally {
                setLoading(false);
            }
        }
    };

    const markAsRead = async (id, url) => {
        try {
            await api.post(`/notifications/${id}/read`);
            setUnreadCount(prev => Math.max(0, prev - 1));
            setNotifications(prev => prev.map(n => n.notification_id === id ? { ...n, is_read: true } : n));
            
            if (url) {
                window.open(url, '_blank', 'noopener,noreferrer');
            }
        } catch (err) {
            console.error("Mark as read error:", err);
        }
    };

    return (
        <nav className="dashboard-nav">
            <div className="nav-left" style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                <Link to="/dashboard" className="nav-brand">EastCoders</Link>
            </div>
            <div className="nav-links">
                <Link to="/dashboard" className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}>Özet</Link>
                <Link to="/products" className={`nav-link ${location.pathname === '/products' ? 'active' : ''}`}>Ürünlerim</Link>
                <Link to="/integration" className={`nav-link ${location.pathname === '/integration' ? 'active' : ''}`}>Aktarma</Link>
                <Link to="/haber" className={`nav-link ${location.pathname === '/haber' ? 'active' : ''}`}>Haber</Link>
                <Link to="/trend" className={`nav-link ${location.pathname === '/trend' ? 'active' : ''}`}>Trend</Link>
                <Link to="/profile" className={`nav-link ${location.pathname === '/profile' ? 'active' : ''}`}>Profil</Link>
            </div>
            <div className="nav-user" style={{ display: 'flex', alignItems: 'center', gap: '20px', position: 'relative' }}>
                <div 
                    className="notification-bell" 
                    onClick={handleBellClick}
                    style={{ position: 'relative', cursor: 'pointer', display: 'flex', alignItems: 'center', transition: 'transform 0.2s' }} 
                    onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'} 
                    onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
                >
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#475569" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-bell">
                        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                        <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                    </svg>
                    {unreadCount > 0 && (
                        <span className="notification-dot" style={{ position: 'absolute', top: '0', right: '2px', width: '8px', height: '8px', backgroundColor: '#ef4444', borderRadius: '50%', border: '2px solid #fff' }}></span>
                    )}
                </div>
                
                {showNotifications && (
                    <div className="notifications-dropdown">
                        <div className="notifications-header">
                            <h3>Bildirimler</h3>
                            {unreadCount > 0 && <span className="unread-badge">{unreadCount} Yeni</span>}
                        </div>
                        <div className="notifications-body">
                            {loading ? (
                                <div className="notifications-loading">Yükleniyor...</div>
                            ) : notifications.length === 0 ? (
                                <div className="notifications-empty">Bildiriminiz yok.</div>
                            ) : (
                                notifications.map(notif => (
                                    <div 
                                        key={notif.notification_id} 
                                        className={`notification-item ${!notif.is_read ? 'unread' : ''}`}
                                        onClick={() => markAsRead(notif.notification_id, notif.url)}
                                    >
                                        <div className="notification-content">
                                            {notif.category && <span className="notification-category">{notif.category}</span>}
                                            <p className="notification-title">{notif.title}</p>
                                            <span className="notification-time">{new Date(notif.created_at).toLocaleDateString()}</span>
                                        </div>
                                        {!notif.is_read && <div className="unread-indicator"></div>}
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                )}

                <span>Hoş geldin, {user?.full_name || 'Kullanıcı'}</span>
                <button onClick={logout} className="logout-btn">Çıkış Yap</button>
            </div>
        </nav>
    );
};
