import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import './IntegrationPage.css';

export const IntegrationPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();
    
    const [selectedPlatform, setSelectedPlatform] = useState(null);
    const [apiKey, setApiKey] = useState('');

    const platforms = [
        { 
            id: 'trendyol', 
            name: 'Trendyol', 
            color: '#f27a1a', 
            logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Trendyol_logo.svg/1024px-Trendyol_logo.svg.png' 
        },
        { 
            id: 'hepsiburada', 
            name: 'Hepsiburada', 
            color: '#ff6000', 
            logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Hepsiburada_logo.svg/1024px-Hepsiburada_logo.svg.png' 
        },
        { 
            id: 'amazon', 
            name: 'Amazon', 
            color: '#232f3e', 
            logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1024px-Amazon_logo.svg.png' 
        }
    ];

    const handlePlatformClick = (platformId) => {
        if (selectedPlatform === platformId) {
            setSelectedPlatform(null);
        } else {
            setSelectedPlatform(platformId);
            setApiKey('');
        }
    };

    const handleConnect = (e) => {
        e.preventDefault();
        alert(`${platforms.find(p => p.id === selectedPlatform).name} için API Key başarıyla aktarıldı!`);
        setApiKey('');
        setSelectedPlatform(null);
    };

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

            <main className="dashboard-main integration-main">
                <div className="integration-header">
                    <h1>Mağaza Entegrasyonları</h1>
                    <p>Satış yaptığınız platformların API anahtarlarını girerek mağazalarınızı birbirine bağlayın.</p>
                </div>

                <div className="platforms-container">
                    <div className="platforms-grid">
                        {platforms.map(platform => (
                            <div key={platform.id} className="platform-card-wrapper">
                                <button 
                                    className={`platform-btn ${selectedPlatform === platform.id ? 'active' : ''}`}
                                    style={{ '--brand-color': platform.color }}
                                    onClick={() => handlePlatformClick(platform.id)}
                                >
                                    <img src={platform.logo} alt={platform.name} className="platform-logo" />
                                </button>
                                
                                {selectedPlatform === platform.id && (
                                    <form className="api-key-form slide-down" onSubmit={handleConnect}>
                                        <div className="input-group">
                                            <input 
                                                type="text" 
                                                placeholder={`${platform.name} API Key...`}
                                                value={apiKey}
                                                onChange={(e) => setApiKey(e.target.value)}
                                                required 
                                            />
                                            <button type="submit" className="connect-btn">Aktar</button>
                                        </div>
                                    </form>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </main>
        </div>
    );
};
