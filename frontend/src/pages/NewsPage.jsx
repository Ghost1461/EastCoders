import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import './NewsPage.css';

export const NewsPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();
    
    const [news, setNews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchNews = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    setError("Oturum süresi dolmuş. Lütfen tekrar giriş yapın.");
                    setLoading(false);
                    return;
                }

                const response = await fetch('http://localhost:8000/news/display_market_news', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error("Haberler yüklenirken bir sorun oluştu.");
                }

                const data = await response.json();
                setNews(data);
            } catch (err) {
                console.error("Haber fetch hatası:", err);
                setError(err.message || "Haberler yüklenemedi.");
            } finally {
                setLoading(false);
            }
        };

        fetchNews();
    }, []);

    const formatDate = (dateString) => {
        if (!dateString) return "Tarih belirtilmedi";
        const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        return new Date(dateString).toLocaleDateString('tr-TR', options);
    };

    const getImpactBadgeClass = (impact) => {
        switch(impact?.toLowerCase()) {
            case 'high': return 'impact-high';
            case 'low': return 'impact-low';
            default: return 'impact-medium';
        }
    };

    const getImpactLabel = (impact) => {
        switch(impact?.toLowerCase()) {
            case 'high': return 'Yüksek Etki';
            case 'low': return 'Düşük Etki';
            default: return 'Orta Etki';
        }
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

            <main className="dashboard-main news-main">
                <div className="news-header">
                    <h1>Sektörel Haberler</h1>
                    <p>E-ticaret ve piyasa ile ilgili en güncel gelişmeleri takip edin.</p>
                </div>

                <div className="news-content">
                    {loading ? (
                        <div className="loading-state">
                            <div className="loading-spinner"></div>
                            <p>Haberler yükleniyor...</p>
                        </div>
                    ) : error ? (
                        <div className="error-state">
                            <div style={{ fontSize: '32px', marginBottom: '16px' }}>⚠️</div>
                            <p>{error}</p>
                            <button onClick={() => window.location.reload()} style={{ marginTop: '16px', padding: '8px 16px', background: '#ef4444', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer' }}>Tekrar Dene</button>
                        </div>
                    ) : news.length === 0 ? (
                        <div className="empty-state">
                            <div style={{ fontSize: '48px', marginBottom: '16px' }}>📰</div>
                            <p>Şu an için gösterilecek bir haber bulunmuyor.</p>
                        </div>
                    ) : (
                        <div className="news-list">
                            {news.map((item) => (
                                <article key={item.news_id} className="news-card">
                                    <div className="news-card-header">
                                        <h2 className="news-title">
                                            <a href={item.url} target="_blank" rel="noopener noreferrer">
                                                {item.title}
                                            </a>
                                        </h2>
                                    </div>
                                    
                                    <div className="news-meta">
                                        {item.source && (
                                            <span className="news-source">{item.source}</span>
                                        )}
                                        <div className="news-meta-item">
                                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                                            {formatDate(item.published_at)}
                                        </div>
                                        {item.category && (
                                            <div className="news-meta-item">
                                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>
                                                {item.category}
                                            </div>
                                        )}
                                    </div>

                                    {item.summary && (
                                        <p className="news-summary">{item.summary}</p>
                                    )}

                                    {item.related_tags && item.related_tags.length > 0 && (
                                        <div className="tags-list">
                                            {item.related_tags.map((tag, index) => (
                                                <span key={index} className="tag-item">#{tag}</span>
                                            ))}
                                        </div>
                                    )}

                                    <div className="news-footer">
                                        <span className={`impact-badge ${getImpactBadgeClass(item.impact_level)}`}>
                                            {getImpactLabel(item.impact_level)}
                                        </span>
                                        
                                        {item.url && (
                                            <a href={item.url} target="_blank" rel="noopener noreferrer" className="read-more-btn">
                                                Habere Git 
                                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"></path><path d="M12 5l7 7-7 7"></path></svg>
                                            </a>
                                        )}
                                    </div>
                                </article>
                            ))}
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
};
