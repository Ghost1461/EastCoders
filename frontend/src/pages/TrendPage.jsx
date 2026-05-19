import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import './OverviewPage.css'; // Or a separate TrendPage.css if needed, using OverviewPage for layout basics

export const TrendPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    return (
        <div className="dashboard-container">
            <nav className="dashboard-nav">
                <div className="nav-left" style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <Link to="/dashboard" className="nav-brand">EastCoders</Link>
                </div>
                <div className="nav-links">
                    <Link to="/dashboard" className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}>Özet</Link>
                    <Link to="/products" className={`nav-link ${location.pathname === '/products' ? 'active' : ''}`}>Ürünlerim</Link>
                    <Link to="/integration" className={`nav-link ${location.pathname === '/integration' ? 'active' : ''}`}>Aktarma</Link>
                    <Link to="/haber" className={`nav-link ${location.pathname === '/haber' ? 'active' : ''}`}>Haber</Link>
                    <Link to="/reports" className={`nav-link ${location.pathname === '/reports' ? 'active' : ''}`}>Raporlar</Link>
                    <Link to="/trend" className={`nav-link ${location.pathname === '/trend' ? 'active' : ''}`}>Trend</Link>
                    <Link to="/profile" className={`nav-link ${location.pathname === '/profile' ? 'active' : ''}`}>Profil</Link>
                </div>
                <div className="nav-user" style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <div className="notification-bell" style={{ position: 'relative', cursor: 'pointer', display: 'flex', alignItems: 'center', transition: 'transform 0.2s' }} onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'} onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}>
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#475569" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-bell">
                            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                        </svg>
                        <span className="notification-dot" style={{ position: 'absolute', top: '0', right: '2px', width: '8px', height: '8px', backgroundColor: '#ef4444', borderRadius: '50%', border: '2px solid #fff' }}></span>
                    </div>
                    <span>Hoş geldin, {user?.full_name || 'Kullanıcı'}</span>
                    <button onClick={logout} className="logout-btn">Çıkış Yap</button>
                </div>
            </nav>

            <main className="dashboard-main">
                <div className="dashboard-header">
                    <h1>Trendler</h1>
                    <p>Piyasadaki güncel e-ticaret trendlerini ve arama verilerini buradan takip edebilirsiniz.</p>
                </div>
                <div className="overview-content" style={{ marginTop: '24px', backgroundColor: '#fff', padding: '40px', borderRadius: '16px', border: '1px solid rgba(0,0,0,0.05)', textAlign: 'center', color: '#64748b' }}>
                    <div style={{ fontSize: '48px', marginBottom: '16px' }}>📈</div>
                    <h2>Yakında Sizlerle!</h2>
                    <p>Trend analizi altyapımız hazırlanıyor. Çok yakında sektörünüze özel anlık trend verilerini burada görebileceksiniz.</p>
                </div>
            </main>
        </div>
    );
};
