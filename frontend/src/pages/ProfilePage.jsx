import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import './ProfilePage.css';

export const ProfilePage = () => {
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

            <main className="dashboard-main profile-main">
                <div className="profile-header">
                    <h1>Profilim</h1>
                    <p>Kişisel bilgilerinizi ve güvenlik ayarlarınızı buradan görüntüleyebilirsiniz.</p>
                </div>

                <div className="profile-content">
                    <div className="profile-card">
                        <h2>Kişisel Bilgiler</h2>
                        <div className="profile-form">
                            <div className="form-group">
                                <label>Ad Soyad</label>
                                <input type="text" value={user?.full_name || ''} readOnly className="read-only-input" />
                            </div>
                            
                            <div className="form-group">
                                <label>E-posta Adresi</label>
                                <input type="email" value={user?.email || ''} readOnly className="read-only-input" />
                            </div>

                            <div className="form-group">
                                <label>Telefon Numarası</label>
                                <input type="text" value={user?.phone_number || ''} readOnly className="read-only-input" />
                            </div>

                            <div className="form-group">
                                <label>Kullanıcı Rolü</label>
                                <input type="text" value={user?.role === 'seller' ? 'Satıcı' : (user?.role || '')} readOnly className="read-only-input role-input" />
                            </div>
                        </div>
                    </div>

                    <div className="profile-card">
                        <h2>Güvenlik ve API</h2>
                        <div className="profile-form">
                            <div className="form-group">
                                <label>Şifre</label>
                                <div className="password-group">
                                    <input type="password" value="********" readOnly className="read-only-input" />
                                    <button className="change-pwd-btn" disabled title="Şifre değiştirme henüz aktif değil">Değiştir</button>
                                </div>
                            </div>
                            
                            <div className="form-group api-section">
                                <label>Bağlı API Key'ler (Aktarma)</label>
                                <div className="api-list">
                                    <div className="api-item empty">
                                        <div className="api-info">
                                            <span className="api-icon">🔗</span>
                                            <span>API bağlantılarınızı <Link to="/integration" className="api-link">Aktarma</Link> sayfasından yönetebilirsiniz.</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};
