import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import './NewsPage.css';

export const NewsPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    const [news, setNews] = useState([]);
    const [activeFilter, setActiveFilter] = useState("fashion");
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

                const headers = {
                    'Authorization': `Bearer ${token}`
                };

                // Veritabanından haberleri oku
                const [fashionRes, commerceRes] = await Promise.all([
                    fetch('http://localhost:8000/news/fashion', { headers }),
                    fetch('http://localhost:8000/news/commerce-finance', { headers })
                ]);

                if (!fashionRes.ok || !commerceRes.ok) {
                    throw new Error("Haberler yüklenirken bir sorun oluştu.");
                }

                const fashionData = await fashionRes.json();
                const commerceData = await commerceRes.json();

                // Arka arkaya birleştir
                setNews([...fashionData, ...commerceData]);
            } catch (err) {
                console.error("Haber okuma hatası:", err);
                setError(err.message || "Haberler yüklenemedi.");
            } finally {
                setLoading(false);
            }
        };

        fetchNews();
    }, []);

    const filteredNews = news.filter(item => {
        if (activeFilter === 'all') return true;
        if (activeFilter === 'fashion') return item.category === 'fashion';
        if (activeFilter === 'commerce') return item.category === 'commerce_finance';
        return true;
    });

    const formatDate = (dateString) => {
        if (!dateString) return "Tarih belirtilmedi";
        const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        return new Date(dateString).toLocaleDateString('tr-TR', options);
    };



    return (
        <div className="dashboard-container">
            <Navbar />

            <main className="dashboard-main news-main">
                <div className="news-inner-container" style={{ maxWidth: '900px', margin: '0 auto' }}>
                    <div className="news-header">
                        <div>
                            <h1>Sektörel Haberler</h1>
                            <p>E-ticaret ve piyasa ile ilgili en güncel gelişmeleri takip edin.</p>
                        </div>
                        <div className="news-filter-buttons">
                            <button
                                className={`filter-btn ${activeFilter === "fashion" ? "active" : ""}`}
                                onClick={() => setActiveFilter("fashion")}
                            >
                                Moda Haberleri
                            </button>

                            <button
                                className={`filter-btn ${activeFilter === "commerce" ? "active" : ""}`}
                                onClick={() => setActiveFilter("commerce")}
                            >
                                E-Ticaret Haberleri
                            </button>
                        </div>
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
                        ) : filteredNews.length === 0 ? (
                            <div className="empty-state">
                                <div style={{ fontSize: '48px', marginBottom: '16px' }}>📰</div>
                                <p>Şu an için gösterilecek bir haber bulunmuyor.</p>
                            </div>
                        ) : (
                            <div className="news-list">
                                {filteredNews.map((item) => (
                                    <article key={item.news_id} className="news-card">
                                        <div className="news-card-image-wrapper">
                                            <img src={item.image_url || 'https://via.placeholder.com/300x200'} alt={item.title} />
                                            {item.category && <div className="news-card-badge">{item.category}</div>}
                                        </div>
                                        <div className="news-card-info">
                                            <h3 className="news-card-title">
                                                <a href={item.url} target="_blank" rel="noopener noreferrer">
                                                    {item.title}
                                                </a>
                                            </h3>
                                            <div className="news-card-meta">
                                                {item.source && (
                                                    <span className="news-source">{item.source}</span>
                                                )}
                                                <span className="news-date">
                                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '4px' }}><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                                                    {formatDate(item.published_at)}
                                                </span>
                                            </div>
                                            {item.summary && (
                                                <p className="news-card-summary">{item.summary}</p>
                                            )}
                                            {item.related_tags && item.related_tags.length > 0 && (
                                                <div className="tags-list">
                                                    {item.related_tags.map((tag, index) => (
                                                        <span key={index} className="tag-item">#{tag}</span>
                                                    ))}
                                                </div>
                                            )}
                                            <div className="news-card-footer">
                                                {item.url && (
                                                    <a href={item.url} target="_blank" rel="noopener noreferrer" className="read-more-btn">
                                                        Habere Git
                                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"></path><path d="M12 5l7 7-7 7"></path></svg>
                                                    </a>
                                                )}
                                            </div>
                                        </div>
                                    </article>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
};
