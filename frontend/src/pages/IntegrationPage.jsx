import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import { Link, useLocation } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import './IntegrationPage.css';

import trendyolLogo from '../assets/trendyol.jpeg';
import hepsiburadaLogo from '../assets/hepsiburada.jpeg';
import amazonLogo from '../assets/amazon.jpeg';

export const IntegrationPage = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    const [selectedPlatform, setSelectedPlatform] = useState(null);
    const [apiKey, setApiKey] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const [connectedAccounts, setConnectedAccounts] = useState([]);
    const [platformTotals, setPlatformTotals] = useState({});
    const [isSyncingMap, setIsSyncingMap] = useState({});
    const [syncModalData, setSyncModalData] = useState(null);

    useEffect(() => {
        fetchConnectedAccounts();
    }, []);

    const fetchConnectedAccounts = async () => {
        try {
            const response = await api.get('/connected-accounts/');
            if (response.data && response.data.accounts) {
                const activeAccounts = response.data.accounts.filter(acc => acc.is_active);
                setConnectedAccounts(activeAccounts);

                activeAccounts.forEach(acc => {
                    fetchPlatformTotals(acc.platform);
                });
            }
        } catch (error) {
            console.error("Bağlı hesaplar getirilemedi:", error);
        }
    };

    const fetchPlatformTotals = async (platformId) => {
        try {
            const [productsRes, ordersRes, reviewsRes, platformAnalysisRes] = await Promise.all([
                api.get(`/products_display/platform/${platformId}`).catch(() => ({ data: { total: 0 } })),
                api.get(`/orders/platform/${platformId}`).catch(() => ({ data: { total: 0 } })),
                api.get(`/review_display/platform/${platformId}`).catch(() => ({ data: { total: 0 } })),
                api.get(`/orders/analysis/platform`).catch(() => ({ data: { platforms: [] } }))
            ]);

            const platformAnalysis = platformAnalysisRes.data?.platforms?.find(p => p.platform === platformId) || {};

            setPlatformTotals(prev => ({
                ...prev,
                [platformId]: {
                    products: productsRes.data?.count || 0,
                    orders: ordersRes.data?.total || 0,
                    reviews: reviewsRes.data?.total || 0,
                    revenue: platformAnalysis.total_revenue || 0,
                    aov: platformAnalysis.average_order_value || 0
                }
            }));
        } catch (error) {
            console.error(`${platformId} verileri getirilemedi:`, error);
        }
    };


    const platforms = [
        {
            id: 'trendyol',
            name: 'Trendyol',
            color: '#f27a1a',
            logo: trendyolLogo
        },
        {
            id: 'hepsiburada',
            name: 'Hepsiburada',
            color: '#ff6000',
            logo: hepsiburadaLogo
        },
        {
            id: 'amazon',
            name: 'Amazon',
            color: '#232f3e',
            logo: amazonLogo
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

    const handleConnect = async (e) => {
        e.preventDefault();

        if (!apiKey) {
            alert("Lütfen API Key giriniz.");
            return;
        }

        setIsLoading(true);
        try {
            const connectResponse = await api.post(`/connected-accounts/api_key/${selectedPlatform}/connect/by-api-key?api_key=${apiKey}`);
            const { platform, source_user_id } = connectResponse.data;

            const newAccounts = [...connectedAccounts];
            const existingIndex = newAccounts.findIndex(acc => acc.platform === platform);
            if (existingIndex >= 0) {
                newAccounts[existingIndex].source_user_id = source_user_id;
            } else {
                newAccounts.push({ platform, source_user_id });
            }
            setConnectedAccounts(newAccounts);

            setApiKey('');

            await handleManualSync(platform, source_user_id);
            await fetchPlatformTotals(platform);

        } catch (error) {
            console.error("Entegrasyon hatası:", error);
            alert(`Hata: ${error.response?.data?.detail || error.message}`);
        } finally {
            setIsLoading(false);
        }
    };

    const handleManualSync = async (platformId, sourceUserId) => {
        setIsSyncingMap(prev => ({ ...prev, [platformId]: true }));
        try {
            const syncResponse = await api.post(`/sync/source_user/${platformId}/${sourceUserId}`);
            const results = syncResponse.data?.results || {};

            setSyncModalData({
                products: results.products?.new_products || 0,
                orders: results.orders?.created_orders || 0,
                reviews: results.reviews?.created_reviews || 0
            });

            await fetchPlatformTotals(platformId);
        } catch (error) {
            console.error("Senkronizasyon hatası:", error);
            const errorMsg = error.response?.data?.detail || error.message;
            alert(`Hata: ${errorMsg}`);

            if (typeof errorMsg === 'string' && (errorMsg.includes('bağlantılı değil') || errorMsg.includes('not linked'))) {
                handleDisconnect(platformId, sourceUserId);
            }
        } finally {
            setIsSyncingMap(prev => ({ ...prev, [platformId]: false }));
        }
    };

    const handleDisconnect = async (platformId, sourceUserId) => {
        try {
            await api.put(`/connected-accounts/source_user_id/${platformId}/deactivate/${sourceUserId}`);
        } catch (error) {
            console.error("Bağlantı kesme hatası:", error);
        }

        const updatedAccounts = connectedAccounts.filter(acc => acc.platform !== platformId);
        setConnectedAccounts(updatedAccounts);

        setPlatformTotals(prev => {
            const newTotals = { ...prev };
            delete newTotals[platformId];
            return newTotals;
        });
    };

    return (
        <div className="dashboard-container">
            <Navbar />

            <main className="dashboard-main integration-main">
                <div className="integration-header">
                    <h1>Mağaza Entegrasyonları</h1>
                    <p>Satış yaptığınız platformların Api Key'lerini girerek mağazalarınızı birbirine bağlayın.</p>
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

                                {selectedPlatform === platform.id && (() => {
                                    const connectedAcc = connectedAccounts.find(acc => acc.platform === platform.id);

                                    if (connectedAcc) {
                                        const totals = platformTotals[platform.id];
                                        const isPlatformSyncing = isSyncingMap[platform.id];
                                        return (
                                            <div className="connected-platform-details slide-down" style={{ marginTop: '15px', padding: '15px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', textAlign: 'center' }}>
                                                {totals && (
                                                    <div style={{ marginBottom: '15px', textAlign: 'left', backgroundColor: '#fff', padding: '15px', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                                                        <ul style={{ margin: 0, padding: 0, listStyle: 'none', color: '#475569', fontSize: '14px', lineHeight: '1.6' }}>
                                                            <li>Toplam Ürün: <strong>{totals?.products || 0}</strong></li>
                                                            <li>Toplam Sipariş: <strong>{totals?.orders || 0}</strong></li>
                                                            <li>Toplam Yorum: <strong>{totals?.reviews || 0}</strong></li>
                                                            <li>Toplam Ciro: <strong>₺{(totals?.revenue || 0).toLocaleString('tr-TR')}</strong></li>
                                                            <li>Ortalama Sipariş Tutarı: <strong>₺{(totals?.aov || 0).toLocaleString('tr-TR')}</strong></li>
                                                        </ul>
                                                    </div>
                                                )}
                                                <button
                                                    onClick={() => handleManualSync(platform.id, connectedAcc.source_user_id)}
                                                    className="action-btn-sync"
                                                    disabled={isPlatformSyncing}
                                                >
                                                    {isPlatformSyncing ? 'Senkronize Ediliyor...' : 'Senkronize Et (Sync)'}
                                                </button>
                                                <button
                                                    onClick={() => handleDisconnect(platform.id, connectedAcc.source_user_id)}
                                                    className="action-btn-disconnect"
                                                    disabled={isPlatformSyncing}
                                                >
                                                    Bağlantıyı Kes
                                                </button>
                                            </div>
                                        );
                                    }

                                    return (
                                        <form className="api-key-form slide-down" onSubmit={handleConnect}>
                                            <div className="input-group">
                                                <input
                                                    type="text"
                                                    placeholder={`${platform.name} API Key...`}
                                                    value={apiKey}
                                                    onChange={(e) => setApiKey(e.target.value)}
                                                    required
                                                    disabled={isLoading}
                                                />
                                                <button type="submit" className="connect-btn" disabled={isLoading}>
                                                    {isLoading ? 'Bağlanıyor...' : 'Bağla'}
                                                </button>
                                            </div>
                                        </form>
                                    );
                                })()}
                            </div>
                        ))}
                    </div>
                </div>
            </main>

            {syncModalData && (
                <div className="custom-modal-overlay">
                    <div className="custom-modal-content">
                        <h2>Senkronizasyon Tamamlandı!</h2>
                        <div className="sync-results-box">
                            <ul style={{ margin: 0, padding: 0, listStyle: 'none', color: '#475569', fontSize: '15px', lineHeight: '1.8' }}>
                                <li>Eklenen Ürün: <strong>{syncModalData.products}</strong></li>
                                <li>Eklenen Sipariş: <strong>{syncModalData.orders}</strong></li>
                                <li>Eklenen Yorum: <strong>{syncModalData.reviews}</strong></li>
                            </ul>
                        </div>
                        <div className="modal-actions">
                            <button onClick={() => setSyncModalData(null)} className="confirm-btn">
                                Tamam
                            </button>
                        </div>
                    </div>
                </div>
            )}

        </div>
    );
};
