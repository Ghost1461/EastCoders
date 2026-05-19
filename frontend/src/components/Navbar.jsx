import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import stockRadarLogo from '../assets/stockradar.jpeg';
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
            <div className="nav-left">
                <Link to="/dashboard" className="nav-brand">
                    <img src={stockRadarLogo} alt="StockRadar" style={{ height: '56px', objectFit: 'contain' }} />
                </Link>
            </div>
            <div className="nav-links">
                <Link to="/dashboard" className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}>Özet</Link>
                <Link to="/products" className={`nav-link ${location.pathname === '/products' ? 'active' : ''}`}>Ürünlerim</Link>
                <Link to="/orders" className={`nav-link ${location.pathname === '/orders' ? 'active' : ''}`}>Siparişlerim</Link>
                <Link to="/integration" className={`nav-link ${location.pathname === '/integration' ? 'active' : ''}`}>Aktarma</Link>
                <Link to="/reports" className={`nav-link ${location.pathname === '/reports' ? 'active' : ''}`}>Raporlar</Link>
                <Link to="/haber" className={`nav-link ${location.pathname === '/haber' ? 'active' : ''}`}>Haberler</Link>
                <Link to="/trend" className={`nav-link ${location.pathname === '/trend' ? 'active' : ''}`}>Trendler</Link>
            </div>
            <div className="nav-user">
                <div
                    className="notification-bell"
                    onClick={handleBellClick}
                >
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#475569" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-bell">
                        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                        <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                    </svg>
                    {unreadCount > 0 && (
                        <span className="notification-dot"></span>
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

                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', justifyContent: 'center' }}>
                    <span style={{ fontSize: '13px', color: '#94a3b8', fontWeight: '500', lineHeight: '1.2' }}>Hoş geldin,</span>
                    <Link to="/profile" style={{ textDecoration: 'none' }}>
                        <span style={{ color: '#0f172a', transition: 'color 0.2s', cursor: 'pointer' }} onMouseEnter={e => e.target.style.color = '#2563eb'} onMouseLeave={e => e.target.style.color = '#0f172a'}>
                            {user?.full_name || 'Kullanıcı'}
                        </span>
                    </Link>
                </div>
                <button onClick={logout} className="logout-btn">Çıkış Yap</button>
            </div>
        </nav>
    );
};
