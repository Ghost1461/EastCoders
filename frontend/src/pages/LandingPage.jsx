import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <div className="landing-container">
            {/* Header / Navbar */}
            <header className="landing-header">
                <div className="logo-container">
                    <div className="logo-icon">E</div>
                    <span className="logo-text">EastCoders</span>
                </div>
                <div className="header-actions">
                    <button className="auth-btn" onClick={() => navigate('/login')}>
                        Sign In / Sign Up
                    </button>
                </div>
            </header>

            {/* Hero Section */}
            <main className="landing-main">
                <section className="hero-section">
                    <div className="hero-content">
                        <div className="badge">✨ Yeni Nesil E-Ticaret Yönetimi</div>
                        <h1 className="hero-title">
                            Tüm Pazaryerlerini <br />
                            <span className="gradient-text">Tek Noktadan</span> Yönetin
                        </h1>
                        <p className="hero-subtitle">
                            EastCoders, farklı platformlardaki mağazalarınızı birbirine bağlar, veri analitiği ile satışlarınızı artırmanıza yardımcı olur. Karmaşık süreçleri unutun, otomasyonun keyfini çıkarın.
                        </p>
                        <div className="hero-buttons">
                            <button className="primary-btn" onClick={() => navigate('/signup')}>
                                Hemen Başlayın
                            </button>
                            <button className="secondary-btn" onClick={() => {
                                document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
                            }}>
                                Daha Fazla Bilgi
                            </button>
                        </div>
                    </div>
                    
                    <div className="hero-visual">
                        <div className="glass-card visual-card main-visual">
                            <div className="card-header">
                                <div className="dot red"></div>
                                <div className="dot yellow"></div>
                                <div className="dot green"></div>
                            </div>
                            <div className="card-body">
                                <div className="chart-bar-group">
                                    <div className="chart-bar" style={{height: '60%'}}></div>
                                    <div className="chart-bar" style={{height: '80%'}}></div>
                                    <div className="chart-bar" style={{height: '40%'}}></div>
                                    <div className="chart-bar" style={{height: '100%'}}></div>
                                </div>
                                <div className="stats-row">
                                    <div className="stat-box">
                                        <span className="stat-value">+45%</span>
                                        <span className="stat-label">Satış Artışı</span>
                                    </div>
                                    <div className="stat-box">
                                        <span className="stat-value">3.2k</span>
                                        <span className="stat-label">Aktif Sipariş</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Features Section */}
                <section id="features" className="features-section">
                    <h2 className="section-title">Nasıl Faydalanırım?</h2>
                    <p className="section-subtitle">İşletmenizi büyütmeniz için gereken tüm araçlar burada.</p>
                    
                    <div className="features-grid">
                        <div className="feature-card">
                            <div className="feature-icon bg-blue">🔄</div>
                            <h3 className="feature-title">Platform Entegrasyonu</h3>
                            <p className="feature-desc">Farklı mağaza hesaplarınızı bağlayın. Ürün, sipariş ve değerlendirme verilerinizi tek bir tıkla senkronize edin.</p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon bg-purple">📊</div>
                            <h3 className="feature-title">Gelişmiş Analitik</h3>
                            <p className="feature-desc">Satış eğilimlerinizi, ürün dağılımlarını ve genel mağaza performansınızı dinamik grafiklerle takip edin.</p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon bg-green">⚡</div>
                            <h3 className="feature-title">Trend Analizi</h3>
                            <p className="feature-desc">Pazar trendlerini yakından izleyin, rakiplerinizin önüne geçecek stratejik kararları veri ile alın.</p>
                        </div>
                    </div>
                </section>
                
                {/* CTA Section */}
                <section className="cta-section">
                    <div className="cta-card">
                        <h2>Siz de binlerce mutlu satıcıya katılın</h2>
                        <p>Kayıt olmak tamamen ücretsizdir. Kredi kartı gerekmez.</p>
                        <button className="primary-btn mt-4" onClick={() => navigate('/signup')}>
                            Ücretsiz Hesap Oluştur
                        </button>
                    </div>
                </section>
            </main>

            {/* Footer */}
            <footer className="landing-footer">
                <p>&copy; {new Date().getFullYear()} EastCoders. Tüm hakları saklıdır.</p>
            </footer>
        </div>
    );
};

export default LandingPage;
