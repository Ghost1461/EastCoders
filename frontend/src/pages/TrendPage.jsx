import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import api from '../api/client';
import './TrendPage.css';

export const TrendPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    const [trends, setTrends] = useState([]);
    const [isPersonalized, setIsPersonalized] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [aiSummary, setAiSummary] = useState(null);
    const [aiLoading, setAiLoading] = useState(false);
    const [showAiModal, setShowAiModal] = useState(false);

    const fetchAiSummary = async () => {
        setAiLoading(true);
        setShowAiModal(true);
        try {
            const response = await api.post('/trends/ai-summary');
            setAiSummary(response.data);
        } catch (err) {
            console.error("AI Summary hatası:", err);
            setAiSummary({ error: "Tavsiyeler alınırken bir hata oluştu." });
        } finally {
            setAiLoading(false);
        }
    };

    useEffect(() => {
        const fetchTrends = async () => {
            setLoading(true);
            setError(null);
            try {
                const endpoint = isPersonalized ? '/trends/personalized' : '/trends/raw';
                const response = await api.get(endpoint);
                setTrends(response.data || []);
            } catch (err) {
                console.error("Trend getirme hatası:", err);
                setError("Trendler yüklenirken bir hata oluştu.");
            } finally {
                setLoading(false);
            }
        };

        fetchTrends();
    }, [isPersonalized]);

    const renderCards = () => {
        if (loading) {
            return (
                <div className="loading-state" style={{ gridColumn: '1 / -1' }}>
                    <div className="loading-spinner"></div>
                    <p>Yükleniyor...</p>
                </div>
            );
        }

        if (error) {
            return (
                <div className="error-state" style={{ gridColumn: '1 / -1', color: '#e11d48' }}>
                    <p>⚠️ {error}</p>
                    <button onClick={() => window.location.reload()} style={{ marginTop: '16px', padding: '8px 16px', background: '#e11d48', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer' }}>Tekrar Dene</button>
                </div>
            );
        }

        if (!trends || trends.length === 0) {
            return (
                <div className="loading-state" style={{ gridColumn: '1 / -1' }}>
                    <p>Şu an için gösterilecek trend bulunamadı.</p>
                </div>
            );
        }

        if (isPersonalized) {
            return trends.map((item, index) => {
                const trend = item.trend || {};
                const firstMatch = item.matched_products && item.matched_products.length > 0 ? item.matched_products[0] : {};

                const brand = firstMatch.brand || trend.category || 'Önerilen Marka';
                const price = firstMatch.price ? `${firstMatch.price} TL` : 'Fiyat bilgisi yok';
                const reviewCount = firstMatch.review_count || Math.floor(Math.random() * 5000);
                const rating = firstMatch.rating || 4.5;

                return (
                    <div key={index} className="trendyol-card">
                        <div className="card-image-wrapper">
                            <img src={trend.image_url || 'https://via.placeholder.com/200x300'} alt={trend.trend_name} />
                            <div className="card-badge" style={{ background: '#0ea5e9' }}>Önerilen</div>
                        </div>
                        <div className="card-info">
                            <h3 className="card-title">
                                <strong>{brand}</strong> {trend.trend_name}
                            </h3>
                            <div className="card-rating">
                                <span style={{ fontSize: '12px', fontWeight: '700', color: '#475569' }}>{rating}</span>
                                <span className="stars">★★★★★</span>
                                <span className="review-count">({reviewCount})</span>
                            </div>
                            <div className="card-price">
                                {price}
                            </div>
                        </div>
                    </div>
                );
            });
        } else {
            return trends.map((item, index) => {
                const extra = item.extra_data || {};
                const brand = extra.brand || item.platform || 'Trend';
                const price = extra.price ? `${extra.price} TL` : (extra.discountedPrice ? `${extra.discountedPrice} TL` : '199,99 TL');
                const reviewCount = extra.reviewCount || extra.review_count || Math.floor(Math.random() * 5000);
                const rating = extra.rating || 4.5;

                return (
                    <div key={index} className="trendyol-card">
                        <div className="card-image-wrapper">
                            <img src={item.image_url || 'https://via.placeholder.com/200x300'} alt={item.trend_name} />
                            <div className="card-badge">Popüler</div>
                        </div>
                        <div className="card-info">
                            <h3 className="card-title">
                                <strong>{brand}</strong> {item.trend_name}
                            </h3>
                            <div className="card-rating">
                                <span style={{ fontSize: '12px', fontWeight: '700', color: '#475569' }}>{rating}</span>
                                <span className="stars">★★★★★</span>
                                <span className="review-count">({reviewCount})</span>
                            </div>
                            <div className="card-price">
                                {price}
                            </div>
                        </div>
                    </div>
                );
            });
        }
    };

    return (
        <div className="dashboard-container">
            <Navbar />

            <main className="dashboard-main trend-main">
                <div className="trend-inner-container" style={{ maxWidth: '1200px', margin: '0 auto' }}>
                    <div className="trend-header">
                        <div>
                            <h1>Çok Satanlar & Trendler</h1>
                            <p>E-ticaret platformlarındaki en popüler ürünleri keşfedin.</p>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '16px' }}>
                            <div className="trend-controls">
                                <button
                                    className={`personalize-btn ${!isPersonalized ? 'active' : ''}`}
                                    onClick={() => setIsPersonalized(false)}
                                >
                                    Genel Trendler
                                </button>
                                <button
                                    className={`personalize-btn ${isPersonalized ? 'active' : ''}`}
                                    onClick={() => setIsPersonalized(true)}
                                >
                                    Kişiselleştir
                                </button>
                            </div>

                            {isPersonalized && (
                                <div className="ai-advice-section" style={{ marginBottom: 0 }}>
                                    <div className="ai-advice-wrapper">
                                        <button className="ai-advice-btn">
                                            ✨ Size Özel Tavsiyeler
                                        </button>
                                    </div>
                                    {showAiModal && (
                                        <div className="ai-modal-overlay" onClick={() => setShowAiModal(false)}>
                                            <div className="ai-modal-content" onClick={e => e.stopPropagation()}>
                                                <div className="ai-modal-header">
                                                    <h2>✨ Yapay Zeka Tavsiyeleri</h2>
                                                    <button className="close-btn" onClick={() => setShowAiModal(false)}>✕</button>
                                                </div>
                                                <div className="ai-modal-body">
                                                    {aiLoading ? (
                                                        <div className="loading-state">
                                                            <div className="loading-spinner"></div>
                                                            <p>Raporunuz hazırlanıyor...</p>
                                                        </div>
                                                    ) : aiSummary?.error ? (
                                                        <p style={{ color: '#e11d48' }}>{aiSummary.error}</p>
                                                    ) : aiSummary ? (
                                                        <div className="ai-report">
                                                            <div className="report-section">
                                                                <h3>Piyasa Özeti</h3>
                                                                <p>{aiSummary.market_overview}</p>
                                                            </div>
                                                            <div className="report-section">
                                                                <h3>Kişisel Fırsatlar</h3>
                                                                <p>{aiSummary.personal_opportunities}</p>
                                                            </div>
                                                            <div className="report-section">
                                                                <h3>Aksiyon Önerileri</h3>
                                                                <p>{aiSummary.action_suggestions}</p>
                                                            </div>
                                                        </div>
                                                    ) : null}
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>



                    <div className="trend-grid">
                        {renderCards()}
                    </div>
                </div>
            </main>
        </div>
    );
};
