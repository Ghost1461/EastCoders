import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const container = document.querySelector('.landing-container');
        if (!container) return;

        let throttle = false;

        const handleMouseMove = (e) => {
            if (throttle) return;
            throttle = true;
            setTimeout(() => throttle = false, 30); // limit to ~30 bubbles per second

            // Exclude specific elements
            const excludedTags = ['BUTTON', 'A', 'H1', 'H2', 'H3', 'P', 'SPAN', 'HEADER', 'INPUT', 'STRONG', 'B'];
            if (
                excludedTags.includes(e.target.tagName) || 
                e.target.closest('header') || 
                e.target.closest('button') || 
                e.target.closest('.feature-card') || 
                e.target.closest('.cta-card') ||
                e.target.closest('.glass-card')
            ) {
                return;
            }

            const bubble = document.createElement('div');
            bubble.className = 'interactive-bubble';
            bubble.style.left = `${e.pageX}px`;
            bubble.style.top = `${e.pageY}px`;
            
            const size = Math.random() * 25 + 10;
            bubble.style.width = `${size}px`;
            bubble.style.height = `${size}px`;

            container.appendChild(bubble);

            setTimeout(() => {
                bubble.remove();
            }, 800);
        };

        container.addEventListener('mousemove', handleMouseMove);
        
        return () => {
            container.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    return (
        <div className="landing-container">
            {/* Header / Navbar */}
            <header className="landing-header">
                <div className="logo-container">
                    <img src="/logo.png" alt="Stock Radar Logo" className="brand-logo" style={{ height: '48px', objectFit: 'contain' }} />
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
                
                {/* Truck Animation Section */}
                <div className="truck-animation-container">
                    <div className="road"></div>
                    <div className="truck-wrapper">
                        <div className="truck">
                            <div className="truck-body">
                                <span className="truck-logo">S-R</span>
                            </div>
                            <div className="truck-cabin">
                                <div className="truck-window"></div>
                            </div>
                            <div className="wheels">
                                <div className="wheel front-wheel">
                                    <div className="wheel-inner"></div>
                                </div>
                                <div className="wheel back-wheel">
                                    <div className="wheel-inner"></div>
                                </div>
                            </div>
                            <div className="exhaust">
                                <div className="puff puff-1"></div>
                                <div className="puff puff-2"></div>
                                <div className="puff puff-3"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="landing-footer">
                <p>&copy; {new Date().getFullYear()} Stock Radar. Tüm hakları saklıdır.</p>
            </footer>
        </div>
    );
};

export default LandingPage;
