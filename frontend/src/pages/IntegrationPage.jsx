import { useState } from 'react';
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
    const [syncResults, setSyncResults] = useState({});
    const [isSyncingMap, setIsSyncingMap] = useState({});

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
            
            // Otomatik olarak ilk senkronizasyonu başlat
            await handleManualSync(platform, source_user_id);
            
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
            setSyncResults(prev => ({
                ...prev,
                [platformId]: syncResponse.data.results
            }));
        } catch (error) {
            console.error("Senkronizasyon hatası:", error);
            const errorMsg = error.response?.data?.detail || error.message;
            alert(`Hata: ${errorMsg}`);
            
            // Eğer backend veritabanı sıfırlanmışsa ve bağlantı yok diyorsa, frontend'den de sil
            if (typeof errorMsg === 'string' && (errorMsg.includes('bağlantılı değil') || errorMsg.includes('not linked'))) {
                handleDisconnect(platformId);
            }
        } finally {
            setIsSyncingMap(prev => ({ ...prev, [platformId]: false }));
        }
    };

    const handleDisconnect = (platformId) => {
        const updatedAccounts = connectedAccounts.filter(acc => acc.platform !== platformId);
        setConnectedAccounts(updatedAccounts);
        
        // Remove from syncResults if exists
        setSyncResults(prev => {
            const newResults = { ...prev };
            delete newResults[platformId];
            return newResults;
        });
    };

    return (
        <div className="dashboard-container">
            <Navbar />

            <main className="dashboard-main integration-main">
                <div className="integration-header">
                    <h1>Mağaza Entegrasyonları</h1>
                    <p>Satış yaptığınız platformların User ID'lerini girerek mağazalarınızı birbirine bağlayın.</p>
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
                                        const result = syncResults[platform.id];
                                        const isPlatformSyncing = isSyncingMap[platform.id];
                                        return (
                                            <div className="connected-platform-details slide-down" style={{ marginTop: '15px', padding: '15px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', textAlign: 'center' }}>
                                                {result && (
                                                    <div style={{ marginBottom: '15px', textAlign: 'left', backgroundColor: '#fff', padding: '15px', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                                                        <h4 style={{ margin: '0 0 10px 0', color: '#0f172a', fontSize: '16px' }}>Aktarım Tamamlandı</h4>
                                                        <p style={{ margin: '0 0 10px 0', fontSize: '13px', color: '#64748b' }}><strong>{platform.name}</strong> verileri başarıyla sisteme aktarıldı.</p>
                                                        <ul style={{ margin: 0, padding: 0, listStyle: 'none', color: '#475569', fontSize: '14px', lineHeight: '1.6' }}>
                                                            <li>Eklenen Ürün: <strong>{result.products?.new_products || 0}</strong></li>
                                                            <li>Eklenen Sipariş: <strong>{result.orders?.created_orders || 0}</strong></li>
                                                            <li>Eklenen Yorum: <strong>{result.reviews?.created_reviews || 0}</strong></li>
                                                        </ul>
                                                    </div>
                                                )}
                                                <button 
                                                    onClick={() => handleManualSync(platform.id, connectedAcc.source_user_id)}
                                                    className="connect-btn" 
                                                    style={{ width: '100%', backgroundColor: '#3b82f6' }}
                                                    disabled={isPlatformSyncing}
                                                >
                                                    {isPlatformSyncing ? 'Senkronize Ediliyor...' : 'Senkronize Et (Sync)'}
                                                </button>
                                                <button 
                                                    onClick={() => handleDisconnect(platform.id)}
                                                    className="connect-btn" 
                                                    style={{ width: '100%', marginTop: '10px', backgroundColor: '#ef4444' }}
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


        </div>
    );
};
